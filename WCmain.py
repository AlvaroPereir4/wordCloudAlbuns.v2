from src.WCParser import WCParser
from src.WCCrawler import WCCrawler


def main():
    parser = WCParser()
    crawler = WCCrawler(parser)
    wordcloud_data = crawler.crawler()
    print(wordcloud_data)


if __name__ == "__main__":
    main()
