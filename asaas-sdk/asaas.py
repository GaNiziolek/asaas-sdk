# https://asaasv3.docs.apiary.io

from requests import Session
from requests.exceptions import HTTPError
from urllib.parse import urljoin
from typing import Optional

from customers import Customers

class Asaas():
    def __init__(self, access_token, production = False):

        self.access_token = access_token

        if production:
            self.url = 'https://www.asaas.com'
        else:
            self.url = 'https://sandbox.asaas.com'

        self.session = Session()

        self.default_headers = {
            'access_token': access_token
        }

        self.customers = Customers(self)

    def get(self, endpoint: str, params: Optional[dict] = None):

        response = self.session.get(
            url     = urljoin(self.url, endpoint),
            headers = self.default_headers,
            params  = params
        )

        response.raise_for_status()

        return response.json()
    
    def post(self, endpoint: str, json: Optional[dict] = None):

        response = self.session.post(
            url     = urljoin(self.url, endpoint),
            headers = self.default_headers,
            json    = json
        )

        try:
            response.raise_for_status()
        except HTTPError as e:
            return False, response.json()

        return True,  response.json()


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    load_dotenv()

    acess_token = os.getenv('acess_token')

    asaas = Asaas(acess_token, production = False)

    asaas.customers.new('name', '12')