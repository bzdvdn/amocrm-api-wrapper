from json import JSONDecodeError

import httpx
from httpx import AsyncClient, Client

from .base import BaseClient, mask_token
from .errors import AmoException


class AmoLegacyClient(BaseClient):
    def __init__(self, login: str, token: str, crm_url: str) -> None:
        """Init

        Args:
            login (str): login
            token (str): seckter token
            crm_url (str): your crm url like https://example.amocrm.ru
        """
        self.login = login
        self.token = token
        self.crm_url = crm_url if not crm_url.endswith('/') else crm_url[:-1]
        self._session = self._init_session()

    def _init_session(self, headers: dict | None = None) -> Client:
        """Init session

        Args:
            headers (Optional[dict], optional): headers params. Defaults to None.

        Raises:
            AmoException: if invalid auth data

        Returns:
            Client: session
        """
        url = f"{self.crm_url}/private/api/auth.php?type=json"
        params = {"USER_LOGIN": self.login, "USER_HASH": self.token}
        session = Client(timeout=self.timeout)
        if isinstance(headers, dict):
            session.headers.update(**headers)
        auth_response = session.post(url, json=params).json()
        if auth_response.get("response", {}).get("auth", {}):
            return session
        raise AmoException(auth_response)

    async def _init_async_session(
        self, headers: dict | None = None
    ) -> AsyncClient:
        """Init async session

        Args:
            headers (Optional[dict], optional): headers params. Defaults to None.

        Raises:
            AmoException: if invalid auth data

        Returns:
            AsyncClient: session
        """
        url = f"{self.crm_url}/private/api/auth.php?type=json"
        params = {"USER_LOGIN": self.login, "USER_HASH": self.token}
        session = AsyncClient(timeout=self.timeout)
        if isinstance(headers, dict):
            session.headers.update(**headers)
        auth_response = await session.post(url, json=params)
        data = auth_response.json()
        if data.get("response", {}).get("auth", {}):
            return session
        raise AmoException(data)

    def _send_api_request(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        _retry_counter: int = 0,
    ) -> dict:
        try:
            response = self._session.__getattribute__(method)(
                url, json=data, timeout=self.timeout
            )
            if response.status_code == 204:
                return {}
            json_data = response.json()
            if 'error' in json_data:
                raise AmoException(json_data)
            return json_data
        except (httpx.ConnectTimeout, httpx.ConnectError, JSONDecodeError) as e:
            raise AmoException({'error': str(e)})

    async def _send_api_request_async(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        _retry_counter: int = 0,
    ) -> dict:
        if not hasattr(self, "_async_session"):
            self._async_session = await self._init_async_session()
        try:
            response = await self._async_session.__getattribute__(method)(
                url, json=data, timeout=self.timeout
            )
            if response.status_code == 204:
                return {}
            json_data = response.json()
            if 'error' in json_data:
                raise AmoException(json_data)
            return json_data
        except (httpx.ConnectTimeout, httpx.ConnectError, JSONDecodeError) as e:
            raise AmoException({'error': str(e)})

    async def update_session_params_async(self, params: dict) -> None:
        """update async session

        Args:
            params (dict): like {'IF-MODIFIED-SINCE': <datetime>}
        """
        self._async_session = await self._init_async_session(params)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} login={self.login!r} "
            f"token={mask_token(self.token)!r}>"
        )
