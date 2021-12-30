import json
import regex
import glob
import os
from os import listdir
from os.path import isfile, join

class Builder:
    def __init__(self):
        pass

    def delete_hangul(self, s):
        is_hangul = lambda x: True if regex.search(r'\p{IsHangul}', x) else False
        i = s.find('(')
        j = s.find(')')
        candidate = s[i+1:j] if i >= 0 and j >= 0 else ""
        if is_hangul(candidate):
            res = s[:i] + s[j+1:]
            return res.strip().replace("  ", " ")
        return s

    def build_search_query(self, playlist_entity):
        title, song_entities = playlist_entity
        queries = [" ".join([self.delete_hangul(song['artist']), song['title'], song['album']]) for song in song_entities]
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
