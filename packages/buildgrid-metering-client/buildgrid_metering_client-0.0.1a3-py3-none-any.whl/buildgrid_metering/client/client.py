# Copyright (C) 2023 Bloomberg LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from typing import Awaitable, Callable, Dict, Optional, TypeVar
from urllib.parse import quote_plus

import aiohttp
import tenacity

from buildgrid_metering.client.auth import AuthTokenLoader
from buildgrid_metering.client.exceptions import (
    MeteringServiceClientError,
    MeteringServiceHTTPError,
)
from buildgrid_metering.client.retry import RetryConfig
from buildgrid_metering.models.api import GetThrottlingResponse, PutUsageRequest
from buildgrid_metering.models.dataclasses import Identity, Usage

T = TypeVar("T")

USAGE_API_URL_PREFIX = "/v1/usage/"
THROTTLING_API_URL_PREFIX = "/v1/throttling/"
IDENTITY_EMPTY_INSTANCE_URL_TEMPLATE = "{workflow}/{actor}/{subject}"
IDENTITY_URL_TEMPLATE = "{instance}/" + IDENTITY_EMPTY_INSTANCE_URL_TEMPLATE


class MeteringServiceClient:
    """Python client of BuildGrid Metering Service"""

    _base_url: str
    _token_loader: AuthTokenLoader
    _request_timeout: aiohttp.ClientTimeout
    _headers: Dict[str, str]
    _retry_config: RetryConfig

    def __init__(
        self,
        base_url: str,
        token_loader: AuthTokenLoader,
        request_timeout: float = 5.0,
        headers: Optional[Dict[str, str]] = None,
        retry_config: RetryConfig = RetryConfig(),
    ) -> None:
        """Initialize the client

        Args:
            base_url (str): base URL of the service,
                e.g. http://localhost:8000 or https://somedomain.com
            token_loader (AuthTokenLoader): token loader
            request_timeout (float, optional): HTTP Request timeout . Defaults to 5.0.
            headers (Optional[dict[str, str]], optional): default headers.
                Defaults to None.
            retry_configs: See `buildgrid_metering.client.retry.RetryConfig`
                for details and default values.
        """
        self._base_url = base_url
        self._token_loader = token_loader
        self._request_timeout = aiohttp.ClientTimeout(total=request_timeout)
        self._headers = headers or {}
        self._retry_config = retry_config

    async def put_usage(
        self, identity: Identity, operation_name: str, usage: Usage
    ) -> None:
        url = self._create_url(USAGE_API_URL_PREFIX, identity)
        request = PutUsageRequest(operation_name=operation_name, usage=usage)

        async def request_func(session: aiohttp.ClientSession) -> None:
            async with session.put(
                url,
                json=request.dict(exclude_defaults=True),
            ) as response:
                if response.status != 204:
                    raise MeteringServiceHTTPError(
                        response.status, await response.text()
                    )

        return await self._make_request(request_func)

    async def get_throttling(self, identity: Identity) -> GetThrottlingResponse:
        url = self._create_url(
            THROTTLING_API_URL_PREFIX,
            identity,
        )

        async def request_func(session: aiohttp.ClientSession) -> GetThrottlingResponse:
            async with session.get(url) as response:
                if response.status != 200:
                    raise MeteringServiceHTTPError(
                        response.status, await response.text()
                    )
                return GetThrottlingResponse(**(await response.json()))

        return await self._make_request(request_func)

    async def _make_request(
        self,
        request_func: Callable[[aiohttp.ClientSession], Awaitable[T]],
    ) -> T:
        headers = dict(self._headers)
        auth_token = await self._token_loader.get_token()
        if auth_token is not None:
            headers["Authorization"] = "Bearer " + auth_token

        def should_retry_on_http_error(exc: BaseException) -> bool:
            if not isinstance(exc, MeteringServiceHTTPError):
                return False
            return exc.http_status in self._retry_config.http_statuses

        @tenacity.retry(
            stop=tenacity.stop_after_attempt(self._retry_config.max_attempts),
            retry=tenacity.retry_if_exception(should_retry_on_http_error)
            | tenacity.retry_if_exception_type(self._retry_config.exception_types)
            | tenacity.retry_if_exception_cause_type(
                self._retry_config.cause_exception_types
            ),
            wait=tenacity.wait_exponential(
                multiplier=self._retry_config.multiplier,
                exp_base=self._retry_config.exp_base,
                max=self._retry_config.max_wait,
            ),
            reraise=True,
        )
        async def _request() -> T:
            try:
                async with aiohttp.ClientSession(
                    self._base_url, headers=headers, timeout=self._request_timeout
                ) as session:
                    return await request_func(session)
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                raise MeteringServiceClientError(repr(e)) from e

        return await _request()

    def _create_url(self, url_prefix: str, identity: Identity) -> str:
        if identity.instance == "":
            return url_prefix + IDENTITY_EMPTY_INSTANCE_URL_TEMPLATE.format(
                workflow=quote_plus(identity.workflow),
                actor=quote_plus(identity.actor),
                subject=quote_plus(identity.subject),
            )
        return url_prefix + IDENTITY_URL_TEMPLATE.format(
            instance=quote_plus(identity.instance),
            workflow=quote_plus(identity.workflow),
            actor=quote_plus(identity.actor),
            subject=quote_plus(identity.subject),
        )
