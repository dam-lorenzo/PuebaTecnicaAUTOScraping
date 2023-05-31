import time
import requests

from bs4 import BeautifulSoup
from typing import Optional, Union

from config import config

class RequestHandler():

    """
    A class for handling HTTP requests and responses.

    Attributes:
    - __session: An instance of `requests.session` for making HTTP requests.

    Methods:
    - headers: Property method to retrieve the headers used in the HTTP requests.
    - proxy: Property method to retrieve the proxy configuration used for requests.
    - update_headers: Method to update the headers used in the HTTP requests.
    - use_proxy: Method to configure the HTTP requests to use a proxy.
    - get_response: Method to send an HTTP GET request and retrieve the response.
    - get_soup: Method to retrieve the BeautifulSoup object from an HTML response.
    """

    def __init__(self) -> None:
        self.__session: requests.session = requests.session()

    @property
    def headers(self) -> dict:
        """
        Retrieve the headers used in the HTTP requests.

        Returns:
        - A dictionary representing the headers used in the requests.
        """
        return self.__session.headers
    
    @property
    def proxy(self) -> dict:
        """
        Retrieve the proxy configuration used for requests.

        Returns:
        - A dictionary representing the proxy configuration used for requests.
        """
        return self.__session.proxy

    def update_headers(self, headers: dict, overwrite: Optional[bool] = False) -> None:
        """
        Update the headers used in the HTTP requests.

        Args:
        - headers: A dictionary containing the headers to be updated.
        - overwrite: An optional boolean indicating whether to overwrite the existing headers.
                     If False, the new headers will be merged with the existing ones. (default: False)
        """
        if overwrite:
            self.__session.headers = headers
        else:
            self.__session.headers.update(headers)

    def use_proxy(self) -> None:
        """
        Configure the HTTP requests to use a proxy.
        The proxy configuration is retrieved from the configuration file.
        """
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
        """
        Send an HTTP GET request and retrieve the response.

        Args:
        - url: The URL to send the request to.
        - retries: An optional integer indicating the number of retries in case of failure. (default: 5)
        - timeout: An optional integer indicating the timeout duration for each request in seconds. (default: 15)
        - resType: An optional string indicating the type of response expected. Valid values are 'json' or 'text'. (default: 'json')

        Returns:
        - The response as a string if `resType` is 'text', or a dictionary if `resType` is 'json'.

        Raises:
        - ValueError: If `resType` is not 'json' or 'text'.
        """

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
        """
        Retrieve the BeautifulSoup object from an HTML response.

        Args:
        - url: The URL to send the request to.
        - **kwargs: Additional keyword arguments to be passed to the `get_response` method.

        Returns:
        - A BeautifulSoup object representing the parsed HTML.

        Notes:
        - This method internally calls the `get_response` method with `resType='text'` to retrieve the HTML response.
        - Any additional keyword arguments provided will be forwarded to the `get_response` method.
        """
        kwargs.pop('resType', None)
        html = self.get_response(url=url, resType='text', **kwargs)
        return BeautifulSoup(html, 'lxml')