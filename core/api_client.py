# core/api_client.py
import base64
import json
from typing import Optional, Dict
from playwright.async_api import APIRequestContext


class APIClient:

    def __init__(
        self,
        request: APIRequestContext,
        base_url: str,
        timeout: int = 30000,
        auth_type: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None
    ):
        self.request = request
        self.base_url = base_url
        self.timeout = timeout

        self.auth_type = auth_type
        self.username = username
        self.password = password
        self.token = token

    # ========================
    # Internal Helpers
    # ========================
    def set_token(self, token: str):
        self.token = token
        self.auth_type = "bearer"
    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def _build_headers(
        self,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:

        default_headers = {
            "Content-Type": "application/json"
        }

        # Bearer Token
        if self.auth_type == "bearer" and self.token:
            default_headers["Authorization"] = f"Bearer {self.token}"

        # Basic Auth
        elif self.auth_type == "basic" and self.username and self.password:
            credentials = f"{self.username}:{self.password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            default_headers["Authorization"] = f"Basic {encoded}"

        if headers:
            default_headers.update(headers)

        return default_headers

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ):
        url = self._build_url(endpoint)

        json_payload = kwargs.pop("json", None)

        if json_payload is not None:
            kwargs["data"] = json.dumps(json_payload)

        response = self.request.fetch(
            url,
            method=method,
            headers=self._build_headers(kwargs.pop("headers", None)),
            timeout=self.timeout,
            **kwargs
        )

        return response

    # ========================
    # Public HTTP Methods
    # ========================

    def get(self, endpoint: str, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs):
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)