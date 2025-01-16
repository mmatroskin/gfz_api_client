from __future__ import annotations
from abc import ABC
import logging
import time
from uuid import uuid4

import asyncio
from aiohttp import ClientConnectionError, ClientSession, ClientTimeout, hdrs, ServerTimeoutError
import requests
import ujson

from gfz_client import exceptions, settings

logger = logging.getLogger("gfz_client")


class CommonHTTPBackendProperties(ABC):
    """Common Backend properties and methods"""
    _request_timeout_sec: int = settings.REQUEST_TIMEOUT_SEC


class HTTPBackend(CommonHTTPBackendProperties, ABC):
    """Backend Base Class"""

    def _execute_request(self, method: str, url: str, **kwargs) -> tuple[dict | None, int]:
        """Execute request
        Args:
            method: method
            url: url
            params: Query params
        Raises:
            ExternalServiceNetworkError
        Returns:
            Response body and response status
        """
        headers = kwargs.pop("headers", None) or {}
        request_id = uuid4().hex

        logger.debug(
            "Remote service request: request_id=%s method=%s url=%s params=%s body=%s",
            request_id, method, url, kwargs.get("params"),
        )

        try:
            with requests.Session() as session:
                start_time = time.time()
                response = session.request(
                    method=method,
                    headers=headers,
                    url=url,
                    timeout=self._request_timeout_sec,
                    **kwargs
                )
                end_time = time.time()
                duration = round((end_time - start_time) * 1000)
        except (ServerTimeoutError, ClientConnectionError, asyncio.TimeoutError) as exc:
            logger.error("Remote service request failed: request_id=%s %r",
                          request_id, exc, exc_info=True)
            raise exceptions.ExternalServiceNetworkError() from exc
        logger.debug(
            "Remote service response: request_id=%s duration=%d status=%s",
            request_id, duration, response.status_code,
        )
        try:
            data = response.json()
        except ValueError:
            data = None
        return data, response.status_code


class HTTPAsyncBackend(CommonHTTPBackendProperties, ABC):
    """Async Backend Base Class"""

    async def _make_request(self, method: str, url: str, **kwargs) -> tuple[dict | None, int]:
        """Execute request
        Args:
            method: method
            url: url
            params: Query params
        Raises:
            ExternalServiceNetworkError
        Returns:
            Response body and response status
        """
        headers = kwargs.pop("headers", None) or {}
        request_id = uuid4().hex

        logger.debug(
            "Remote service request: request_id=%s method=%s url=%s params=%s",
            request_id, method, url, kwargs.get("params"),
        )

        session = ClientSession(timeout=ClientTimeout(total=self._request_timeout_sec), json_serialize=ujson.dumps)

        try:
            start_time = time.time()
            async with session, session.request(
                method=method, url=url, headers=headers, verify_ssl=False, **kwargs,
            ) as response:
                end_time = time.time()
                duration = round((end_time - start_time) * 1000)
                response_body = await response.read()
        except (ServerTimeoutError, ClientConnectionError, asyncio.TimeoutError) as exc:
            logger.error("Remote service request failed: request_id=%s %r",
                          request_id, exc, exc_info=True)
            raise exceptions.ExternalServiceNetworkError() from exc
        logger.debug(
            "Remote service response: request_id=%s duration=%d status=%s",
            request_id, duration, response.status,
        )
        return ujson.loads(response_body) if response_body else None, response.status
