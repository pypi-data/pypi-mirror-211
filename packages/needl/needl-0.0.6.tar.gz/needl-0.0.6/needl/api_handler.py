import requests
from typing import Any


def call_api(url: str, json: dict = None) -> requests.Response:
    if json is None:
        return requests.get(url=url)
    else:
        return requests.post(url=url, json=json)


def check_response(resp: requests.Response, return_type: str = "json") -> Any:
    if resp.status_code == 401:
        data = resp.json()
        if data["detail"] == "An API key is required to access the requested data":
            raise Exception("no API key set in the configuration")

    if resp.status_code in {102, 400, 422}:
        data = resp.json()
        raise Exception(data["detail"])

    if resp.status_code == 404:
        raise Exception("not found")

    if return_type == "json":
        data = resp.json()
    elif return_type == "text":
        data = resp.text
    else:
        raise Exception(f"invalid value for return_type ({return_type!r}) in check_response")
    return data
