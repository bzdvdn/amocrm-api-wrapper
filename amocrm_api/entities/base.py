import logging
from json import JSONDecodeError, loads
from time import sleep
from requests import Session, ConnectionError, ConnectTimeout, Response
from typing import Optional, Any
from urllib.parse import urlencode

from ..errors import AmoException

logger = logging.getLogger("amocrm_wrapper")


def mask_token(token: str) -> str:
    """Return a masked form of a token safe for logs and repr."""
    if not token:
        return ""
    return f"{token[:6]}...{token[-4:]}"


class Entity:
    crm_url: str = ""
    max_retries: int = 3
    timeout: Optional[float] = 30.0
    retry_sleep_base: float = 5.0
    retry_sleep_429: float = 20.0
    _session: Session

    def _init_session(self, headers: Optional[dict] = None) -> Session:
        raise NotImplementedError()

    def update_session_params(self, params: dict) -> None:
        """update session

        Args:
            params (dict): like {'IF-MODIFIED-SINCE': <datetime>}
        """
        self._session = self._init_session(params)

    def _parse_response_body(self, response: Response) -> dict:
        raw_data = response.content.decode("utf-8")
        if not raw_data:
            return {}
        data = loads(raw_data)
        return data

    def _retry_after_delay(self, response: Response, _retry_counter: int) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return max(float(retry_after), 0)
            except ValueError:
                pass
        return self.retry_sleep_429 * (2 ** _retry_counter)

    def _send_api_request(
        self, method: str, url: str, data: Any = None, _retry_counter: int = 0
    ) -> dict:
        try:
            response = self._session.__getattribute__(method)(
                url, json=data, timeout=self.timeout
            )
            if response.status_code == 204:
                return {}
            elif response.status_code == 429:
                if _retry_counter >= self.max_retries:
                    logger.error("429 http error after %s retries", _retry_counter)
                    raise AmoException({"error": "too many requests"}, code=429)
                delay = self._retry_after_delay(response, _retry_counter)
                logger.warning(
                    "429 http error, sleep %s sec, retry %s",
                    delay,
                    _retry_counter + 1,
                )
                sleep(delay)
                return self._send_api_request(
                    method, url, data, _retry_counter + 1
                )
            data = self._parse_response_body(response)
            if "error" in data or response.status_code >= 400:
                raise AmoException(data, code=response.status_code)
            json_data = data["response"] if "response" in data else data
            return json_data
        except JSONDecodeError as e:
            raise AmoException({"error": str(e)}, code=500)
        except (ConnectTimeout, ConnectionError):
            if _retry_counter >= self.max_retries:
                raise
            sleep(self.retry_sleep_base)
            self._update_session()
            return self._send_api_request(method, url, data, _retry_counter + 1)

    def _update_session(self):
        self._session = self._init_session(dict(self._session.headers))

    def _create_filter_query(self, filters: dict) -> dict:
        filter_query = {}
        filters = filters.copy()
        update_from = filters.pop("updated_at__from", None)
        update_to = filters.pop("updated_at__to", None)
        created_from = filters.pop("created_at__from", None)
        created_to = filters.pop("created_at__to", None)
        closed_from = filters.pop("closed_at__from", None)
        closed_to = filters.pop("closed_at__to", None)
        if update_from:
            filter_query["filter[updated_at][from]"] = update_from
        if update_to:
            filter_query["filter[updated_at][to]"] = update_to
        if created_from:
            filter_query["filter[created_at][from]"] = created_from
        if created_to:
            filter_query["filter[created_at][to]"] = created_to
        if closed_from:
            filter_query["filter[closed_at][from]"] = closed_from
        if closed_to:
            filter_query["filter[closed_at][to]"] = closed_to
        filter_query.update({f"filter[{k}]": v for k, v in filters.items()})
        return filter_query

    def _get_entities(
        self,
        entity: str,
        limit: int = 250,
        page: int = 1,
        with_params: Optional[list] = None,
        filters: Optional[dict] = None,
        filter_ids: Optional[list] = None,
        order: Optional[dict] = None,
    ) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}"
        params: dict = {"limit": limit, "page": page}
        if with_params:
            params["with"] = ",".join(param for param in with_params)  # type: ignore
        if filters:
            filter_query = self._create_filter_query(filters)
            params.update(filter_query)
        if filter_ids:
            query = {f'filter[id][{index}]': id_ for index, id_ in enumerate(filter_ids)}
            params.update(query)
        if order:
            order_query = {f"order[{k}]": v for k, v in order.items()}
            params.update(order_query)
        url = f"{url}?{urlencode(params)}"
        return self._send_api_request("get", url)

    def _get_entity_links(
        self, entity: str, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/{entity_id}/links"
        if filters:
            filter_query = {f"filter[{k}]": v for k, v in filters.items()}
            url = f"{url}?{urlencode(filter_query)}"
        return self._send_api_request("get", url)

    def _link_entities(self, entity: str, entity_id: int, objects: list) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/{entity_id}/link"
        return self._send_api_request("post", url, objects)

    def _unlink_entities(self, entity: str, entity_id: int, objects: list) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/{entity_id}/unlinks"
        return self._send_api_request("post", url, objects)

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
        Doc: https://www.amocrm.ru/developers/content/crm_platform/account-info
        Args:
            with_amojo_id (bool, optional): . Defaults to False.
            with_amojo_rights (bool, optional): . Defaults to False.
            with_users_groups (bool, optional): . Defaults to False.
            with_task_types (bool, optional):. Defaults to False.
            with_version (bool, optional): . Defaults to False.
            with_ventity_names (bool, optional):. Defaults to False.
            with_datetime_settings (bool, optional):. Defaults to False.
    
        Returns:
            dict: {
                "id": 1231414,
                "name": "example",
                "subdomain": "example",
                "created_at": 1585840134,
                "created_by": 321321,
                "updated_at": 1589472711,
                "updated_by": 321321,
                "current_user_id": 581651,
                "country": "RU",
                "customers_mode": "segments",
                "is_unsorted_on": true,
                "is_loss_reason_enabled": true,
                "is_helpbot_enabled": false,
                "is_technical_account": false,
                "contact_name_display_order": 1,
                "amojo_id": "f3c6340d-410e-4ad1-9f7e-c5e663599909",
                "uuid": "824f3a59-6154-4edf-ba90-0b5593715d07",
                "version": 11,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/account"
                    }
                },
                "_embedded": {
                    "amojo_rights": {
                        "can_direct": true,
                        "can_create_groups": true
                    },
                    "users_groups": [
                        {
                            "id": 0,
                            "name": "Отдел продаж",
                            "uuid": null
                        }
                    ],
                    "task_types": [
                        {
                            "id": 1,
                            "name": "Связаться",
                            "color": null,
                            "icon_id": null,
                            "code": "FOLLOW_UP"
                        },
                        {
                            "id": 2,
                            "name": "Встреча",
                            "color": null,
                            "icon_id": null,
                            "code": "MEETING"
                        }
                    ],
                    "entity_names": {
                        "leads": {
                            "ru": {
                                "gender": "m",
                                "plural_form": {
                                    "dative": "клиентам",
                                    "default": "клиенты",
                                    "genitive": "клиентов",
                                    "accusative": "клиентов",
                                    "instrumental": "клиентами",
                                    "prepositional": "клиентах"
                                },
                                "singular_form": {
                                    "dative": "клиенту",
                                    "default": "клиент",
                                    "genitive": "клиента",
                                    "accusative": "клиента",
                                    "instrumental": "клиентом",
                                    "prepositional": "клиенте"
                                }
                            },
                            "en": {
                                "singular_form": {
                                    "default": "lead"
                                },
                                "plural_form": {
                                    "default": "leads"
                                },
                                "gender": "f"
                            },
                            "es": {
                                "singular_form": {
                                    "default": "acuerdo"
                                },
                                "plural_form": {
                                    "default": "acuerdos"
                                },
                                "gender": "m"
                            }
                        }
                    },
                    "datetime_settings": {
                        "date_pattern": "d.m.Y H:i",
                        "short_date_pattern": "d.m.Y",
                        "short_time_pattern": "H:i",
                        "date_formant": "d.m.Y",
                        "time_format": "H:i:s",
                        "timezone": "Europe/Moscow",
                        "timezone_offset": "+03:00"
                    }
                }
                }
        """
        params = {k.replace("with_", ""): v for k, v in locals().items() if k != "self"}
        with_params = [param for param, value in params.items() if value]
        url = f"{self.crm_url}/api/v4/account"
        if with_params:
            url += "?with=" + ",".join(p for p in with_params)
        return self._send_api_request("get", url)

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
        url = f"{self.crm_url}/api/v4/{entity}"
        http_method = "patch" if update else "post"
        return self._send_api_request(http_method, url, objects)
