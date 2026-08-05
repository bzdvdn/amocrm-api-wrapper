from urllib.parse import urlencode

from .base import Entity


class Sources(Entity):
    def _build_get_sources_url(
        self, page: int, limit: int, with_params: list | None
    ) -> str:
        url = f"{self.crm_url}/api/v4/sources"
        params: dict = {"page": page, "limit": limit}
        if with_params:
            params["with"] = ",".join(param for param in with_params)
        return f"{url}?{urlencode(params)}"

    def _build_get_source_url(self, source_id: int) -> str:
        return f"{self.crm_url}/api/v4/sources/{source_id}"

    def get_sources(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: list | None = None,
    ) -> dict:
        """Get sources
        Doc: https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            with_params (Optional[list], optional): with params. Defaults to None.
        """
        url = self._build_get_sources_url(page, limit, with_params)
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
    ) -> dict:
        """Async version of get_sources."""
        url = self._build_get_sources_url(page, limit, with_params)
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
