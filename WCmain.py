from src.WCParser import WCParser
from src.WCCrawler import WCCrawler


def main():
    parser = WCParser()
    crawler = WCCrawler(parser)
    url = 'https://genius.com/albums/Kendrick-lamar/Damn'
    wordcloud_data = crawler.crawler(url)
    print("Dados extraídos para WordCloud:")
    print(wordcloud_data)


if __name__ == "__main__":
    main()
