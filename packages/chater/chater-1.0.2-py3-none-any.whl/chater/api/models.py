import requests

import chater


class Models:
    def list_models():
        """Lists the currently available models"""
        api_url = f'{chater.api_base}/models'
        headers = {'Authorization':  f'Bearer {chater.api_key}'}
        response = requests.get(api_url, headers=headers).json()
        return response
