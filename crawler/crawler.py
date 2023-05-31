import json
import os
import csv

from typing                 import Generator
from datetime               import datetime

from html2text              import html2text
from utils.api_keys         import ApiKeys
from utils.payload          import Payload, PayloadKeys
from utils.request_handler  import RequestHandler
from utils.url              import URL

CSVS_PATH = os.path.join('.', 'data')

class Crawler():

    def __init__(self, store_name: str = None, store_index: str = None, use_input: bool = False) -> None:
        self.requester = RequestHandler()
        self.created_at = datetime.now().strftime('%Y-%m-%d')
        self.store = store_name
        self.use_input = use_input
        self.store_index = store_index
        self.scraped_products = list()
        self.scraped_ids = set()

    def run(self) -> None:
        """Runs the crawler
        """
        for store, store_index, header in self.get_stores():
            print(f'Scraping {store}')
            self.requester.update_headers(header)
            for category in self.__get_categories():
                self.__scrap_products(category, store_index)
                if len(self.scraped_products) > 300:
                    self.__save_csv(store)
            if self.scraped_products:
                self.__save_csv(store)
            self.scraped_ids.clear()
        print('Scraping finished')

    def __get_categories(self) -> Generator:
        """Gets the slug of each category to be used in the products api

        Yields:
            Generator: string with the category slug
        """
        url_categories = URL.CATEGORIES
        categories = self.requester.get_response(url_categories)
        for categorie in categories:
            print(f'Scraping category {categorie[ApiKeys.name]}')
            if categorie[ApiKeys.hasChildren]:
                for i, children in enumerate(categorie[ApiKeys.children]):
                    children_slug = children[ApiKeys.url].replace(URL.BASE, '')
                    print(f'Children {children[ApiKeys.name]} {i + 1}/{len(categorie[ApiKeys.children])}')
                    yield children_slug

    def __scrap_products(self, slug: str, store_index: str, _from: int = 0) -> None:
        """Recursive method
        Iterate over each category until obtaining all the products it contains.
        Args:
            slug (str): slug of the category
            store_index (str): index of the store, obtained from get_store method
            _from (int, optional): Paginator that iterates through the entire category, start from 0. Defaults to 0.
        """
        category_url = URL.get_products_url(slug, _from, store=store_index)
        products = self.requester.get_response(category_url)
        if not products:
            return
        for product in products:
            item = product[ApiKeys.items][0]
            _id = item[ApiKeys.itemId]
            name = item[ApiKeys.name]
            if _id in self.scraped_ids:
                print(f'Item {_id} {name} already scrapped')
                continue
            print(f'Scraping item: {_id} - {name}')
            sellers = item[ApiKeys.sellers][0]
            self.scraped_ids.add(_id)
            payload = Payload()
            payload.id = _id
            payload.productReference = product[ApiKeys.productId]
            payload.name = name
            payload.completeName = item[ApiKeys.nameComplete]
            payload.brand = product[ApiKeys.brand]
            payload.brandId = product[ApiKeys.brandId]
            payload.categories = self.__get_product_categories(product[ApiKeys.categories])
            payload.link = product[ApiKeys.link]
            payload.description = self.__get_description(product[ApiKeys.description])
            payload.isKit = item[ApiKeys.isKit]
            payload.images = self.__get_images(item[ApiKeys.images])
            payload.sellerId = sellers[ApiKeys.sellerId]
            payload.sellerName = sellers[ApiKeys.sellerName]
            payload.price = sellers[ApiKeys.commertialOffer][ApiKeys.Price]
            payload.listPrice = sellers[ApiKeys.commertialOffer][ApiKeys.ListPrice]
            payload.priceWithoutDiscount = sellers[ApiKeys.commertialOffer][ApiKeys.PriceWithoutDiscount]
            payload.priceValidUntil = sellers[ApiKeys.commertialOffer][ApiKeys.PriceValidUntil]
            payload.stock = sellers[ApiKeys.commertialOffer][ApiKeys.AvailableQuantity]
            payload.paymentOptions = self.__get_payment_options(sellers[ApiKeys.commertialOffer][ApiKeys.PaymentOptions])
            payload.releaseDate = product[ApiKeys.releaseDate]
            payload.createdAt = self.created_at
            self.scraped_products.append(payload.create_payload())
        self.__scrap_products(slug, store_index=store_index, _from = _from + URL.steps + 1)

    def __get_product_categories(self, categories: list) -> list:
        """Clean the categories list obtained from the api

        Args:
            categories (list): categories list obtained from the api

        Returns:
            list: list with clean and unique categories
        """
        format_categories = {cat for item in categories for cat in item.split('/') if cat}
        return list(format_categories)
    
    def __get_description(self, description: str) -> str:
        """Converts an html string into a normal string

        Args:
            description (str): string with html

        Returns:
            str: readable text
        """
        return html2text(description)

    def __get_images(self, images: list) -> list:
        """Extracts the image URLs from a list of image dictionaries.

        Args:
        - images: List of image dictionaries.

        Returns:
        - List of image URLs extracted from the input.
        """
        return [item[ApiKeys.imageUrl] for item in images]
    
    def __get_payment_options(self, payment_options: list) -> list:
        """Process the payment options and generate a structured list of payments.

        Args:
        - payment_options: Payment options (dict).

        Returns:
        - payment_list: Processed list of payments (list).
        """
        payment_list = list()
        installment_options = dict()
        installments = list()
        for payment in payment_options[ApiKeys.installmentOptions]:
            for installment in payment[ApiKeys.installments]:
                installments.append({
                    PayloadKeys.installments: installment[ApiKeys.count],
                    PayloadKeys.monthlyPayment: installment[ApiKeys.value],
                    PayloadKeys.total: installment[ApiKeys.total],
                    PayloadKeys.interestRate: installment[ApiKeys.interestRate],
                })
            installment_options.update({
                payment[ApiKeys.paymentName]: installments.copy(),
            })
            installments.clear()
        for option in payment_options[ApiKeys.paymentSystems]:
            payment_list.append({
                PayloadKeys.type: option[ApiKeys.name],
                PayloadKeys.options: installment_options[option[ApiKeys.name]],
                PayloadKeys.validUntil: option[ApiKeys.dueDate]
            })
        return payment_list

    def __save_csv(self, name: str) -> None:
        """save the current scraping into a csv file

        Args:
            name (str): name of the curren store
        """
        file_name = f'{name.replace(" ", "")}_{self.created_at.replace("-", "")}.csv'
        if not os.path.exists(CSVS_PATH):
            os.mkdir(CSVS_PATH)
        file_exists = os.path.isfile(path_file)
        headers = list(self.scraped_products[0].keys())
        path_file = os.path.join(CSVS_PATH, file_name)
        with open(path_file, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=headers, delimiter=';')
            if not file_exists:
                writer.writeheader()
            writer.writerows(self.scraped_products)
        self.scraped_products.clear()
    
    def get_stores(self) -> Generator:
        """Generator function that yields store information based on the specified criteria.

        Yields:
        - Tuple containing store name, index, and request headers.

        """
        soup = self.requester.get_soup(URL.STORES)
        json_tag = soup.find("div", id="stores-data")
        stores = json.loads(json_tag.text)
        if self.use_input:
            stores_names = [f'\n\t{i+1}. {store[ApiKeys.name]}' for i, store in enumerate(stores[ApiKeys.stores])]
            while True:
                try:
                    self.store_index = int(input(f"Elija una opcion:\n{''.join(stores_names)}\n\nOpcion: ")) - 1
                    break
                except ValueError:
                    print('La opcion no es valida')
        for i, store in enumerate(stores[ApiKeys.stores]):
            store_name = store[ApiKeys.name]
            if self.store and self.store.lower() not in store_name.lower():
                continue
            elif (self.use_input or self.store_index) and i != self.store_index:
                continue
            yield store_name, str(i+1), {
                'Cookie': f'userSelectedStore=true; storeSelectorId={store[ApiKeys.id]};'
            }