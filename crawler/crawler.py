from typing                 import Generator
from utils.api_keys         import ApiKeys
from utils.request_handler  import RequestHandler
from utils.url              import URL

class Crawler():

    def __init__(self) -> None:
        self.requester = RequestHandler()

    def run(self) -> None:
        for category in self.get_categories():
            category_url = URL.get_products_url(category)
            products = self.requester.get_response(category_url)
            print(products)
        print('Scraping finished')

    def get_categories(self) -> Generator:
        url_categories = URL.CATEGORIES
        categories = self.requester.get_response(url_categories)
        for categorie in categories:
            print(f'Scraping category {categorie[ApiKeys.name]}')
            if categorie[ApiKeys.hasChildren]:
                for i, children in enumerate(categorie[ApiKeys.children]):
                    children_slug = children[ApiKeys.url].replace(URL.BASE, '')
                    print(f'Children {children[ApiKeys.name]} {i + 1}/{len(categorie[ApiKeys.children])}')
                    yield children_slug