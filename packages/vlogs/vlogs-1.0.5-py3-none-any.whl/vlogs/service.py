import json

from vlogs.config import BASE_URL
from vlogs.model import CollectorResponse
import httpx


class VLogsService:
    def __init__(self, base_url=BASE_URL):
        self.url = f"{base_url}/api/v1/collector"

    def post(self, body, headers=None, timeout=None):
        response = httpx.post(
            url=self.url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                **headers,
            },
            timeout=timeout * 1000 if timeout else None,
            content=json.dumps(body),
        )

        if response.status_code in [200, 201, 202]:
            return CollectorResponse(**response.json())
        else:
            raise Exception(
                f"Failed to post data to vlogs server with status code: {response.status_code} and message: {response.text}"
            )

    async def post_async(self, body, headers=None, timeout=None):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=self.url,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    **headers,
                },
                timeout=timeout * 1000 if timeout else None,
                content=json.dumps(body),
            )

            if response.status_code in [200, 201, 202]:
                return CollectorResponse(**response.json())
            else:
                raise Exception(
                    f"Failed to post data to vlogs server with status code: {response.status_code} and message: {response.text}"
                )
