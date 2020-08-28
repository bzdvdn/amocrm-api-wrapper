from json import JSONDecodeError
from requests import Session, ConnectionError, ConnectTimeout
from typing import Optional, Union
from urllib.parse import urlencode

from .errors import AmoException
from .base import BaseClient


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

    def _init_session(self, headers: Optional[dict] = None) -> Session:
        """Init session

        Args:
            headers (Optional[dict], optional): headers params. Defaults to None.

        Raises:
            AmoException: if invalid auth data

        Returns:
            Session: session
        """
        url = f"{self.crm_url}/private/api/auth.php?type=json"
        params = {"USER_LOGIN": self.login, "USER_HASH": self.token}
        session = Session()
        if isinstance(headers, dict):
            session.headers.update(**headers)
        auth_response = session.post(url, json=params).json()
        if  auth_response.get("response", {}).get("auth", {}):
            return session
        raise AmoException(auth_response)

    def _send_api_request(
        self, method: str, url: str, data: Optional[dict] = None
    ) -> dict:
        try:
            response = self._session.__getattribute__(method)(url, json=data)
            if response.status_code == 204:
                return {}
            json_data = response.json()
            if 'error' in json_data:
                raise AmoException(json_data)
            return json_data
        except (ConnectTimeout, ConnectionError, JSONDecodeError) as e:
            raise AmoException({'error': str(e)})
