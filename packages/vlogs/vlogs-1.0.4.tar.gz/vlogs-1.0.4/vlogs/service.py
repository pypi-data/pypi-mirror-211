import requests

from vlogs.model import CollectorResponse
from vlogs.config import BASE_URL


class VLogsService:
    def __init__(self, base_url=BASE_URL):
        self.url = f"{base_url}/api/v1/collector"

    def post(self, body, headers=None, timeout=None):
        response = requests.post(
            data=body,
            url=self.url,
            headers=headers,
            timeout=timeout * 1000 if timeout else None,
        )

        if response.status_code in [200, 201, 202]:
            return CollectorResponse(**response.json())
        else:
            raise Exception(
                f"Failed to post data to vlogs server with status code: {response.status_code} and message: {response.text}"
            )
