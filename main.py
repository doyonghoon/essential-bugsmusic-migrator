import requests
from bs4 import BeautifulSoup
import json

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
        with open(ptitle + '.json', 'w') as outfile:
            json.dump(body, outfile)

'''
f = open("playlist.html", 'r')
data = f.read()
f.close()
'''

data = Loader().load("https://music.bugs.co.kr/musicpd/albumview/45863")
ptitle, body = Parser().generate_json(data)
OutputWriter().generate_file(ptitle, body)
