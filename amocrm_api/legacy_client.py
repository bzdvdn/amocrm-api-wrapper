from json import JSONDecodeError
from requests import Session, ConnectionError, ConnectTimeout
from typing import Optional, Union
from urllib.parse import urlencode

from .errors import AmoException
from .base import BaseClient


class AmocrmLegacyClient(BaseClient):
    def __init__(self, login: str, token: str, crm_url: str) -> None:
        """
        :param login: str (Login from amocrm)
        :param token: str (Api key from amocrm)
        :param crm_url: str (url from your amocrm)
        """
        self.login = login
        self.token = token
        self.crm_url = crm_url if not crm_url.endswith('/') else crm_url[:-1]
        self.session = self._init_session()

    def _init_session(self, headers: Optional[dict] = None) -> Session:
        """
        :param headers: dict (amo headers params)
        :return: None
        """
        url = f"{self.crm_url}/private/api/auth.php?type=json"
        params = {"USER_LOGIN": self.login, "USER_HASH": self.token}
        session = Session()
        if isinstance(headers, dict):
            session.headers.update(**headers)
        auth_response = session.post(url, json=params).json()
        if auth_response["response"]["auth"]:
            return session
        raise AmoException(auth_response)

    def _send_api_request(
        self, method: str, url: str, data: Optional[dict] = None
    ) -> dict:
        try:
            response = self.session.__getattribute__(method)(url, json=data)
            if response.status_code == 204:
                return {}
            json_data = response.json()
            if 'error' in json_data:
                raise AmoException(json_data)
            return json_data
        except (ConnectTimeout, ConnectionError, JSONDecodeError) as e:
            raise AmoException({'error': str(e)})
