from typing import Dict, Optional
import requests


class HttpClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})

    def get(self, url: str, headers: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self.session.get(url, headers=headers, **kwargs)

    def post(self, url: str, headers: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self.session.post(url, headers=headers, **kwargs)
