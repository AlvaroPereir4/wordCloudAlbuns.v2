import requests
from lxml.html import fromstring
from src.WCParser import WCParser


class WCCrawler:

    def __init__(self, parser: WCParser):
        self._parser = parser

    def run_rqs_get_wordcloud(self, url: str):
        response = requests.get(url)
        tree = fromstring(response.text)
        track_html_elements = self._parser.element_list(tree, '//h3[@class="chart_row-content-title"]/text()')

        tittles = []
        if track_html_elements:
            for index, html_element in track_html_elements.items():
                position_0_elements = track_html_elements.get(index, [])
                for element in position_0_elements:
                    text = element.strip()

                    if text and '.' in text:
                        text = text.split('.')[0].strip()
                        tittles.append(text)

        song_lyrics = []
        for tittle in tittles:
            url_base = f'https://www.letras.mus.br/kendrick-lamar/{tittle}/'
            request_song = requests.get(url_base)
            tree = fromstring(request_song.text)
            lyric_elements = self._parser.element_list(tree, '//*[@class="lyric-original"]/p/text()')
            song_lyrics.append(lyric_elements)

        album_lyric = ' ' + ' '.join([self._parser.remove_unsual_caracters(str(valor)) for dictionary in song_lyrics
                                      for valor in dictionary.values()])
        wc = self._parser.wordcloud_album(album_lyric)
        wc.to_file("wordcloud.png")
