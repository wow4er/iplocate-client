import httpx
from typing import Optional
from .exceptions import IPLocateError, RateLimitError, InvalidIPError

BASE_URL = "https://iplocate.net/api"


class IPLocate:
    def __init__(self, api_key: str = None, timeout: int = 5):
        self.api_key = api_key
        self.timeout = timeout

    def lookup(self, ip: str = None, fields: list[str] = None) -> dict:
        params = {}
        if ip:
            params["ip"] = ip
        if fields:
            params["fields"] = ",".join(fields)

        with httpx.Client(timeout=self.timeout) as client:
            resp = client.get(f"{BASE_URL}/ip", params=params)

        return self._handle(resp)

    def bulk(self, ips: list[str], fields: list[str] = None) -> list[dict]:
        if not ips:
            raise IPLocateError("ip list cannot be empty")
        if len(ips) > 20:
            raise IPLocateError("max 20 IPs per request")

        payload = {"ip_list": ips, "fields": fields or []}
        if self.api_key:
            payload["api_key"] = self.api_key

        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(f"{BASE_URL}/ip-bulk", json=payload)

        return self._handle(resp)["data"]

    def _handle(self, resp: httpx.Response) -> dict:
        if resp.status_code == 429:
            raise RateLimitError("rate limit exceeded")
        if resp.status_code == 400:
            raise InvalidIPError(resp.json().get("message", "invalid request"))
        resp.raise_for_status()
        
        return resp.json()


class AsyncIPLocate:
    def __init__(self, api_key: str = None, timeout: int = 10):
        self.api_key = api_key
        self.timeout = timeout

    async def lookup(self, ip: str = None, fields: list[str] = None) -> dict:
        params = {}
        if ip:
            params["ip"] = ip
        if fields:
            params["fields"] = ",".join(fields)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{BASE_URL}/ip", params=params)

        return self._handle(resp)

    async def bulk(self, ips: list[str], fields: list[str] = None) -> list[dict]:
        if not ips:
            raise IPLocateError("ip list cannot be empty")
        if len(ips) > 20:
            raise IPLocateError("max 20 IPs per request")

        payload = {"ip_list": ips, "fields": fields or []}
        if self.api_key:
            payload["api_key"] = self.api_key

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(f"{BASE_URL}/ip-bulk", json=payload)

        return self._handle(resp)["data"]

    def _handle(self, resp: httpx.Response) -> dict:
        if resp.status_code == 429:
            raise RateLimitError("rate limit exceeded")
        if resp.status_code == 400:
            raise InvalidIPError(resp.json().get("message", "invalid request"))
        resp.raise_for_status()
        return resp.json()