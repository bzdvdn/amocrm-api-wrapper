
from collections.abc import AsyncIterator, Iterator

from .base import Entity


class Tasks(Entity):
    def _build_execution_task_params(
        self,
        is_completed: bool,
        result: str,
    ) -> dict:
        return {"is_completed": is_completed, "result": {"text": result}}

    def get_tasks(
        self,
        page: int = 1,
        limit: int = 250,
        filters: dict | None = None,
        order: dict | None = None,
    ) -> dict:
        """Get tasks
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit row. Defaults to 250.
            filters (Optional[dict], optional): {'updated_at__from': <timestamp>, 'updated_at__to': <timestamp>}. Defaults to None.
            order (Optional[dict], optional): {'updated_at': <timestamp>}. Defaults to None.
    
        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/tasks?filter[task_type][]=2&filter[is_completed][]=1&limit=2&page=1"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/tasks?filter[task_type][]=2&filter[is_completed][]=1&limit=2&page=2"
                    }
                },
                "_embedded": {
                    "tasks": [
                        {
                            "id": 7087,
                            "created_by": 3987910,
                            "updated_by": 3987910,
                            "created_at": 1575364000,
                            "updated_at": 1575364851,
                            "responsible_user_id": 123123,
                            "group_id": 0,
                            "entity_id": 167353,
                            "entity_type": "leads",
                            "duration": 0,
                            "is_completed": true,
                            "task_type_id": 2,
                            "text": "Пригласить на бесплатную тренировку",
                            "result": [],
                            "complete_till": 1575665940,
                            "account_id": 321321,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/7087"
                                }
                            }
                        },
                        {
                            "id": 215089,
                            "created_by": 0,
                            "updated_by": 3987910,
                            "created_at": 1576767879,
                            "updated_at": 1576767914,
                            "responsible_user_id": 123123,
                            "group_id": 0,
                            "entity_id": 1035487,
                            "entity_type": "leads",
                            "duration": 0,
                            "is_completed": true,
                            "task_type_id": 2,
                            "text": "Назначить встречу с клиентом",
                            "result": [],
                            "complete_till": 1576768179,
                            "account_id": 321312,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/215089"
                                }
                            }
                        }
                    ]
                }
            }
        """
        params = {k: v for k, v in locals().items() if k != "self"}
        return self._get_entities("tasks", **params)

    def get_task(self, task_id: int) -> dict:
        """Get task
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#task-detail
        Args:
            task_id (int): id of task
    
        Returns:
            dict: {
                "id": 56981,
                "created_by": 54224,
                "updated_by": 3987910,
                "created_at": 1575910123,
                "updated_at": 1576767989,
                "responsible_user_id": 123123,
                "group_id": 0,
                "entity_id": 180765,
                "entity_type": "leads",
                "duration": 0,
                "is_completed": true,
                "task_type_id": 2,
                "text": "Назначить встречу с клиентом",
                "result": {
                    "text": "Результат есть"
                },
                "complete_till": 1575910423,
                "account_id": 321312,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/tasks/56981"
                    }
                }
            }
        """
        url = f"{self.crm_url}/api/v4/tasks/{task_id}"
        return self._send_api_request("get", url)

    def add_tasks(self, tasks: list) -> dict:
        """Add tasks
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-add
        Args:
            tasks (list): list of task objects
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/tasks"
                    }
                },
                "_embedded": {
                    "tasks": [
                        {
                            "id": 4745251,
                            "updated_at": 1588760725,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/4745251"
                                }
                            }
                        },
                        {
                            "id": 4747929,
                            "updated_at": 1588760725,
                            "request_id": "1",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/4747929"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities("tasks", tasks)

    def update_tasks(self, tasks: list) -> dict:
        """Add tasks
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-edit
        Args:
            tasks (list): list of task objects
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/tasks"
                    }
                },
                "_embedded": {
                    "tasks": [
                        {
                            "id": 4745251,
                            "updated_at": 1588760725,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/4745251"
                                }
                            }
                        },
                        {
                            "id": 4747929,
                            "updated_at": 1588760725,
                            "request_id": "1",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/4747929"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities("tasks", tasks, True)

    def execution_task(self, task_id: int, is_completed: bool, result: str) -> dict:
        """Executuin task
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-complete
        Args:
            task_id (int): id of task
            is_completed (bool): true if completed
            result: (str) text of result
    
        Returns:
            dict: {
                "is_completed": true,
                "result": {
                    "text": "Удалось связаться с клиентом"
                }
            }
        """
        url = f"{self.crm_url}/api/v4/tasks/{task_id}"
        params = self._build_execution_task_params(is_completed, result)
        return self._send_api_request("patch", url, params)

    async def get_tasks_async(
        self,
        page: int = 1,
        limit: int = 250,
        filters: dict | None = None,
        order: dict | None = None,
    ) -> dict:
        """Async version of get_tasks."""
        params = {k: v for k, v in locals().items() if k != "self"}
        return await self._get_entities_async("tasks", **params)

    def iter_tasks(
        self,
        limit: int = 250,
        filters: dict | None = None,
        order: dict | None = None,
    ) -> Iterator[dict]:
        """Iterate over all tasks across pages."""
        return self._iter_entities(
            "tasks", limit, None, filters, None, order, "tasks"
        )

    async def iter_tasks_async(
        self,
        limit: int = 250,
        filters: dict | None = None,
        order: dict | None = None,
    ) -> AsyncIterator[dict]:
        """Async version of iter_tasks."""
        async for task in self._iter_entities_async(
            "tasks", limit, None, filters, None, order, "tasks"
        ):
            yield task

    async def get_task_async(self, task_id: int) -> dict:
        """Async version of get_task."""
        url = f"{self.crm_url}/api/v4/tasks/{task_id}"
        return await self._send_api_request_async("get", url)

    async def add_tasks_async(self, tasks: list) -> dict:
        """Async version of add_tasks."""
        return await self._create_or_update_entities_async("tasks", tasks)

    async def update_tasks_async(self, tasks: list) -> dict:
        """Async version of update_tasks."""
        return await self._create_or_update_entities_async("tasks", tasks, True)

    async def execution_task_async(
        self, task_id: int, is_completed: bool, result: str
    ) -> dict:
        """Async version of execution_task."""
        url = f"{self.crm_url}/api/v4/tasks/{task_id}"
        params = self._build_execution_task_params(is_completed, result)
        return await self._send_api_request_async("patch", url, params)
