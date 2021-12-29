from ytmusicapi import YTMusic
import bugs_loader as BugsLoader
import bugs_parser as BugsParser
import bugs_builder as BugsBuilder
import bugs_logger as BugsLogger

'''
1. read file from albums.txt -> [url]
2. [url] -> [html_dom]
3. [html_dom] -> (title, [song_entity])
4. (title, [song_entity]) -> (title, [search_entity])
5. (title, [search_entity]) -> ytmusic playlist
'''
loader = BugsLoader.Loader()
parser = BugsParser.Parser()
builder = BugsBuilder.Builder()
logger = BugsLogger.Logger()
album_links = loader.load_playlist_links('albums.txt')
album_html_doms = [loader.load_html(album_link) for album_link in album_links]
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
