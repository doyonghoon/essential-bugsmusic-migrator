# Music Playlist Parser

Migrates playlists from Bugs Music to your Youtube Music library.

# Motivation of the project

My day always goes on with listening to the curated playlists of [Essential](https://www.youtube.com/c/essentialme) for different themes of a day. I love playing their compiled playlists, but a single track of each playlist plays for more than an hour. A minor issue that I've been constantly facing is that I am unable to skip a particular song even if I want to because the playlist is burnt-in as a whole package for the curated songs. Also, even if I find great song to feed in as a seed music to the ML of Youtube Music for recommendations, it would be little hectic for me to pause the music and find the title in order to add into my library. I thought it would make my life much pleasant if I would be able to migrate these playlists to my local library in Youtube Music.

# Installation

This project has been developed in Python `3.9.6`.

* Install dependencies by running `pip install pipreqs`. You can also find a complete list of dependencies at `requirements.txt`.


# Usage

* To link your Youtube Music account with the project, you have to provide `headers_auth.json` file on a root directory of the project. Refer to [this doc](https://ytmusicapi.readthedocs.io/en/latest/setup.html#authenticated-requests) for more info. A template of the request header looks like following:

```json
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "X-Goog-AuthUser": "0",
    "x-origin": "https://music.youtube.com",
    "Cookie" : "<YOUR COOKIE GOES HERE>"
}
```

* Create a file called `albums.txt` and put your album url into the file. Its content should look like following:

```
// https://music.bugs.co.kr/musicpd/albumview/45863
https://music.bugs.co.kr/musicpd/albumview/49912
https://music.bugs.co.kr/musicpd/albumview/48678
```

A migrater reads these urls by line, and will treat it as a ready-to-parse if it starts with `http`. Commenting out like `//` will silently drop the url to be parsed.

* You can find album links of Bug Music from the description section of [each playlist](https://www.youtube.com/watch?v=z060aThI9qM) in Essential channel of Youtube. Or, you can also find the full list of playlists from [the link](https://music.bugs.co.kr/musicpd/).

* Run `python3 main.py`


## Example

Once you run, the migrater will display the title of your new playlist in your Youtube Music, and will tell you whether each song is successfully added by ✅. Though, when the song is not found on Youtube Music, you will see the emoji character ❌, and eventually you will see a new file called `not_found.txt` after the program ends. This file will contain all missing songs from your playlist.

```
$ python3 main.py
문득 그때가 떠올라 chillin tape
- ✅ "keshi 2 soon THE REAPER"
- ✅ "slchld she likes spring, I prefer winter. she likes spring, I prefer winter."
- ✅ "heyden miller decade"
- ✅ "Authentic Solioquy (Feat. Slchld) CLICHE"
- ✅ "Authentic Take 1 CLICHE"
- ✅ "keshi like i need u THE REAPER"
- ✅ "RINI My Favourite Clothes My Favourite Clothes"
- ✅ "eli. say those things i gave you everything i had."
- ✅ "Ant Saunders I Had A Love Song (feat. VanJess) I Had A Love Song (feat. VanJess)"
- ✅ "Dept Autumn breeze (Feat. Milky Day) Autumn breeze"
- ✅ "Sarah Kang Drive (Feat. Kevin Chung) Drive"
- ✅ "Niia Black Dress (CODE KUNST Remix) Black Dress (CODE KUNST Remix)"
- ✅ "Paige Cold Blooded Always Growing EP"
- ✅ "Ok2222 Someone New Someone New"
- ✅ "UMI Frequently Interlude - EP"
- ✅ "Conan Gray Comfort Crowd Kid Krow"
- ✅ "Pink Sweat$ At My Worst The Prelude"
- ✅ "Jesse Barrera Unaware Unaware"
- ✅ "Bruno Major Regent’s Park To Let A Good Thing Die"
- ✅ "sakehands LUCK (feat. Jessica Domingo) Self-HATE"
- ✅ "HONNE Day 1 ◑ Love Me / Love Me Not"
- ❌ "brb. whoops relationsh*t"
- ✅ "Of Methodist Bayfront Stn Bayfront Stn"
- ✅ "Peach Tree Rascals Plus Plus"
- ✅ "heyden Parking lot Parking lot"
- ✅ "guardin alone in the attic creature pt. 1"
- ✅ "Powfu no promises some boring love stories pt 5"
- ✅ "Powfu death bed (coffee for your head) poems of the past"
- ✅ "Hans. Empties Empties"
- ✅ "Hiyo Don't Go Shoegaze"

Done!
```

Example of `not_found.txt` file.

* Each line will keep the following format: `[PLAYLIST_TITLE]: SONG_TITLE`.

```
[2021 크리스마스 시즌송 신곡 모음 (수시 업뎃)]: Sally Boy Baby, It's Christmas Baby, It's Christmas
[달짝지근 기분 좋아지는 Daily Pop 11]: Will Jay Was It Even Real? Was It Even Real?
[달짝지근 기분 좋아지는 Daily Pop 11]: Pablo Brooks Not Like the Movies Not Like the Movies
[문득 그때가 떠올라 chillin tape]: brb. whoops relationsh*t
[기분 좋아지는 cheerful 레트로 감성]: MUNA Loudspeaker The Loudspeaker EP
[기분 좋아지는 cheerful 레트로 감성]: Grate Lakes Super Special LTC
[달짝지근 기분 좋아지는 Daily Pop 2]: Olly Murs Mark On My Heart You Know I Know (Expanded Edition)
[문득 그때가 떠올라 chillin tape]: brb. whoops relationsh*t
[Coffee And Cigarette, Chillax BGM]: Sky.High I Think I'm In Love Discography
```

# Contribution

Pull requests and ideas noting in Issues are always welcome.

# License

The MIT License (MIT)

Copyright (c) 2021 Yong Hoon Do

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
