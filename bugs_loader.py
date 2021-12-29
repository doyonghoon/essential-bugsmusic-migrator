import requests

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
