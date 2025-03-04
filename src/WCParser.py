import re
from lxml.html import fromstring
from matplotlib.colors import LinearSegmentedColormap
from requests import Response
from wordcloud import WordCloud, STOPWORDS
import logging
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')  # Usando o backend TkAgg, que suporta exibição interativa


class WCParser:

    def parser(self, song_lyrics: list):
        album_lyric = self.get_album_lyrics(song_lyrics)

        self.log_general_info(song_lyrics, album_lyric)
        self.wordcloud_album(album_lyric)

    def element_list(self, tree, xpath_expression) -> dict:
        elements = tree.xpath(xpath_expression)
        elements_by_position = {}
        for element in elements:
            position = elements.index(element)
            if position not in elements_by_position:
                elements_by_position[position] = []
            elements_by_position[position].append(element)

        return elements_by_position

    def remove_unsual_caracters(self, phrase: str) -> str:
        return re.sub(r'[^a-zA-Z\s]', '', phrase)

    def wordcloud_album(self, lyric_text: str):
        colors = ["#A93830", "#F28E37", "#CD622B", '#88733C']
        cmap = LinearSegmentedColormap.from_list("mycmap", colors)
        wordcloud = WordCloud(
            stopwords=STOPWORDS,
            contour_width=1,
            width=1600,
            height=800,
            colormap=cmap,
            contour_color='blue',
            random_state=50,
            font_path='./impact.ttf').generate(lyric_text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
        wordcloud.to_file("wordcloud.png")

    def get_song_titles(self, response: Response) -> list:
        tree = fromstring(response.text)
        titles_songs_elements_xpath = '//h3[@class="chart_row-content-title"]/text()'
        titles_songs_elements = self.element_list(tree, titles_songs_elements_xpath)
        tittles = []

        if titles_songs_elements:
            for index, html_element in titles_songs_elements.items():
                position_0_elements = titles_songs_elements.get(index, [])
                for element in position_0_elements:
                    text = element.strip()

                    if text and '.' in text:
                        text = text.split('.')[0].strip()
                        tittles.append(text)

        return tittles

    def get_song_lyric(self, response: Response) -> dict:
        tree = fromstring(response.text)
        lyric_elements = self.element_list(tree, '//*[@class="lyric-original"]/p/text()')

        return lyric_elements

    def get_album_lyrics(self, song_lyrics: list) -> str:
        processed_values = [
            self.remove_unsual_caracters(str(valor))
            for dictionary in song_lyrics
            for valor in dictionary.values()
        ]
        album_lyric = ' ' + ' '.join(processed_values)

        return album_lyric

    def log_general_info(self, song_lyrics: list, album_lyric: str):
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        words = album_lyric.split()

        logging.info(f"🎵 Quantity of songs: {len(song_lyrics)}")
        logging.info(f"📖 Total words: {len(words)}")
        logging.info(f"🔤 Unique words: {len(set(words))}")

    def get_albums_from_response(self, albums: Response) -> str:
        tree = fromstring(albums.text)
        album_list = self.element_list(tree, '//div/h3/text()')  #todo nao ta retornando todos
        album_list_formated = []
        print("Artist albuns: ")

        for idx, album in album_list.items():
            album_name = album[0] if isinstance(album, list) else album
            clean_album = ''.join(e for e in album_name if e.isalnum() or e.isspace())
            album_list_formated.append(clean_album)
            print(f"{idx}: {clean_album}")

        album_id = int(input("Choose the album by number: "))
        album_choose = album_list_formated[album_id]

        return album_choose
