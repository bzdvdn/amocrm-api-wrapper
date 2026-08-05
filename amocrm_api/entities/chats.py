from urllib.parse import urlencode

from .base import Entity


class Chats(Entity):
    def _build_get_chats_url(
        self,
        page: int,
        limit: int,
        filter_by_ids: int | list | None,
        filter_by_created_at_from: int | None,
        filter_by_created_at_to: int | None,
        with_params: list | None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/chats"
        params: dict = {"page": page, "limit": limit}
        if filter_by_ids:
            if isinstance(filter_by_ids, list):
                for index, id_ in enumerate(filter_by_ids):
                    params[f"filter[id][{index}]"] = id_
            else:
                params["filter[id]"] = filter_by_ids
        if filter_by_created_at_from:
            params["filter[created_at][from]"] = filter_by_created_at_from
        if filter_by_created_at_to:
            params["filter[created_at][to]"] = filter_by_created_at_to
        if with_params:
            params["with"] = ",".join(param for param in with_params)
        return f"{url}?{urlencode(params)}"

    def _build_get_chat_url(self, chat_id: int) -> str:
        return f"{self.crm_url}/api/v4/chats/{chat_id}"

    def get_chats(
        self,
        page: int = 1,
        limit: int = 250,
        filter_by_ids: int | list | None = None,
        filter_by_created_at_from: int | None = None,
        filter_by_created_at_to: int | None = None,
        with_params: list | None = None,
    ) -> dict:
        """Get chats
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chats-api#chats-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            filter_by_ids (Union[int, list, None], optional): chats ids. Defaults to None.
            filter_by_created_at_from (Optional[int], optional): created at from. Defaults to None.
            filter_by_created_at_to (Optional[int], optional): created at to. Defaults to None.
            with_params (Optional[list], optional): with params. Defaults to None.
        """
        url = self._build_get_chats_url(
            page,
            limit,
            filter_by_ids,
            filter_by_created_at_from,
            filter_by_created_at_to,
            with_params,
        )
        return self._send_api_request("get", url)

    def get_chat(self, chat_id: int) -> dict:
        """Get chat by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chats-api#chats-detail
        Args:
            chat_id (int): id of chat
        """
        url = self._build_get_chat_url(chat_id)
        return self._send_api_request("get", url)

    def create_chats(self, chats: list) -> dict:
        """Create chats
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chats-api#chats-add
        Args:
            chats (list): list of chats
        """
        url = f"{self.crm_url}/api/v4/chats"
        return self._send_api_request("post", url, chats)

    def update_chat(self, chat_id: int, chat: dict) -> dict:
        """Update chat by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chats-api#chats-edit
        Args:
            chat_id (int): id of chat
            chat (dict): chat model
        """
        url = self._build_get_chat_url(chat_id)
        return self._send_api_request("patch", url, chat)

    async def get_chats_async(
        self,
        page: int = 1,
        limit: int = 250,
        filter_by_ids: int | list | None = None,
        filter_by_created_at_from: int | None = None,
        filter_by_created_at_to: int | None = None,
        with_params: list | None = None,
    ) -> dict:
        """Async version of get_chats."""
        url = self._build_get_chats_url(
            page,
            limit,
            filter_by_ids,
            filter_by_created_at_from,
            filter_by_created_at_to,
            with_params,
        )
        return await self._send_api_request_async("get", url)

    async def get_chat_async(self, chat_id: int) -> dict:
        """Async version of get_chat."""
        url = self._build_get_chat_url(chat_id)
        return await self._send_api_request_async("get", url)

    async def create_chats_async(self, chats: list) -> dict:
        """Async version of create_chats."""
        url = f"{self.crm_url}/api/v4/chats"
        return await self._send_api_request_async("post", url, chats)

    async def update_chat_async(self, chat_id: int, chat: dict) -> dict:
        """Async version of update_chat."""
        url = self._build_get_chat_url(chat_id)
        return await self._send_api_request_async("patch", url, chat)
