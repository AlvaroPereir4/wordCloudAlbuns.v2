import re
from matplotlib.colors import LinearSegmentedColormap
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


class WCParser:

    def element_list(self, tree, xpath_expression):
        elements = tree.xpath(xpath_expression)
        elements_by_position = {}
        for element in elements:
            position = elements.index(element)
            if position not in elements_by_position:
                elements_by_position[position] = []
            elements_by_position[position].append(element)

        return elements_by_position

    def remove_unsual_caracters(self, phrase: str):
        return re.sub(r'[^a-zA-Z\s]', '', phrase)

    def wordcloud_album(self, lyric_text):
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

        return wordcloud
