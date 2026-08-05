from urllib.parse import urlencode

from .base import Entity


class Sources(Entity):
    def _build_get_sources_url(
        self,
        page: int,
        limit: int,
        with_params: list | None,
        filter_by_external_id: int | str | bool | list | None = None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/sources"
        params: dict = {"page": page, "limit": limit}
        if with_params:
            params["with"] = ",".join(param for param in with_params)
        if filter_by_external_id is not None:
            if isinstance(filter_by_external_id, list):
                params["filter[external_id][]"] = filter_by_external_id
            else:
                params["filter[external_id]"] = filter_by_external_id
        return f"{url}?{urlencode(params, doseq=True)}"

    def _build_get_source_url(self, source_id: int) -> str:
        return f"{self.crm_url}/api/v4/sources/{source_id}"

    def get_sources(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: list | None = None,
        filter_by_external_id: int | str | bool | list | None = None,
    ) -> dict:
        """Get sources
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            with_params (Optional[list], optional): with params. Defaults to None.
            filter_by_external_id (Union[int, str, bool, list, None], optional): filter by external id. Defaults to None.
        """
        url = self._build_get_sources_url(
            page, limit, with_params, filter_by_external_id
        )
        return self._send_api_request("get", url)

    def get_source(self, source_id: int) -> dict:
        """Get source by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-detail
        Args:
            source_id (int): id of source
        """
        url = self._build_get_source_url(source_id)
        return self._send_api_request("get", url)

    def create_sources(self, sources: list) -> dict:
        """Create sources
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-add
        Args:
            sources (list): list of sources
        """
        url = f"{self.crm_url}/api/v4/sources"
        return self._send_api_request("post", url, sources)

    def update_sources(self, sources: list) -> dict:
        """Update sources
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-edit
        Args:
            sources (list): list of sources with ids
        """
        url = f"{self.crm_url}/api/v4/sources"
        return self._send_api_request("patch", url, sources)

    def delete_sources(self, sources: list) -> dict:
        """Delete sources
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-delete
        Args:
            sources (list): list of sources with ids
        """
        url = f"{self.crm_url}/api/v4/sources"
        return self._send_api_request("delete", url, sources)

    async def get_sources_async(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: list | None = None,
        filter_by_external_id: int | str | bool | list | None = None,
    ) -> dict:
        """Async version of get_sources."""
        url = self._build_get_sources_url(
            page, limit, with_params, filter_by_external_id
        )
        return await self._send_api_request_async("get", url)

    async def get_source_async(self, source_id: int) -> dict:
        """Async version of get_source."""
        url = self._build_get_source_url(source_id)
        return await self._send_api_request_async("get", url)

    async def create_sources_async(self, sources: list) -> dict:
        """Async version of create_sources."""
        url = f"{self.crm_url}/api/v4/sources"
        return await self._send_api_request_async("post", url, sources)

    async def update_sources_async(self, sources: list) -> dict:
        """Async version of update_sources."""
        url = f"{self.crm_url}/api/v4/sources"
        return await self._send_api_request_async("patch", url, sources)

    async def delete_sources_async(self, sources: list) -> dict:
        """Async version of delete_sources."""
        url = f"{self.crm_url}/api/v4/sources"
        return await self._send_api_request_async("delete", url, sources)

    def _build_get_website_buttons_url(
        self,
        page: int,
        limit: int,
        with_params: list | None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/website_buttons"
        params: dict = {"page": page, "limit": limit}
        if with_params:
            params["with"] = ",".join(param for param in with_params)
        return f"{url}?{urlencode(params)}"

    def _build_get_website_button_url(
        self, source_id: int, with_params: list | None
    ) -> str:
        url = f"{self.crm_url}/api/v4/website_buttons/{source_id}"
        if with_params:
            url = f"{url}?with={','.join(param for param in with_params)}"
        return url

    def get_website_buttons(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: list | None = None,
    ) -> dict:
        """Get CRM Plugin list
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#website-buttons-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            with_params (Optional[list], optional): with params (scripts). Defaults to None.
        """
        url = self._build_get_website_buttons_url(page, limit, with_params)
        return self._send_api_request("get", url)

    def get_website_button(
        self, source_id: int, with_params: list | None = None
    ) -> dict:
        """Get CRM Plugin by source id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#website-buttons-detail
        Args:
            source_id (int): id of source
            with_params (Optional[list], optional): with params (scripts). Defaults to None.
        """
        url = self._build_get_website_button_url(source_id, with_params)
        return self._send_api_request("get", url)

    def create_website_button(self, params: dict) -> dict:
        """Create CRM Plugin (website button)
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#website-buttons-add
        Args:
            params (dict): {'pipeline_id': int, 'trusted_websites': list, 'is_used_in_app': bool}
        """
        url = f"{self.crm_url}/api/v4/website_buttons"
        return self._send_api_request("post", url, params)

    def update_website_button(self, source_id: int, params: dict) -> dict:
        """Update CRM Plugin (add trusted websites)
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#website-buttons-edit
        Args:
            source_id (int): id of source
            params (dict): {'trusted_websites': {'add': ['my-website.com']}}
        """
        url = f"{self.crm_url}/api/v4/website_buttons/{source_id}"
        return self._send_api_request("patch", url, params)

    def connect_online_chat_to_website_button(self, source_id: int) -> dict:
        """Connect online chat to CRM Plugin
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#website-buttons-online-chat
        Args:
            source_id (int): id of source
        """
        url = f"{self.crm_url}/api/v4/website_buttons/{source_id}/online_chat"
        return self._send_api_request("post", url)

    async def get_website_buttons_async(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: list | None = None,
    ) -> dict:
        """Async version of get_website_buttons."""
        url = self._build_get_website_buttons_url(page, limit, with_params)
        return await self._send_api_request_async("get", url)

    async def get_website_button_async(
        self, source_id: int, with_params: list | None = None
    ) -> dict:
        """Async version of get_website_button."""
        url = self._build_get_website_button_url(source_id, with_params)
        return await self._send_api_request_async("get", url)

    async def create_website_button_async(self, params: dict) -> dict:
        """Async version of create_website_button."""
        url = f"{self.crm_url}/api/v4/website_buttons"
        return await self._send_api_request_async("post", url, params)

    async def update_website_button_async(
        self, source_id: int, params: dict
    ) -> dict:
        """Async version of update_website_button."""
        url = f"{self.crm_url}/api/v4/website_buttons/{source_id}"
        return await self._send_api_request_async("patch", url, params)

    async def connect_online_chat_to_website_button_async(
        self, source_id: int
    ) -> dict:
        """Async version of connect_online_chat_to_website_button."""
        url = f"{self.crm_url}/api/v4/website_buttons/{source_id}/online_chat"
        return await self._send_api_request_async("post", url)
