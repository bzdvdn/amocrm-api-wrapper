from requests import Session, ConnectionError, ConnectTimeout
from typing import Optional, Union
from urllib.parse import urlencode


class AmoException(Exception):
    def __init__(self, error_data: dict, *args):
        self.error_data = error_data
        super().__init__(args)

    def __str__(self):
        return ''.join(f'{k}: {v}' for k, v in self.error_data.items())


class Amo(object):
    def __init__(self, login: str, token: str, crm_url: str) -> None:
        """
        :param login: str (Login from amocrm)
        :param token: str (Api key from amocrm)
        :param crm_url: str (url from your amocrm)
        """
        self.login = login
        self.token = token
        self.crm_url = crm_url if crm_url.endswith('/') else crm_url[:-1]
        self.session = self._init_session()

    def _init_session(self, headers: Optional[dict] = None) -> Session:
        """
        :param headers: dict (amo headers params)
        :return: None
        """
        url = f"{self.crm_url}private/api/auth.php?type=json"
        params = {"USER_LOGIN": self.login, "USER_HASH": self.token}
        session = Session()
        if isinstance(headers, dict):
            session.headers.update(**headers)
        auth_response = session.post(url, json=params).json()
        if auth_response["response"]["auth"]:
            return session
        raise AmoException(auth_response)

    def update_session_params(self, params: dict) -> None:
        """
        :param params: dict (amo headers params)
        :return: None
        """
        self.session = self._init_session(params)

    def _send_api_request(self, method: str, url: str, data: Optional[dict] = None) -> dict:
        response = self.session.__getattribute__(method)(url, json=data).json()
        if 'error' in response:
            raise AmoException(response)
        return response

    def get_account_info(self, with_custom_fields: bool = False, with_users: bool = False,
                         with_pipelines: bool = True, with_groups: bool = False, with_note_types: bool = False,
                         with_task_types: bool = False) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/account
        :param with_custom_fields: bool
        :param with_users: bool
        :param with_pipelines: bool
        :param with_groups: bool
        :param with_note_types: bool
        :param with_task_types: bool
        :return: dict
        """
        with_params = [param for param, value in locals().items() if value]
        url = f'{self.crm_url}api/v2/account'
        url += '?with=' + ''.joins(p for p in with_params)
        return self._send_api_request('get', url)

    def create_or_update_leads(self, add: Optional[list] = None, update: Optional[list] = None) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/leads
        :param add: list (list of leads)
        :param update: list (list of leads)
        :return: dict
        """
        url = f'{self.crm_url}api/v2/leads'
        params = {}
        if add is not None:
            params['add'] = add
        if update is not None:
            params['update'] = update
        return self._send_api_request('post', url, params)

    def get_leads(self, limit_rows: int = 500, limit_offset: int = 0, id: Union[list, int, None] = None,
                  query: Optional[str] = None, status: Union[int, list, None] = None,
                  with_params: Optional[list] = None) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/leads
        :param limit_rows: int (limit of rows, default=500)
        :param limit_offset: int (offset, default=0)
        :param id: list or int (lead ids)
        :param query: str (query)
        :param status: list or int (id lead statuses)
        :param with_params: list (is_price_modified_by_robot, loss_reason_name, only_deleted)
        :return: dict
        """
        url = f'{self.crm_url}api/v2/leads'
        params = {'limit_rows': limit_rows, 'limit_offset': limit_offset}
        if id is not None:
            params['id'] = ','.join(i for i in id) if isinstance(id, list) else id
        if query is not None:
            params['query'] = query
        if status is not None:
            params['status'] = ','.join(i for i in status) if isinstance(status, list) else status
        if with_params:
            params['with'] = ','.join(param for param in with_params)
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

