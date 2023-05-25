import time
import requests

from typing import Optional, Union

class RequestHandler():

    def __init__(self) -> None:
        self.__session: requests.session = requests.session()

    @property
    def headers(self) -> dict:
        return self.__session.headers

    def update_headers(self, headers: dict, overwrite: Optional[bool] = False) -> None:
        if overwrite:
            self.__session.headers = headers
        else:
            self.__session.headers.update(headers)

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