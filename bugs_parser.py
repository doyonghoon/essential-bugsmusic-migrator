from bs4 import BeautifulSoup

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
