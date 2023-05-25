import argparse
from crawler.crawler import Crawler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    crawler = Crawler()
    crawler.run()