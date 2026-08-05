from urllib.parse import urlencode

from .base import Entity


class Talks(Entity):
    def _build_get_talks_url(
        self,
        page: int,
        limit: int,
        filter_by_talk_ids: int | list | None,
        filter_by_contact_ids: int | list | None,
        filter_by_entity_ids: int | list | None,
        filter_by_entity_type: str | None,
        filter_by_only_in_work: bool | None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/talks"
        params: dict = {"page": page, "limit": limit}
        if filter_by_talk_ids:
            params[
                "filter[talk_id][]"
                if isinstance(filter_by_talk_ids, list)
                else "filter[talk_id]"
            ] = filter_by_talk_ids
        if filter_by_contact_ids:
            params[
                "filter[contact_id][]"
                if isinstance(filter_by_contact_ids, list)
                else "filter[contact_id]"
            ] = filter_by_contact_ids
        if filter_by_entity_ids:
            params[
                "filter[entity_id][]"
                if isinstance(filter_by_entity_ids, list)
                else "filter[entity_id]"
            ] = filter_by_entity_ids
        if filter_by_entity_type:
            params["filter[entity_type]"] = filter_by_entity_type
        if filter_by_only_in_work:
            params["filter[only_in_work]"] = ""
        return f"{url}?{urlencode(params, doseq=True)}"

    def _build_get_talk_url(self, talk_id: int) -> str:
        return f"{self.crm_url}/api/v4/talks/{talk_id}"

    def _build_close_talk_url(self, talk_id: int) -> str:
        return f"{self.crm_url}/api/v4/talks/{talk_id}/close"

    def get_talks(
        self,
        page: int = 1,
        limit: int = 250,
        filter_by_talk_ids: int | list | None = None,
        filter_by_contact_ids: int | list | None = None,
        filter_by_entity_ids: int | list | None = None,
        filter_by_entity_type: str | None = None,
        filter_by_only_in_work: bool | None = None,
    ) -> dict:
        """Get talks list
        Doc: https://www.amocrm.ru/developers/content/crm_platform/talks-api#talks-list
        Args:
            page (int, optional): page number. Defaults to 1.
            limit (int, optional): limit per page. Defaults to 250.
            filter_by_talk_ids (Union[int, list, None], optional): talk ids filter. Defaults to None.
            filter_by_contact_ids (Union[int, list, None], optional): contact ids filter. Defaults to None.
            filter_by_entity_ids (Union[int, list, None], optional): entity ids filter. Defaults to None.
            filter_by_entity_type (Optional[str], optional): entity type (lead, customer). Defaults to None.
            filter_by_only_in_work (Optional[bool], optional): only opened talks. Defaults to None.

        Returns:
            dict: list of talks
        """
        url = self._build_get_talks_url(
            page,
            limit,
            filter_by_talk_ids,
            filter_by_contact_ids,
            filter_by_entity_ids,
            filter_by_entity_type,
            filter_by_only_in_work,
        )
        return self._send_api_request("get", url)

    def get_talk(self, talk_id: int) -> dict:
        """Get talk by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/talks-api#talk-detail
        Args:
            talk_id (int): talk id

        Returns:
            dict: talk model
        """
        url = self._build_get_talk_url(talk_id)
        return self._send_api_request("get", url)

    def close_talk(self, talk_id: int, force_close: bool = False) -> dict:
        """Close talk or launch NPS-bot
        Doc: https://www.amocrm.ru/developers/content/crm_platform/talks-api#talk-close
        Args:
            talk_id (int): talk id
            force_close (bool, optional): force close without NPS-bot. Defaults to False.

        Returns:
            dict: empty response
        """
        url = self._build_close_talk_url(talk_id)
        return self._send_api_request("post", url, {"force_close": force_close})

    async def get_talks_async(
        self,
        page: int = 1,
        limit: int = 250,
        filter_by_talk_ids: int | list | None = None,
        filter_by_contact_ids: int | list | None = None,
        filter_by_entity_ids: int | list | None = None,
        filter_by_entity_type: str | None = None,
        filter_by_only_in_work: bool | None = None,
    ) -> dict:
        """Async version of get_talks."""
        url = self._build_get_talks_url(
            page,
            limit,
            filter_by_talk_ids,
            filter_by_contact_ids,
            filter_by_entity_ids,
            filter_by_entity_type,
            filter_by_only_in_work,
        )
        return await self._send_api_request_async("get", url)

    async def get_talk_async(self, talk_id: int) -> dict:
        """Async version of get_talk."""
        url = self._build_get_talk_url(talk_id)
        return await self._send_api_request_async("get", url)

    async def close_talk_async(self, talk_id: int, force_close: bool = False) -> dict:
        """Async version of close_talk."""
        url = self._build_close_talk_url(talk_id)
        return await self._send_api_request_async(
            "post", url, {"force_close": force_close}
        )
