import requests
from bs4 import BeautifulSoup
import json
from ytmusicapi import YTMusic
from os import listdir
from os.path import isfile, join
import glob
import os
import regex

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

class Builder:
    def __init__(self):
        pass

    def __delete_hangul(self, s):
        is_hangul = lambda x: True if regex.search(r'\p{IsHangul}', x) else False
        i = s.find('(')
        j = s.find(')')
        candidate = s[i+1:j]
        if is_hangul(candidate):
            res = s[:i] + s[j+1:]
            return res
        return s

    def build_search_query(self, playlist_entity):
        title, song_entities = playlist_entity
        queries = [" ".join([self.__delete_hangul(song['artist']), song['title'], song['album']]) for song in song_entities]
        return (title, queries)

    def build_search_queries_from_files(self):
        res = list()
        playlists = [f for f in listdir('playlists') if isfile(join('playlists', f))]
        for filename in playlists:
            with open('playlists/' + filename, 'r') as json_file:
                songs = json.load(json_file)
                queries = [" ".join([song['artist'], song['title'], song['album']]) for song in songs]
                res.append((filename.replace(".json", ""), queries))
        return res


    def generate_file(self, ptitle, body):
        with open('playlists/' + ptitle + '.json', 'w') as outfile:
            pretty_body = json.dumps(body, indent=2)
            outfile.write(pretty_body)

    def cleanup_json_files(self):
        files = glob.glob('playlists/*.json')
        for f in files:
            try:
                os.remove(f)
                print('✅ file deleted: "{}"'.format(f))
            except OSError as e:
                print("Error: {} : {}".format(f, e.strerror))

class Logger:
    def __init__(self):
        self.notfounds = list()

    def add_song_not_found(self, search_entity):
        self.notfounds.append(search_entity)

    def write_not_founds(self):
        if len(self.notfounds) > 0:
            for entity in self.notfounds:
                title, body = entity
                with open('not_founds.txt', 'a') as outfile:
                    line = "[{}]: {}".format(title, body)
                    outfile.write(line)
                    outfile.write("\n")

'''
1. read file from albums.txt -> [link]
2. [link] -> [html_dom]
3. [html_dom] -> (title, [song_entity])
4. (title, [song_entity]) -> (title, [search_entity])
5. (title, [search_entity]) -> ytmusic playlist
'''

loader = Loader()
parser = Parser()
builder = Builder()
logger = Logger()
album_links = loader.load_playlist_links('albums.txt')
album_html_doms = [Loader().load_html(album_link) for album_link in album_links]
playlist_entities = [parser.generate_json(album_html_dom) for album_html_dom in album_html_doms]
query_entities = [builder.build_search_query(entity) for entity in playlist_entities]

ytmusic = YTMusic('headers_auth.json')
for query in query_entities:
    title, search_queries = query
    print(title)
    playlistId = ytmusic.create_playlist(title, title)
    for q in search_queries:
        search_results = ytmusic.search(q)
        if len(search_results) == 0:
            print('- ❌ "{}"'.format(q))
            logger.add_song_not_found((title, q))
            continue

        search_result = search_results[0]
        if 'videoId' in search_result:
            ytmusic.add_playlist_items(playlistId, [search_result['videoId']])
            print('- ✅ "{}"'.format(q))
        else:
            print('- ❌ "{}"'.format(q))
            logger.add_song_not_found((title, q))
    print("\n")

builder.cleanup_json_files()
logger.write_not_founds()
print("Done!\n")
