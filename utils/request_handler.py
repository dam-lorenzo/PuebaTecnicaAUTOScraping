import time
import requests

from bs4 import BeautifulSoup
from typing import Optional, Union

from config import config

class RequestHandler():

    def __init__(self) -> None:
        self.__session: requests.session = requests.session()

    @property
    def headers(self) -> dict:
        return self.__session.headers
    
    @property
    def proxy(self) -> dict:
        return self.__session.proxy

    def update_headers(self, headers: dict, overwrite: Optional[bool] = False) -> None:
        if overwrite:
            self.__session.headers = headers
        else:
            self.__session.headers.update(headers)

    def use_proxy(self) -> None:
        proxy_config = config()['proxy']
        proxy = {
            'http': f"http://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}",
            'https': f"http://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}"
        }
        self.__session.proxy = proxy

    def get_response(
            self,
            url: str,
            retries: Optional[int] = 5,
            timeout: Optional[int] = 15,
            resType: Optional[str] = 'json'
        ) -> Union[str, dict]:

        resType = resType.lower()
        if resType not in ['json', 'text']:
            raise ValueError(f'resType must be \'json\' or \'text\'\nActual value {resType}')
        
        for _ in range(retries):
            try:
                res = self.__session.get(url=url)
                if res.ok:
                    break
                time.sleep(timeout)
            except requests.exceptions.RequestException as exc:
                print(f'Error getting response {exec}')
                time.sleep(timeout)
                
        method = getattr(res, resType)
        if callable(method):
            return method()
        else:
            return method
        
    def get_soup(self, url: str, **kwargs) -> BeautifulSoup:
        kwargs.pop('resType', None)
        html = self.get_response(url=url, resType='text', **kwargs)
        return BeautifulSoup(html, 'lxml')