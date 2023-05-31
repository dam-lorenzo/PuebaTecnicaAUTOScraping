import argparse
from crawler.crawler import Crawler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--storeName', type=str, help='Store name to scrap', default=None)
    parser.add_argument('--storeIndex', type=str, help='Store index to scrap', default=None)
    parser.add_argument('--input', type=bool, help='If you want to enter the store manually', nargs='?', const=True, default=False)
    args = parser.parse_args()
    store_name = args.storeName
    store_index = args.storeIndex
    use_input = args.input
    crawler = Crawler(store_name=store_name, store_index=store_index, use_input=use_input)
    crawler.run()