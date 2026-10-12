import requests
from config.settings import BASE_URL, TIMEOUT

class RequestClient:
    """封装 request，以后不用每次写完整 URL 和 timeout"""

    def get(self, path, **kwargs):
        return requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT, **kwargs)

    def post(self, path, **kwargs):
        return requests.post(f"{BASE_URL}{path}", timeout=TIMEOUT, **kwargs)

    def delete(self, path, **kwargs):
        return requests.delete(f"{BASE_URL}{path}", timeout=TIMEOUT, **kwargs)

client = RequestClient()
