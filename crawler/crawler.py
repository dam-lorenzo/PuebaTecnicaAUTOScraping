import os
import csv

from typing                 import Generator

from html2text              import html2text
from utils.api_keys         import ApiKeys
from utils.payload          import Payload, PayloadKeys
from utils.request_handler  import RequestHandler
from utils.url              import URL

CSVS_PATH = os.path.join('.', 'data')

class Crawler():

    def __init__(self) -> None:
        self.requester = RequestHandler()
        self.scraped_products = list()
        self.scraped_ids = set()

    def run(self) -> None:
        for category in self.__get_categories():
            self.__scrap_products(category)
            self.__save_csv()
            if len(self.scraped_products) > 300:
                self.__save_csv()
        if self.scraped_products:
            self.__save_csv()
        print('Scraping finished')

    def __get_categories(self) -> Generator:
        url_categories = URL.CATEGORIES
        categories = self.requester.get_response(url_categories)
        for categorie in categories:
            print(f'Scraping category {categorie[ApiKeys.name]}')
            if categorie[ApiKeys.hasChildren]:
                for i, children in enumerate(categorie[ApiKeys.children]):
                    children_slug = children[ApiKeys.url].replace(URL.BASE, '')
                    print(f'Children {children[ApiKeys.name]} {i + 1}/{len(categorie[ApiKeys.children])}')
                    yield children_slug

    def __scrap_products(self, slug: str, _from: int = 0) -> None:
        category_url = URL.get_products_url(slug, _from)
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
            payload.completeName = item[ApiKeys.complementName]
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
            self.scraped_products.append(payload.create_payload())
        print()
        self.__scrap_products(slug, _from + URL.steps + 1)

    def __get_product_categories(self, categories: list) -> list:
        format_categories = {cat for item in categories for cat in item.split('/') if cat}
        return list(format_categories)
    
    def __get_description(self, description: str) -> str:
        return html2text(description)

    def __get_images(self, images: list) -> list:
        return [item[ApiKeys.imageUrl] for item in images]
    
    def __get_payment_options(self, payment_options: list) -> list:
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

    def __save_csv(self) -> None:
        if not os.path.exists(CSVS_PATH):
            os.mkdir(CSVS_PATH)
        headers = list(self.scraped_products[0].keys())
        path_file = os.path.join(CSVS_PATH, 'test.csv')
        with open(path_file, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=headers, delimiter=';')
            writer.writeheader()
            writer.writerows(self.scraped_products)
        return