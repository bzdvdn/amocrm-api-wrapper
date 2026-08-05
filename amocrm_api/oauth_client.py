import asyncio
from collections.abc import Callable
from threading import Lock

import httpx
from httpx import AsyncClient, Client

from .base import BaseClient, mask_token
from .errors import AmoException


class AmoOAuthClient(BaseClient):
    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        crm_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        token_store: Callable[[str, str], None] | None = None,
    ):
        self._access_token = access_token
        self._refresh_token = refresh_token
        self.crm_url = crm_url if not crm_url.endswith('/') else crm_url[:-1]
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_store = token_store
        self._token_lock = Lock()
        self._async_token_lock = asyncio.Lock()
        self._session = self._init_session()
        self._async_session = AsyncClient(
            headers=self._auth_headers(), timeout=self.timeout
        )

    def _auth_headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self.access_token}',
            'User-Agent': 'amocrm-api-client/1.0',
        }

    def _init_session(self, params: dict | None = None) -> Client:
        session = Client(timeout=self.timeout)
        session.headers.update(self._auth_headers())
        if params:
            session.headers.update(params)
        return session

    async def _init_async_session(
        self, params: dict | None = None
    ) -> AsyncClient:
        session = AsyncClient(timeout=self.timeout)
        session.headers.update(self._auth_headers())
        if params:
            session.headers.update(params)
        return session

    def _send_api_request(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        _retry_counter: int = 0,
        *,
        update_tokens: bool = False,
    ) -> dict:
        try:
            return super()._send_api_request(method, url, data, _retry_counter)
        except AmoException as e:
            if getattr(e, "code", None) == 401 and not update_tokens:
                self.update_tokens()
                return self._send_api_request(
                    method, url, data, _retry_counter, update_tokens=True
                )
            raise

    async def _send_api_request_async(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        _retry_counter: int = 0,
        *,
        update_tokens: bool = False,
    ) -> dict:
        try:
            return await super()._send_api_request_async(
                method, url, data, _retry_counter
            )
        except AmoException as e:
            if getattr(e, "code", None) == 401 and not update_tokens:
                await self.update_tokens_async()
                return await self._send_api_request_async(
                    method, url, data, _retry_counter, update_tokens=True
                )
            raise

    def update_session_auth_headers(self) -> None:
        self.update_session_params({'Authorization': f'Bearer {self.access_token}'})

    async def update_session_auth_headers_async(self) -> None:
        await self.update_session_params_async(
            {'Authorization': f'Bearer {self.access_token}'}
        )

    def _refresh_tokens(self) -> tuple[str, dict]:
        url = f'{self.crm_url}/oauth2/access_token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'redirect_uri': self.redirect_uri,
        }
        return url, params

    def update_tokens(self) -> None:
        with self._token_lock:
            url, params = self._refresh_tokens()
            r = httpx.post(url, json=params, timeout=self.timeout)
            data = r.json()
            if r.status_code >= 400:
                raise AmoException(data, code=r.status_code)
            self._update_token_params(data['access_token'], data['refresh_token'])
            self.update_session_auth_headers()
            if self.token_store is not None:
                self.token_store(self.access_token, self.refresh_token)

    async def update_tokens_async(self) -> None:
        async with self._async_token_lock:
            url, params = self._refresh_tokens()
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.post(url, json=params)
            data = r.json()
            if r.status_code >= 400:
                raise AmoException(data, code=r.status_code)
            self._update_token_params(data['access_token'], data['refresh_token'])
            await self.update_session_auth_headers_async()
            if self.token_store is not None:
                self.token_store(self.access_token, self.refresh_token)

    def _update_token_params(self, access_token: str, refresh_token: str) -> None:
        self._access_token = access_token
        self._refresh_token = refresh_token

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @property
    def tokens(self) -> dict:
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
        }

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} crm_url={self.crm_url!r} "
            f"access_token={mask_token(self.access_token)!r}>"
        )
