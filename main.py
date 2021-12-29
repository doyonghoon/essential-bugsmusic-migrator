import requests
from bs4 import BeautifulSoup
import json
from ytmusicapi import YTMusic
from os import listdir
from os.path import isfile, join

class Loader:
    def __init__(self):
        pass

    def load_html(self, url):
        body = requests.get(url)
        return body.text

    def load_playlist_links(self, album_filepath):
        should_exclude = lambda s: s.startswith("//")
        links = list()
        with open(album_filepath, 'r') as infile:
            links.extend(infile.readlines())
        return [link.replace("\n", "") for link in links if link.startswith("http") and not should_exclude(link)]

class Parser:
    def __init__(self):
        pass

    def _get_title(self, soup):
        playlisttitle = soup.find_all("h1")
        return playlisttitle[2].text

    def generate_json(self, data):
        soup = BeautifulSoup(data, 'html.parser')
        playlisttitle = self._get_title(soup)
        mytitles = soup.find_all("p", { "class": "title" })
        myartists = soup.find_all("p", { "class": "artist" })
        myalbums = soup.find_all("a", { "class": "album" })
        res = list()
        for a, b, c in zip(mytitles, myartists, myalbums):
            if (a.find("a")):
                res.append({ "title": a.find("a").text, "artist": b.find("a").text, "album": c.text })
        return (playlisttitle, res)

class OutputWriter:
    def __init__(self):
        pass

    def generate_file(self, ptitle, body):
        with open('playlists/' + ptitle + '.json', 'w') as outfile:
            pretty_body = json.dumps(body, indent=2)
            outfile.write(pretty_body)
    
    def build_search_queries(self):
        res = list()
        playlists = [f for f in listdir('playlists') if isfile(join('playlists', f))]
        for filename in playlists:
            with open('playlists/' + filename, 'r') as json_file:
                songs = json.load(json_file)
                queries = [" ".join([song['artist'], song['title'], song['album']]) for song in songs]
                res.append((filename.replace(".json", ""), queries))
        return res

'''
1. read file from albums.txt -> [link]
2. [link] -> [html_dom]
3. [html_dom] -> (title, [song_entity])
4. (title, [song_entity]) -> playlists/title.json
5. title.json -> ytmusic playlist
'''

loader = Loader()
parser = Parser()
album_links = loader.load_playlist_links('albums.txt')
album_html_doms = [Loader().load_html(album_link) for album_link in album_links]
song_entities = [parser.generate_json(album_html_dom) for album_html_dom in album_html_doms]
for song_title, song_metadata_body in song_entities:
    OutputWriter().generate_file(song_title, song_metadata_body)
    print('wrote a file (\"{}.json\") w/ {} of songs'.format(song_title, len(song_metadata_body)))

queries = OutputWriter().build_search_queries()
ytmusic = YTMusic('headers_auth.json')
for query in queries:
    title, search_queries = query
    print(title)
    playlistId = ytmusic.create_playlist(title, title)
    for q in search_queries:
        search_results = ytmusic.search(q)
        if len(search_results) == 0:
            print('❌ "{}"'.format(q))
            continue

        search_result = search_results[0]
        if 'videoId' in search_result:
            ytmusic.add_playlist_items(playlistId, [search_result['videoId']])
            print('✅ "{}"'.format(q))
        else:
            print('❌ "{}"'.format(q))
