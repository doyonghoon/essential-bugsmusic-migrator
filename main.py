import requests
from bs4 import BeautifulSoup
import json
from ytmusicapi import YTMusic
from os import listdir
from os.path import isfile, join

class Loader:
    def __init__(self):
        pass

    def load(self, url):
        body = requests.get(url)
        return body.text

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
f = open("playlist.html", 'r')
data = f.read()
f.close()
'''

'''
data = Loader().load("https://music.bugs.co.kr/musicpd/albumview/45863")
ptitle, body = Parser().generate_json(data)
OutputWriter().generate_file(ptitle, body)
'''
queries = OutputWriter().build_search_queries()
ytmusic = YTMusic('headers_auth.json')
for query in queries:
    title, search_queries = query
    print(title)
    playlistId = ytmusic.create_playlist(title, title)
    for q in search_queries:
        search_result = ytmusic.search(q)[0]
        print(search_result)
        ytmusic.add_playlist_items(playlistId, [search_result['videoId']])
