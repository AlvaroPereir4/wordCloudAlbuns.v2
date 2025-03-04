import requests
from src.WCParser import WCParser


class WCCrawler:

    def __init__(self, parser: WCParser):
        self._parser = parser

    def crawler(self):
        url = self.get_url()
        main_response = requests.get(url)
        titles = self._parser.get_song_titles(main_response)
        song_lyrics = self.song_lyrics_requests(titles)
        self._parser.parser(song_lyrics)

    def song_lyrics_requests(self, titles: list) -> list:
        song_lyrics = []
        for tittle in titles:
            url_base = f'https://www.letras.mus.br/kendrick-lamar/{tittle}/'
            song_response = requests.get(url_base)
            song_lyrics.append(self._parser.get_song_lyric(song_response))

        return song_lyrics

    def get_url(self) -> str:
        artist = input("Artist?")
        url_albums = f'https://genius.com/artists/{artist}/albums'
        albums_request = requests.get(url_albums)
        album = self._parser.get_albums_from_response(albums_request)
        url = f'https://genius.com/albums/{artist}/{album}'

        return url
