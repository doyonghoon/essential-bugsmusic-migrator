import requests

class Loader:
    def __init__(self):
        pass

    def remove_commented_out_line(self, line):
        tmp_line = line.replace("://", "___")
        url = tmp_line.split("//")[0].strip().replace("___", "://")
        return url

    def load_html(self, url):
        body = requests.get(url)
        return body.text

    def load_playlist_links(self, album_filepath):
        links = list()
        with open(album_filepath, 'r') as infile:
            links.extend(infile.readlines())
        return [self.remove_commented_out_line(line) for line in lines]
