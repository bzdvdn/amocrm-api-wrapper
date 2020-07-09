from json import JSONDecodeError
from requests import Session, ConnectionError, ConnectTimeout
from typing import Optional, Union
from urllib.parse import urlencode

from .errors import AmoException


class BaseClient(object):
    def _init_session(self, headers: Optional[dict] = None) -> Session:
        raise NotImplementedError()

    def update_session_params(self, params: dict) -> None:
        """
        :param params: dict (amo headers params)
        :return: None
        """
        self.session = self._init_session(params)

    def _send_api_request(
        self, method: str, url: str, data: Optional[dict] = None
    ) -> dict:
        try:
            response = self.session.__getattribute__(method)(url, json=data)
            if response.status_code == 204:
                return {}
            data = response.json()
            json_data = data['response'] if 'response' in data else data
            if 'error' in json_data:
                raise AmoException(json_data)
            return json_data
        except (ConnectTimeout, ConnectionError, JSONDecodeError) as e:
            raise AmoException({'error': str(e)})

    def get_account_info(
        self,
        with_custom_fields: bool = False,
        with_users: bool = False,
        with_pipelines: bool = True,
        with_groups: bool = False,
        with_note_types: bool = False,
        with_task_types: bool = False,
    ) -> dict:
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
        params = {k.replace('with_', ''): v for k, v in locals().items() if k != 'self'}
        with_params = [param for param, value in params.items() if value]
        url = f'{self.crm_url}/api/v2/account'
        url += '?with=' + ','.join(p for p in with_params)
        return self._send_api_request('get', url)

    def _create_or_update(
        self, endpoint: str, add: Optional[list] = None, update: Optional[list] = None
    ) -> dict:
        """
        :param endpoint: str
        :param add: list or None
        :param update: list or None
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/{endpoint}'
        params = {}
        if add is not None:
            params['add'] = add
        if update is not None:
            params['update'] = update
        return self._send_api_request('post', url, params)

    def create_or_update_leads(
        self, add: Optional[list] = None, update: Optional[list] = None
    ) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/leads
        :param add: list (list of leads)
        :param update: list (list of leads)
        :return: dict
        """
        return self._create_or_update('leads', add, update)

    def get_leads(
        self,
        limit_rows: int = 500,
        limit_offset: int = 0,
        id: Union[list, int, None] = None,
        query: Optional[str] = None,
        status: Union[int, list, None] = None,
        responsible_user_id: Union[int, list, None] = None,
        with_params: Optional[list] = None,
    ) -> dict:  #
        # TODO: filter data
        """
        doc - https://www.amocrm.ru/developers/content/api/leads
        :param limit_rows: int (limit of rows, default=500)
        :param limit_offset: int (offset, default=0)
        :param id: list or int (lead ids)
        :param query: str (query)
        :param status: list or int (id lead statuses)
        :param responsible_user_id: list or int (id manager)
        :param with_params: list (is_price_modified_by_robot, loss_reason_name, only_deleted)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/leads'
        params = {'limit_rows': limit_rows, 'limit_offset': limit_offset}
        if id is not None:
            params['id'] = ','.join(i for i in id) if isinstance(id, list) else id
        if query is not None:
            params['query'] = query
        if status is not None:
            params['status'] = (
                ','.join(i for i in status) if isinstance(status, list) else status
            )
        if responsible_user_id is not None:
            params['responsible_user_id'] = (
                ','.join(i for i in responsible_user_id)
                if isinstance(responsible_user_id, list)
                else responsible_user_id
            )
        if with_params:
            params['with'] = ','.join(param for param in with_params)
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

    def create_or_create_contacts(
        self, add: Optional[list] = None, update: Optional[list] = None
    ) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/contacts
        :param add: list (list for create contacts)
        :param update: (list for update contacts)
        :return: dict
        """
        return self._create_or_update('contacts', add, update)

    def get_contacts(
        self,
        limit_rows: int = 500,
        limit_offset: int = 0,
        id: Union[int, list, None] = None,
        responsible_user_id: Union[list, int, None] = None,
        query: Optional[str] = None,
    ) -> dict:
        """
         doc - https://www.amocrm.ru/developers/content/api/contacts
        :param limit_rows: int (limit of rows, default=500)
        :param limit_offset: int (offset, default=0)
        :param id: list or int (contact ids)
        :param query: str (query)
        :param responsible_user_id: list or int (manager ids)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/contacts'
        params = {'limit_rows': limit_rows, 'limit_offset': limit_offset}
        if id is not None:
            params['id'] = ','.join(i for i in id) if isinstance(id, list) else id
        if query is not None:
            params['query'] = query
        if responsible_user_id is not None:
            params['responsible_user_id'] = (
                ','.join(i for i in responsible_user_id)
                if isinstance(responsible_user_id, list)
                else responsible_user_id
            )
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

    def create_or_update_companies(
        self, add: Optional[list] = None, update: Optional[list] = None
    ) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/companies
        :param add: list (list for create contacts)
        :param update: (list for update contacts)
        :return: dict
        """
        return self._create_or_update('companies', add, update)

    def get_companies(
        self,
        limit_rows: int = 500,
        limit_offset: int = 0,
        id: Union[int, list, None] = None,
        responsible_user_id: Union[list, int, None] = None,
        query: Optional[str] = None,
    ) -> dict:
        """
         doc - https://www.amocrm.ru/developers/content/api/companies
        :param limit_rows: int (limit of rows, default=500)
        :param limit_offset: int (offset, default=0)
        :param id: list or int (company ids)
        :param query: str (query)
        :param responsible_user_id: list or int (manager ids)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/companies'
        params = {'limit_rows': limit_rows, 'limit_offset': limit_offset}
        if id is not None:
            params['id'] = ','.join(i for i in id) if isinstance(id, list) else id
        if query is not None:
            params['query'] = query
        if responsible_user_id is not None:
            params['responsible_user_id'] = (
                ','.join(i for i in responsible_user_id)
                if isinstance(responsible_user_id, list)
                else responsible_user_id
            )
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

    def create_or_update_customers(
        self, add: Optional[list] = None, update: Optional[list] = None
    ) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/customers
        :param add: list (list for create customers)
        :param update: (list for update customers)
        :return: dict
        """
        return self._create_or_update('customers', add, update)

    def delete_customers(self, delete_ids: list) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/companies
        :param delete: list (list of customer ids)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/customers'
        params = {'delete': delete_ids}
        return self._send_api_request('post', url, data=params)

    def get_customers(
        self, limit_rows: int = 500, limit_offset: int = 0
    ) -> dict:  # TODO: filters
        """
        :param limit_rows: int
        :param limit_offset: int
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/customers'
        params = {'limit_rows': limit_rows, 'limit_offset': limit_offset}
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

    def create_transactions(self, add: list) -> dict:
        """
        :param add: list (list of transactions)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/transactions'
        params = {'add': add}
        return self._send_api_request('post', url, params)

    def delete_transactions(self, delete: list) -> dict:
        """
        :param delete: list (list of transactions)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/transactions'
        params = {'delete': delete}
        return self._send_api_request('post', url, params)

    def update_transaction_comments(self, update: list) -> dict:
        """
        :param update: list (list of transactions)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/transactions'
        params = {'update': update}
        return self._send_api_request('post', url, params)

    def get_transactions(
        self,
        limit_rows: int = 500,
        limit_offset: int = 0,
        id: Optional[int] = None,
        customer_id: Optional[int] = None,
    ) -> dict:
        """
        :param limit_rows: int
        :param limit_offset: int
        :param id: int (id of transaction)
        :param customer_id: int (id of customer)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/transactions'
        params = {'limit_rows': limit_rows, 'limit_offset': limit_offset}
        if id is not None:
            params['id'] = id
        if customer_id is not None:
            params['customer_id'] = customer_id
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

    def update_customer_periods(self, update: list) -> dict:
        """
        :param update: list (exclude del period)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/customers_periods'
        params = {'update': update}
        return self._send_api_request('post', url, params)

    def get_customer_periods(self) -> dict:
        """
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/customers_periods'
        return self._send_api_request('get', url)

    def create_or_create_tasks(
        self, add: Optional[list] = None, update: Optional[list] = None
    ) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/tasks
        :param add: list (list of tasks)
        :param update: list (list of tasks)
        :return: dict
        """
        return self._create_or_update('tasks', add, update)

    def get_tasks(
        self,
        limit_rows: int = 500,
        limit_offset: int = 0,
        id: Optional[int] = None,
        element_id: Optional[int] = None,
        responsible_user_id: Optional[int] = None,
        type: Optional[str] = None,
    ) -> dict:  # TODO: filters
        """
        doc - https://www.amocrm.ru/developers/content/api/tasks
        :param limit_rows: int
        :param limit_offset: int
        :param id: list or int
        :param element_id: int
        :param responsible_user_id: int
        :param type: str
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/tasks'
        params = {'limit_rows': limit_rows, 'limit_offset': limit_offset}
        if id is not None:
            params['id'] = id
        if element_id is not None:
            params['element_id'] = element_id
        if responsible_user_id is not None:
            params['responsible_user_id'] = responsible_user_id
        if type is not None:
            params['type'] = type
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

    def create_or_update_notes(
        self, add: Optional[list] = None, update: Optional[list] = None
    ) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/notes
        :param add: list (list of notes)
        :param update: list (list of notes)
        :return: dict
        """
        return self._create_or_update('notes', add, update)

    def get_notes(
        self,
        type,
        limit_rows: int = 500,
        limit_offset: int = 0,
        id: Optional[int] = None,
        element_id: Optional[int] = None,
        note_type: Optional[int] = None,
        if_modified_since: Optional[str] = None,
    ) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/notes
        :param type: str (contact or lead or company or task)
        :param limit_rows: int
        :param limit_offset: int
        :param id: list or int
        :param element_id: int
        :param note_type: int
        :param if_modified_since: str
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/notes'
        params = {'limit_rows': limit_rows, 'limit_offset': limit_offset, 'type': type}
        if id is not None:
            params['id'] = id
        if element_id is not None:
            params['element_id'] = element_id
        if note_type is not None:
            params['note_type'] = note_type
        if if_modified_since is not None:
            params['if-modified-since'] = if_modified_since
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

    def create_sip_incoming_leads(self, add: list) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/unsorted
        :param add: list (list of incoming leads)
        :return: dict
        """
        return self._create_or_update('incoming_leads/sip', add)

    def create_form_incoming_leads(self, add: list) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/unsorted
        :param add: list (list of incoming leads)
        :return: dict
        """
        return self._create_or_update('incoming_leads/form', add)

    def accept_incoming_leads(self, accept: list, user_id: int, status_id: int) -> dict:
        """
        :param accept: list (list of uid incoming lead)
        :param user_id: int (manager id)
        :param status_id: int (lead status id)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/incoming_leads/accept'
        params = {'accept': accept, 'user_id': user_id, 'status_id': status_id}
        return self._send_api_request('post', url, params)

    def decline_incoming_leads(self, decline: list, user_id: int) -> dict:
        """
        :param decline: list (list of uid incoming lead)
        :param user_id: int (manager id)
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/incoming_leads/accept'
        params = {'decline': decline, 'user_id': user_id}
        return self._send_api_request('post', url, params)

    def get_incoming_leads(
        self,
        page_size: int = 500,
        page: int = 1,
        categories: Optional[list] = None,
        order_by: str = 'asc',
        pipeline_id: Optional[int] = None,
    ) -> dict:
        """
        :param page_size: int
        :param page: int
        :param categories: list
        :param order_by: str
        :param pipeline_id: int
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/incoming_leads'
        params = {'page_size': page_size, 'page': page, 'order_by': order_by}
        if categories is not None:
            params['categories'] = categories
        if pipeline_id is not None:
            params['pipeline_id'] = pipeline_id
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

    def get_incoming_leads_summary(self, date_from: str, date_to: str) -> dict:
        """
        :param date_from: str
        :param date_to: str
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/incoming_leads/summary'
        params = {
            'data[filter][date][from]': date_from,
            'data[filter][date][to]': date_to,
        }
        url += '?' + urlencode(params)
        return self._send_api_request('get', url)

    def create_custom_fields(self, add: list) -> dict:
        """
        :param add: list (list of custom fields)
        :return: dict
        """
        return self._create_or_update('fields', add)

    def delete_custom_fields(self, delete: list) -> dict:
        """
        :param delete: list (list of custom_fields (id, origin))
        :return: dict
        """
        url = f'{self.crm_url}/api/v2/fields'
        params = {'delete': delete}
        return self._send_api_request('post', url, params)

    def create_pipelines(self, add: list) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/pipelines
        :param add: list (list of pipelines)
        :return: dict
        """
        url = f'{self.crm_url}/private/api/v2/json/pipelines/set'
        params = {'request': {'pipelines': {'add': add}}}
        return self._send_api_request('post', url, params)

    def update_pipelines(self, update: list) -> dict:
        """
        doc - https://www.amocrm.ru/developers/content/api/pipelines
        :param update: list (list of pipelines)
        :return: dict
        """
        url = f'{self.crm_url}/private/api/v2/json/pipelines/set'
        params = {'request': {'pipelines': {'update': update}}}
        return self._send_api_request('post', url, params)

    def delete_pipelines(self, id: Union[list, int]) -> dict:
        """
        :param id: list (list of pipelines, ot)
        :return:
        """
        url = f'{self.crm_url}/private/api/v2/json/pipelines/set'
        params = {'request': {'id': id}}
        return self._send_api_request('post', url, params)
