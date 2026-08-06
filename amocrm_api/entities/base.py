import asyncio
import logging
from collections.abc import AsyncIterator, Callable, Iterator
from json import JSONDecodeError, loads
from time import sleep
from typing import Any
from urllib.parse import urlencode

import httpx
from httpx import AsyncClient, Client, Response

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
    timeout: float | None = 30.0
    retry_sleep_base: float = 5.0
    retry_sleep_429: float = 20.0
    _session: Client
    _async_session: AsyncClient

    def _init_session(self, headers: dict | None = None) -> Client:
        raise NotImplementedError()

    async def _init_async_session(self, headers: dict | None = None) -> AsyncClient:
        raise NotImplementedError()

    def update_session_params(self, params: dict) -> None:
        """update session

        Args:
            params (dict): like {'IF-MODIFIED-SINCE': <datetime>}
        """
        self._session = self._init_session(params)

    async def update_session_params_async(self, params: dict) -> None:
        """update async session

        Args:
            params (dict): like {'IF-MODIFIED-SINCE': <datetime>}
        """
        self._async_session = await self._init_async_session(params)

    def close(self) -> None:
        """Close the underlying sync HTTP session."""
        if hasattr(self, "_session"):
            self._session.close()

    async def close_async(self) -> None:
        """Close the underlying async HTTP session."""
        if hasattr(self, "_async_session"):
            await self._async_session.aclose()

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
            return self._finalize_response(
                response, method, url, data, _retry_counter, sleep
            )
        except (httpx.ConnectTimeout, httpx.ConnectError) as e:
            if _retry_counter >= self.max_retries:
                raise AmoException({"error": str(e)}, code=0)
            sleep(self.retry_sleep_base)
            self._update_session()
            return self._send_api_request(method, url, data, _retry_counter + 1)

    async def _send_api_request_async(
        self, method: str, url: str, data: Any = None, _retry_counter: int = 0
    ) -> dict:
        try:
            response = await self._async_session.__getattribute__(method)(
                url, json=data, timeout=self.timeout
            )
            return await self._finalize_response_async(
                response, method, url, data, _retry_counter
            )
        except (httpx.ConnectTimeout, httpx.ConnectError) as e:
            if _retry_counter >= self.max_retries:
                raise AmoException({"error": str(e)}, code=0)
            await asyncio.sleep(self.retry_sleep_base)
            await self._update_session_async()
            return await self._send_api_request_async(
                method, url, data, _retry_counter + 1
            )

    def _finalize_response(
        self,
        response: Response,
        method: str,
        url: str,
        data: Any,
        _retry_counter: int,
        sleeper: Callable[[float], Any],
    ) -> dict:
        if response.status_code == 204:
            return {}
        if response.status_code == 429:
            if _retry_counter >= self.max_retries:
                logger.error("429 http error after %s retries", _retry_counter)
                raise AmoException({"error": "too many requests"}, code=429)
            delay = self._retry_after_delay(response, _retry_counter)
            logger.warning(
                "429 http error, sleep %s sec, retry %s",
                delay,
                _retry_counter + 1,
            )
            sleeper(delay)
            return self._send_api_request(method, url, data, _retry_counter + 1)
        if response.status_code >= 500:
            if _retry_counter >= self.max_retries:
                logger.error("%s http error after %s retries", response.status_code, _retry_counter)
                raise AmoException({"error": "server error"}, code=response.status_code)
            delay = self.retry_sleep_base * (2 ** _retry_counter)
            logger.warning(
                "%s http error, sleep %s sec, retry %s",
                response.status_code,
                delay,
                _retry_counter + 1,
            )
            sleeper(delay)
            return self._send_api_request(method, url, data, _retry_counter + 1)
        try:
            body = self._parse_response_body(response)
        except JSONDecodeError as e:
            raise AmoException({"error": str(e)}, code=500)
        if "error" in body or response.status_code >= 400:
            raise AmoException(body, code=response.status_code)
        return body["response"] if isinstance(body, dict) and "response" in body else body

    async def _finalize_response_async(
        self,
        response: Response,
        method: str,
        url: str,
        data: Any,
        _retry_counter: int,
    ) -> dict:
        if response.status_code == 204:
            return {}
        if response.status_code == 429:
            if _retry_counter >= self.max_retries:
                logger.error("429 http error after %s retries", _retry_counter)
                raise AmoException({"error": "too many requests"}, code=429)
            delay = self._retry_after_delay(response, _retry_counter)
            logger.warning(
                "429 http error, sleep %s sec, retry %s",
                delay,
                _retry_counter + 1,
            )
            await asyncio.sleep(delay)
            return await self._send_api_request_async(
                method, url, data, _retry_counter + 1
            )
        if response.status_code >= 500:
            if _retry_counter >= self.max_retries:
                logger.error("%s http error after %s retries", response.status_code, _retry_counter)
                raise AmoException({"error": "server error"}, code=response.status_code)
            delay = self.retry_sleep_base * (2 ** _retry_counter)
            logger.warning(
                "%s http error, sleep %s sec, retry %s",
                response.status_code,
                delay,
                _retry_counter + 1,
            )
            await asyncio.sleep(delay)
            return await self._send_api_request_async(
                method, url, data, _retry_counter + 1
            )
        try:
            body = self._parse_response_body(response)
        except JSONDecodeError as e:
            raise AmoException({"error": str(e)}, code=500)
        if "error" in body or response.status_code >= 400:
            raise AmoException(body, code=response.status_code)
        return body["response"] if isinstance(body, dict) and "response" in body else body

    def _update_session(self) -> None:
        self._session = self._init_session(dict(self._session.headers))

    async def _update_session_async(self) -> None:
        self._async_session = await self._init_async_session(
            dict(self._async_session.headers)
        )

    def _create_filter_query(self, filters: dict) -> dict:
        filter_query = {}
        for key, value in filters.items():
            if value is None:
                continue
            if key.endswith("__from"):
                filter_query[f"filter[{key[:-6]}][from]"] = value
            elif key.endswith("__to"):
                filter_query[f"filter[{key[:-4]}][to]"] = value
            elif isinstance(value, list):
                filter_query[f"filter[{key}][]"] = value
            else:
                filter_query[f"filter[{key}]"] = value
        return filter_query

    def _build_get_entities_url(
        self,
        entity: str,
        limit: int = 250,
        page: int = 1,
        with_params: list | None = None,
        filters: dict | None = None,
        filter_ids: list | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/{entity}"
        params: dict = {"limit": limit, "page": page}
        if with_params:
            params["with"] = ",".join(param for param in with_params)
        if query:
            params["query"] = query
        if filters:
            filter_query = self._create_filter_query(filters)
            params.update(filter_query)
        if filter_ids:
            params["filter[id][]"] = filter_ids
        if order:
            order_query = {f"order[{k}]": v for k, v in order.items()}
            params.update(order_query)
        return f"{url}?{urlencode(params, doseq=True)}"

    def _get_entities(
        self,
        entity: str,
        limit: int = 250,
        page: int = 1,
        with_params: list | None = None,
        filters: dict | None = None,
        filter_ids: list | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> dict:
        url = self._build_get_entities_url(
            entity, limit, page, with_params, filters, filter_ids, order, query
        )
        return self._send_api_request("get", url)

    async def _get_entities_async(
        self,
        entity: str,
        limit: int = 250,
        page: int = 1,
        with_params: list | None = None,
        filters: dict | None = None,
        filter_ids: list | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> dict:
        url = self._build_get_entities_url(
            entity, limit, page, with_params, filters, filter_ids, order, query
        )
        return await self._send_api_request_async("get", url)

    def _extract_items(self, data: dict, embedded_key: str | None = None) -> list:
        embedded = data.get("_embedded") or {}
        if embedded_key:
            return embedded.get(embedded_key, [])
        for value in embedded.values():
            if isinstance(value, list):
                return value
        return []

    def _iter_entities(
        self,
        entity: str,
        limit: int = 250,
        with_params: list | None = None,
        filters: dict | None = None,
        filter_ids: list | None = None,
        order: dict | None = None,
        embedded_key: str | None = None,
        query: str | None = None,
    ) -> Iterator[dict]:
        page = 1
        while True:
            data = self._get_entities(
                entity, limit, page, with_params, filters, filter_ids, order, query
            )
            items = self._extract_items(data, embedded_key)
            if not items:
                break
            yield from items
            if len(items) < limit:
                break
            page += 1

    async def _iter_entities_async(
        self,
        entity: str,
        limit: int = 250,
        with_params: list | None = None,
        filters: dict | None = None,
        filter_ids: list | None = None,
        order: dict | None = None,
        embedded_key: str | None = None,
        query: str | None = None,
    ) -> AsyncIterator[dict]:
        page = 1
        while True:
            data = await self._get_entities_async(
                entity, limit, page, with_params, filters, filter_ids, order, query
            )
            items = self._extract_items(data, embedded_key)
            if not items:
                break
            for item in items:
                yield item
            if len(items) < limit:
                break
            page += 1

    def _get_entity_links(
        self, entity: str, entity_id: int, filters: dict | None = None
    ) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/{entity_id}/links"
        if filters:
            filter_query = {
                f"filter[{k}][]" if isinstance(v, list) else f"filter[{k}]": v
                for k, v in filters.items()
            }
            url = f"{url}?{urlencode(filter_query, doseq=True)}"
        return self._send_api_request("get", url)

    async def _get_entity_links_async(
        self, entity: str, entity_id: int, filters: dict | None = None
    ) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/{entity_id}/links"
        if filters:
            filter_query = {
                f"filter[{k}][]" if isinstance(v, list) else f"filter[{k}]": v
                for k, v in filters.items()
            }
            url = f"{url}?{urlencode(filter_query, doseq=True)}"
        return await self._send_api_request_async("get", url)

    def _link_entities(self, entity: str, entity_id: int, objects: list) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/{entity_id}/link"
        return self._send_api_request("post", url, objects)

    async def _link_entities_async(
        self, entity: str, entity_id: int, objects: list
    ) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/{entity_id}/link"
        return await self._send_api_request_async("post", url, objects)

    def _unlink_entities(self, entity: str, entity_id: int, objects: list) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/{entity_id}/unlink"
        return self._send_api_request("post", url, objects)

    async def _unlink_entities_async(
        self, entity: str, entity_id: int, objects: list
    ) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/{entity_id}/unlink"
        return await self._send_api_request_async("post", url, objects)

    def get_account_info(
        self,
        with_amojo_id: bool = False,
        with_amojo_rights: bool = False,
        with_users_groups: bool = False,
        with_task_types: bool = False,
        with_version: bool = False,
        with_entity_names: bool = False,
        with_datetime_settings: bool = False,
        with_drive_url: bool = False,
        with_is_api_filter_enabled: bool = False,
        with_invoices_settings: bool = False,
    ) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/account-info
        Args:
            with_amojo_id (bool, optional): . Defaults to False.
            with_amojo_rights (bool, optional): . Defaults to False.
            with_users_groups (bool, optional): . Defaults to False.
            with_task_types (bool, optional):. Defaults to False.
            with_version (bool, optional): . Defaults to False.
            with_entity_names (bool, optional):. Defaults to False.
            with_datetime_settings (bool, optional):. Defaults to False.
            with_drive_url (bool, optional):. Defaults to False.
            with_is_api_filter_enabled (bool, optional):. Defaults to False.
            with_invoices_settings (bool, optional):. Defaults to False.
    
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

    async def get_account_info_async(
        self,
        with_amojo_id: bool = False,
        with_amojo_rights: bool = False,
        with_users_groups: bool = False,
        with_task_types: bool = False,
        with_version: bool = False,
        with_entity_names: bool = False,
        with_datetime_settings: bool = False,
        with_drive_url: bool = False,
        with_is_api_filter_enabled: bool = False,
        with_invoices_settings: bool = False,
    ) -> dict:
        params = {k.replace("with_", ""): v for k, v in locals().items() if k != "self"}
        with_params = [param for param, value in params.items() if value]
        url = f"{self.crm_url}/api/v4/account"
        if with_params:
            url += "?with=" + ",".join(p for p in with_params)
        return await self._send_api_request_async("get", url)

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

    async def _create_or_update_entities_async(
        self, entity: str, objects: list, update: bool = False
    ) -> dict:
        """async method for create or update entities

        Args:
            entity (str): name of entities like 'leads'
            objects (list): list of obejcts
            update (bool): if True http method patch else post

        Returns:
            dict: query result
        """
        url = f"{self.crm_url}/api/v4/{entity}"
        http_method = "patch" if update else "post"
        return await self._send_api_request_async(http_method, url, objects)
