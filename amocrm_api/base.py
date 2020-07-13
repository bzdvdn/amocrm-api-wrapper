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
        with_amojo_id: bool = False,
        with_amojo_rights: bool = False,
        with_users_groups: bool = False,
        with_task_types: bool = False,
        with_version: bool = False,
        with_ventity_names: bool = False,
        with_datetime_settings: bool = False,
    ) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/account-info    
        Args:
            with_amojo_id (bool, optional): [description]. Defaults to False.
            with_amojo_rights (bool, optional): [description]. Defaults to False.
            with_users_groups (bool, optional): [description]. Defaults to False.
            with_task_types (bool, optional): [description]. Defaults to False.
            with_version (bool, optional): [description]. Defaults to False.
            with_ventity_names (bool, optional): [description]. Defaults to False.
            with_datetime_settings (bool, optional): [description]. Defaults to False.

        Returns:
            dict: query result
        """
        params = {k.replace('with_', ''): v for k, v in locals().items() if k != 'self'}
        with_params = [param for param, value in params.items() if value]
        url = f'{self.crm_url}/api/v4/account'
        url += '?with=' + ','.join(p for p in with_params)
        return self._send_api_request('get', url)

    def _create_or_update_entities(
        self, entity: str, objects: list, update: bool = False
    ) -> dict:
        """method for create or update entities

        Args:
            entity (str): name of entities like 'leads'
            objects (list): list of obejcts
            update (bool): if True http method patch else post

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/{entity}'
        http_method = 'patch' if update else 'post'
        return self._send_api_request(http_method, url, objects)

    def create_leads(self, objects: list) -> dict:
        """create leads
        doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-add
        Args:
            objects (list): list of leads

        Returns:
            dict: query result
        """
        return self._create_or_update_entities('leads', objects)

    def update_leads(self, objects: list) -> dict:
        """update leads
        doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-edit
        Args:
            objects (list): list of leads
        Returns:
            dict: query result
        """
        return self._create_or_update_entities('leads', objects, True)

    def get_lead(self, lead_id: int) -> dict:
        """return lead
        doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#lead-detail
        Args:
            lead_id (int): id of lead

        Returns:
            dict: lead obj
        """
        url = f'{self.crm_url}/api/v4/leads/{lead_id}'
        return self._send_api_request('get', url)

    def get_leads(
        self,
        limit: int = 250,
        query: Optional[str] = None,
        page: int = 1,
        with_params: Optional[list] = None,
    ) -> dict:  #
        # TODO: filter data
        """return leads

        Args:
            limit (int, optional): limit of rows. Defaults to 250.
            query (Optional[str], optional): str query. Defaults to None.
            page (int, optional): number of page. Defaults to 1.
            with_params (Optional[list], optional): params. Defaults to None.

        Returns:
            dict: 
        """
        url = f'{self.crm_url}/api/v4/leads'
        params = {'limit': limit, 'page': page}
        if query is not None:
            params['query'] = query
        if with_params:
            params['with'] = ','.join(param for param in with_params)
        url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

    def get_unsorted_leads(
        self,
        page: int = 1,
        limit: int = 250,
        filter_by_uids: Union[str, list, None] = None,
        filter_by_pipeline_id: Union[str, list, None] = None,
        filter_by_category: Union[str, list, None] = None,
        order_by: Optional[dict] = None,
    ) -> dict:
        """get unsorted leads

        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            filter_by_uids (Union[str, list, None], optional): filter by uids, values str or list. Defaults to None.
            filter_by_pipeline_id (Union[str, list, None], optional): filter by pipelines. Defaults to None.
            filter_by_category (Union[str, list, None], optional): filter by category(sip, mail, forms, chats). Defaults to None.
            order_by (Optional[dict], optional): orber by params like {'created_at': 'asc'}. Defaults to None.

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/unsorted'
        params = {'limit': limit, 'page': page}
        if filter_by_uids:
            params['filter[uid]'] = filter_by_uids
        if filter_by_category:
            params['filter[category]'] = filter_by_category
        if filter_by_pipeline_id:
            params['filter[pipeline_id]'] = filter_by_pipeline_id
        if order_by:
            orders = {f'order[{key}]': value for key, value in order_by.items()}
        url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

    def get_unsorted_by_uid(self, uid: str) -> dict:
        url = f'{self.crm_url}/api/v4/unsorted/{uid}'
        return self._send_api_request('get', url)

    def _create_unsorted(
        self,
        entity: str,
        source_uid: str,
        source_name: str,
        metadata: dict,
        conctact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """create unsorted

        Args:
            entity (str): form or sip
            source_uid (str): unique uid
            source_name (str): name of unsorted object
            metadata (dict): meta object
            conctact (dict): contact object
            lead (dict): lead object
            comapany (dict): company object
            pipeline_id (Optional[int], optional): id of pipeline. Defaults to None.
            created_at (Optional[int], optional): tamstamp of lead created. Defaults to None.
            request_id (Optional[str], optional): str. Defaults to None.

        Returns:
            dict: query result
        """
        url = f'{self.crm}/api/v4/leads/unsorted/{entity}'
        params = {
            'source_uid': source_uid,
            'source_name': source_name,
            'metadata': metadata,
            'contact': conctact,
        }
        _embedded = {'contacts': [conctact], 'leads': [lead], 'companies': [comapany]}
        params['_embedded'] = _embedded
        if request_id:
            params['request_id'] = request_id
        if pipeline_id:
            params['pipeline_id'] = pipeline_id
        if created_at:
            params['created_at'] = created_at
        return self._send_api_request('post', url, params)

    def create_unsorted_by_sip(
        self,
        source_uid: str,
        source_name: str,
        metadata: dict,
        conctact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-sip
        """
        params = {k: v for k, v in locals() if k != 'self'}
        return self._create_unsorted(entity='sip', **params)

    def create_unsorted_by_form(
        self,
        source_uid: str,
        source_name: str,
        metadata: dict,
        conctact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-form
        """
        params = {k: v for k, v in locals().items() if k != 'self'}
        return self._create_unsorted(entity='form', **params)

    def accept_unsorted(self, uid: str, user_id: int, status_id: int) -> dict:
        """Accept unsorted
        doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-accept
        Args:
            uid (str): unsorted obejct uid
            user_id (int): user id
            status_id (int): status id

        Returns:
            dict: query resutl
        """
        url = f'{self.crm_url}/api/v4/leads/unsorted/{uid}/accept'
        params = {'user_id': user_id, 'status_id': status_id}
        return self._send_api_request('post', url, params)

    def decline_unsorted(self, uid: str, user_id: int) -> dict:
        """Decline unsorted
        doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-decline
        Args:
            uid (str): unsorted object uid
            user_id (int): user id

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/leads/unsorted/{uid}/decline'
        params = {'user_id': user_id}
        return self._send_api_request('delete', url, params)

    def link_unsorted(self, uid: str, user_id: int, link: dict) -> dict:
        """Link unsorted to another entity
        doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-link
        Args:
            uid (str): unsorted object uid
            user_id (int): user id
            link (dict): link object like {'entity_id': 123, 'entity_type': 'leads'}

        Returns:
            dict: [description]
        """
        url = f'{self.crm_url}api/v4/leads/unsorted/{uid}/link'
        params = {'user_id': user_id, 'link': link}
        return self._send_api_request('post', url, params)

    def get_summary_unsorted(
        self,
        uid: Union[str, list, None] = None,
        created_at__from: Union[str, list, None] = None,
        created_at__to: Union[str, list, None] = None,
        pipeline_id: Union[str, list, None] = None,
    ) -> dict:
        """Get summarty unsorted object

        Args:
            uid (Union[str, list, None], optional): list or str uids. Defaults to None.
            created_at__from (Union[str, list, None], optional): timestamp. Defaults to None.
            created_at__to (Union[str, list, None], optional): timestamp. Defaults to None.
            pipeline_id (Union[str, list, None], optional): int. Defaults to None.

        Returns:
            dict: query result
        """
        params = {}
        if uid:
            params['filter[uid]'] = uid
        if created_at__from:
            params['filter[created_at][from]'] = created_at__from
        if created_at__to:
            params['filter[created_at][to]'] = created_at__to
        if pipeline_id:
            params['filter[pipeline_id]'] = pipeline_id
        url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

    def get_pipelines(self) -> dict:
        """get leads pipelines

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines'
        return self._send_api_request('get', url)

    def get_pipeline(self, pipeline_id: int) -> dict:
        """get leads pipeline

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}'
        return self._send_api_request('get', url)

    def create_pipeline(
        self,
        name: str,
        sort: int,
        is_main: bool,
        statuses: list,
        is_unsorted_on: bool = False,
        request_id: Optional[str] = None,
    ) -> dict:
        """craete pipeline
        doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-add
        Args:
            name (str): name of pipeline
            sort (int): sort of pipeline
            is_main (bool): True or False, True if is main pipeline
            statuses (list): list of statuses objects
            is_unsorted_on (bool, optional): True if unsorted is enabled. Defaults to False.
            request_id (Optional[str], optional): random string for check request. Defaults to None.

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines'
        params = {
            'name': name,
            'sort': sort,
            'is_main': is_main,
            'statuses': statuses,
            'is_unsorted_on': is_unsorted_on,
        }
        if request_id:
            params['request_id'] = request_id
        return self._send_api_request('post', url, params)

    def edit_pipeline(
        self,
        pipeline_id: int,
        name: str,
        sort: int,
        is_main: bool,
        is_unsorted_on: bool,
    ) -> dict:
        """Edit pipeline
        doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipeline-edit
        Args:
            pipeline_id (int): id of pipeline
            name (str): name of pipeline
            sort (int):  sort of pipeline
            is_main (bool): True or False, True if is main pipeline
            is_unsorted_on (bool): True if unsorted is enabled

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}'
        params = {
            'name': name,
            'sort': sort,
            'is_main': is_main,
            'is_unsorted_on': is_unsorted_on,
        }
        return self._send_api_request('patch', url, params)

    def delete_pipeline(self, pipeline_id: int) -> dict:
        """Delete pipeline
        doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipeline-delete
        Args:
            pipeline_id (int): id of pipeline

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}'
        return self._send_api_request('delete', url)

    def _get_custom_fields(self, entity: str) -> dict:
        url = f'{self.crm_url}/api/v4/{entity}/custom_fields'
        return self._send_api_request('get', url)

    def get_contacts_custom_fields(self) -> dict:
        return self._get_custom_fields('contacts')

    def get_leads_custom_fields(self) -> dict:
        return self._get_custom_fields('leads')

    def get_companies_custom_fields(self) -> dict:
        return self._get_custom_fields('companies')

    def get_customers_custom_fields(self) -> dict:
        return self._get_custom_fields('customers')

    def get_customer_segments_custom_fields(self) -> dict:
        return self._get_custom_fields('customers/segments')

    def get_catalog_custom_fields(self, catalog_id: str) -> dict:
        return self._get_custom_fields(f'catalogs/{catalog_id}')

    def get_users(
        self,
        page: int = 1,
        limit_rows: int = 250,
        with_role: bool = False,
        with_group: bool = False,
    ) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/users-api#users-list
        :param page: int (number of page) 
        :param limit_rows: int (limit)
        :param with_role: bool
        :param with_group: bool
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/users'
        params = {'page': page, 'limit_rows': limit_rows}
        with_ = []
        if with_group:
            with_.append('group')
        if with_role:
            with_.append('role')
        url = f'{url}?{urlencode(params)}'
        if with_:
            with_str = ','.join(i for i in with_)
            url = f'{url}&with={with_str}'
        return self._send_api_request('get', url)

    def get_user(
        self, user_id: int, with_role: bool = False, with_group: bool = False,
    ) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/users-api#user-detail
        :param user_id: int  
        :param with_role: bool
        :param with_group: bool
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/users/{user_id}'
        with_ = []
        if with_group:
            with_.append('group')
        if with_role:
            with_.append('role')
        if with_:
            with_str = ','.join(i for i in with_)
            url = f'{url}?with={with_str}'
        return self._send_api_request('get', url)

    def get_webhooks(self) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-list
        """
        url = f'{self.crm_url}/api/v4/webhooks'
        return self._send_api_request('get', url)

    def subscribe_webhook(self, destination: str, settings: list) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-list
        :param destination: str (webhook url)  
        :param settings: list (list of events)
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/webhooks'
        params = {'destination': destination, 'settings': settings}
        return self._send_api_request('post', url)

    def unsubscribe_webhook(self):
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-delete
        """
        url = f'{self.crm_url}/api/v4/webhooks'
        return self._send_api_request('delete', url)

    def get_widgets(self, page: int = 1, limit_rows: int = 250) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widgets-list
        :param page: int (page)  
        :param limit_rows: int 
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/widgets'
        params = {'page': page, 'limit': limit_rows}
        url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

    def get_widget(self, widget_code: str) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-detail
        :param widget_code: str
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/widgets/{widget_code}'
        return self._send_api_request('get', url)

    def install_widget(self, widget_code: str, **kwargs) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-install
        :param widget_code: str (page)
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/widgets/{widget_code}'
        return self._send_api_request('post', url, kwargs)

    def uninstall_widget(self, widget_code: str) -> dict:
        """
        doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-uninstall
        :param widget_code: str (page)
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/widgets/{widget_code}'
        return self._send_api_request('delete', url)
