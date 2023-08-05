import os
import json
import pytz
import requests
import hashlib
from datetime import datetime


class CJClient:
    """
    A client to interact with Clear Junction API.
    """

    def __init__(self, api_key=None, password=None, wallet_uuid=None):
        """
        Initializes the client with credentials.

        Credentials are read from environment variables if not provided.
        """
        self.api_key = api_key or os.getenv("CLEAR_JUNCTION_API_KEY")
        self.password = password or os.getenv("CLEAR_JUNCTION_PASSWORD")
        self.wallet_uuid = wallet_uuid or os.getenv(
            "CLEAR_JUNCTION_WALLET_UUID")
        self.url_base = 'https://client.clearjunction.com/'

    def transaction_report(self, from_date, to_date):
        """
        Retrieves a transaction report for the specified date range.
        """
        end_point = 'v7/gate/reports/transactionReport'
        body = {
            "walletUuid": self.wallet_uuid,
            "timestampFrom": from_date.isoformat(),
            "timestampTo": to_date.isoformat()
        }
        return self._make_request(end_point, body, 'POST')

    def order_reference(self, order_id, transaction_type="invoice"):
        """
        Retrieves the status of an order by its reference.
        """
        end_point = f'v7/gate/status/{transaction_type}/orderReference/{order_id}'
        return self._make_request(end_point, None, 'GET')

    def _make_request(self, end_point, body, method):
        """
        Makes a request to the specified endpoint.

        Raises an exception if the request fails.
        """
        iso_date = (datetime.now(pytz.utc).replace(microsecond=0)).isoformat()
        body = self._create_request_body(body) if body else None

        signature = self._calculate_signature(iso_date, body)

        url = self.url_base + end_point

        headers = {
            'Content-Type': 'application/json',
            'Date': iso_date,
            'X-API-KEY': self.api_key,
            'Authorization': signature
        }

        if method == 'POST':
            response = requests.post(url, headers=headers, data=body)
        elif method == 'GET':
            response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"Request failed with status {response.status_code}.")

        return response.json()

    def _create_request_body(self, body):
        """
        Creates the request body from a dictionary.
        """
        return json.dumps(body) if body else ''

    def _calculate_signature(self, iso_date, body):
        """
        Calculates the signature for a request.
        """
        hashed_pass = hashlib.sha512(
            self.password.encode("utf-8")).hexdigest().upper()
        auth = self.api_key.upper() + iso_date + hashed_pass + \
            (body.upper() if body else '')
        return hashlib.sha512(auth.encode()).hexdigest()
