from datetime import datetime, timedelta

import requests

import chater
from .abstract.typings import SubscriptionResponse


class Billing:
    """
    Billing Dashboard

    Only support secret key.
    """

    @staticmethod
    def usage():
        api_url = f'{chater.api_base}/dashboard/billing/usage'

        headers = {
            'Content-Type':    'application/json',
            'Authorization':  f'Bearer {chater.api_key}'
        }

        params = {
            'start_date': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
            'end_date':   (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        }

        response = requests.get(api_url, headers=headers, params=params)

        if response.ok:
            return response.json()
        else:
            raise Exception(response.json()['error'])

    @staticmethod
    def subscription() -> SubscriptionResponse:
        api_url = f'{chater.api_base}/dashboard/billing/subscription'

        headers = {
            'Content-Type':    'application/json',
            'Authorization':  f'Bearer {chater.api_key}'
        }

        response = requests.get(api_url, headers=headers)

        if response.ok:
            return SubscriptionResponse(**response.json())
        else:
            raise Exception(response.json()['error'])
