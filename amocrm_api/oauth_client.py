from json import JSONDecodeError
from requests import Session, ConnectionError, ConnectTimeout, post
from typing import Optional, Union
from urllib.parse import urlencode

from .errors import AmoException
from .base import BaseClient


class AmoOAuthClient(BaseClient):
    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        crm_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
    ):
        self._access_token = access_token
        self._refresh_token = refresh_token
        self.crm_url = crm_url if not crm_url.endswith('/') else crm_url[:-1]
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._session = self._init_session()

    def _init_session(self, params: Optional[dict] = None) -> Session:
        session = Session()
        session.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'User-Agent': 'amocrm-api-client/1.0',
        }
        if params:
            session.headers.update(params)
        return session

    def _send_api_request(
        self,
        method: str,
        url: str,
        data: Optional[dict] = None,
        update_tokens: bool = False,
    ) -> dict:
        try:
            response = super()._send_api_request(method, url, data)
            return response
        except AmoException as e:
            if 'Jsonstatus: 401' in str(e) and not update_tokens:
                self.update_tokens()
                return self._send_api_request(method, url, data, True)
            raise

    def update_session_auth_headers(self):
        self.update_session_params({'Authorization': f'Bearer {self.access_token}'})

    def update_tokens(self):
        url = f'{self.crm_url}/oauth2/access_token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'redirect_uri': self.redirect_uri,
        }
        r = post(url, json=params)
        data = r.json()
        if r.status_code > 204:
            raise AmoException(data)
        self._update_token_params(data['access_token'], data['refresh_token'])
        self.update_session_auth_headers()

    def _update_token_params(self, access_token: str, refresh_token: str):
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
