from .base import Entity

from typing import Optional

class Pipelines(Entity):
    def get_pipelines(self) -> dict:
        """get leads pipelines
    
        Returns:
            dict: {
                "_total_items": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/pipelines"
                    }
                },
                "_embedded": {
                    "pipelines": [
                        {
                            "id": 3177727,
                            "name": "Воронка",
                            "sort": 1,
                            "is_main": true,
                            "is_unsorted_on": true,
                            "is_archive": false,
                            "account_id": 12345678,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727"
                                }
                            },
                            "_embedded": {
                                "statuses": [
                                    {
                                        "id": 32392156,
                                        "name": "Неразобранное",
                                        "sort": 10,
                                        "is_editable": false,
                                        "pipeline_id": 3177727,
                                        "color": "#c1c1c1",
                                        "type": 1,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392156"
                                            }
                                        }
                                    },
                                    {
                                        "id": 32392159,
                                        "name": "Первичный контакт",
                                        "sort": 20,
                                        "is_editable": true,
                                        "pipeline_id": 3177727,
                                        "color": "#99ccff",
                                        "type": 0,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392159"
                                            }
                                        }
                                    },
                                    {
                                        "id": 32392165,
                                        "name": "Принимают решение",
                                        "sort": 30,
                                        "is_editable": true,
                                        "pipeline_id": 3177727,
                                        "color": "#ffcc66",
                                        "type": 0,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392165"
                                            }
                                        }
                                    },
                                    {
                                        "id": 142,
                                        "name": "Успешно реализовано",
                                        "sort": 10000,
                                        "is_editable": false,
                                        "pipeline_id": 3177727,
                                        "color": "#CCFF66",
                                        "type": 0,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/142"
                                            }
                                        }
                                    },
                                    {
                                        "id": 143,
                                        "name": "Закрыто и не реализовано",
                                        "sort": 11000,
                                        "is_editable": false,
                                        "pipeline_id": 3177727,
                                        "color": "#D5D8DB",
                                        "type": 0,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/143"
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/leads/pipelines"
        return self._send_api_request("get", url)

    def get_pipeline(self, pipeline_id: int) -> dict:
        """get leads pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-list
        Returns:
            dict: {
                "id": 3177727,
                "name": "Воронка",
                "sort": 1,
                "is_main": true,
                "is_unsorted_on": true,
                "is_archive": false,
                "account_id": 28847170,
                "_links": {
                    "self": {
                        "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727"
                    }
                },
                "_embedded": {
                    "statuses": [
                        {
                            "id": 32392156,
                            "name": "Неразобранное",
                            "sort": 10,
                            "is_editable": false,
                            "pipeline_id": 3177727,
                            "color": "#c1c1c1",
                            "type": 1,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392156"
                                }
                            }
                        },
                        {
                            "id": 32392159,
                            "name": "Первичный контакт",
                            "sort": 20,
                            "is_editable": true,
                            "pipeline_id": 3177727,
                            "color": "#99ccff",
                            "type": 0,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392159"
                                }
                            }
                        },
                        {
                            "id": 32392165,
                            "name": "Принимают решение",
                            "sort": 30,
                            "is_editable": true,
                            "pipeline_id": 3177727,
                            "color": "#ffcc66",
                            "type": 0,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392165"
                                }
                            }
                        },
                        {
                            "id": 142,
                            "name": "Успешно реализовано",
                            "sort": 10000,
                            "is_editable": false,
                            "pipeline_id": 3177727,
                            "color": "#CCFF66",
                            "type": 0,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/142"
                                }
                            }
                        },
                        {
                            "id": 143,
                            "name": "Закрыто и не реализовано",
                            "sort": 11000,
                            "is_editable": false,
                            "pipeline_id": 3177727,
                            "color": "#D5D8DB",
                            "type": 0,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/143"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}"
        return self._send_api_request("get", url)

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
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-add
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
        url = f"{self.crm_url}/api/v4/leads/pipelines"
        params = {
            "name": name,
            "sort": sort,
            "is_main": is_main,
            "_embedded": {"statuses": statuses},
            "is_unsorted_on": is_unsorted_on,
        }
        if request_id:
            params["request_id"] = request_id
        return self._send_api_request("post", url, [params])

    def edit_pipeline(
        self,
        pipeline_id: int,
        name: str,
        sort: int,
        is_main: bool,
        is_unsorted_on: bool,
    ) -> dict:
        """Edit pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipeline-edit
        Args:
            pipeline_id (int): id of pipeline
            name (str): name of pipeline
            sort (int):  sort of pipeline
            is_main (bool): True or False, True if is main pipeline
            is_unsorted_on (bool): True if unsorted is enabled
    
        Returns:
            dict: query result
        """
        url = f"{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}"
        params = {
            "name": name,
            "sort": sort,
            "is_main": is_main,
            "is_unsorted_on": is_unsorted_on,
        }
        return self._send_api_request("patch", url, params)

    def delete_pipeline(self, pipeline_id: int) -> dict:
        """Delete pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipeline-delete
        Args:
            pipeline_id (int): id of pipeline
    
        Returns:
            dict: query result
        """
        url = f"{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}"
        return self._send_api_request("delete", url)

    def get_pipeline_statuses(self, pipeline_id: int) -> dict:
        """return pipeline Statuses
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-list
        Args:
            pipeline_id (int): id of pipeline
        Returns:
            dict: {
            "_total_items": 1,
            "_links": {
                "self": {
                    "href": "https://example.amocrm.ru/api/v4/leads/pipelines"
                }
            },
            "_embedded": {
                "pipelines": [
                    {
                        "id": 3177727,
                        "name": "Воронка",
                        "sort": 1,
                        "is_main": true,
                        "is_unsorted_on": true,
                        "is_archive": false,
                        "account_id": 12345678,
                        "_links": {
                            "self": {
                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727"
                            }
                        },
                        "_embedded": {
                            "statuses": [
                                {
                                    "id": 32392156,
                                    "name": "Неразобранное",
                                    "sort": 10,
                                    "is_editable": false,
                                    "pipeline_id": 3177727,
                                    "color": "#c1c1c1",
                                    "type": 1,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392156"
                                        }
                                    }
                                },
                                {
                                    "id": 32392159,
                                    "name": "Первичный контакт",
                                    "sort": 20,
                                    "is_editable": true,
                                    "pipeline_id": 3177727,
                                    "color": "#99ccff",
                                    "type": 0,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392159"
                                        }
                                    }
                                },
                                {
                                    "id": 32392165,
                                    "name": "Принимают решение",
                                    "sort": 30,
                                    "is_editable": true,
                                    "pipeline_id": 3177727,
                                    "color": "#ffcc66",
                                    "type": 0,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392165"
                                        }
                                    }
                                },
                                {
                                    "id": 142,
                                    "name": "Успешно реализовано",
                                    "sort": 10000,
                                    "is_editable": false,
                                    "pipeline_id": 3177727,
                                    "color": "#CCFF66",
                                    "type": 0,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/142"
                                        }
                                    }
                                },
                                {
                                    "id": 143,
                                    "name": "Закрыто и не реализовано",
                                    "sort": 11000,
                                    "is_editable": false,
                                    "pipeline_id": 3177727,
                                    "color": "#D5D8DB",
                                    "type": 0,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/143"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
        """
        url = f"{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses"
        return self._send_api_request("get", url)

    def get_pipeline_status(self, pipeline_id: int, status_id: int) -> dict:
        """Get status
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-detail
        Args:
            pipeline_id (int): id of pipeline
            status_id (int): id of status
    
        Returns:
            dict: {
                "id": 32392156,
                "name": "Неразобранное",
                "sort": 10,
                "is_editable": false,
                "pipeline_id": 3177727,
                "color": "#c1c1c1",
                "type": 1,
                "account_id": 12345678,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392156"
                    }
                }
            }
        """
        url = (
            f"{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses/{status_id}"
        )
        return self._send_api_request("get", url)

    def add_statuses_to_pipeline(self, pipeline_id: int, statuses: list) -> dict:
        """Add status tot pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-add
        Args:
            pipeline_id (int): id of pipeline
            statuses (list): list of status object
    
        Returns:
            dict: {
                "_total_items": 2,
                "_embedded": {
                    "statuses": [
                        {
                            "id": 33035290,
                            "name": "Новый этап",
                            "sort": 60,
                            "is_editable": true,
                            "pipeline_id": 3270355,
                            "color": "#fffeb2",
                            "type": 0,
                            "account_id": 1415131,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3270355/statuses/33035290"
                                }
                            }
                        },
                        {
                            "id": 33035293,
                            "name": "Новый этап 2",
                            "sort": 70,
                            "is_editable": true,
                            "pipeline_id": 3270355,
                            "color": "#fffeb2",
                            "type": 0,
                            "account_id": 1415131,
                            "request_id": "1",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3270355/statuses/33035293"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses"
        return self._send_api_request("post", url, statuses)

    def edit_pipeline_status(
        self, pipeline_id: int, status_id: int, name: str, sort: int, color: str
    ) -> dict:
        """Edit pipeline status
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-edit
        Args:
            pipeline_id (int): id of pipeline
            status_id (int): id of status
            name (str): status name
            sort (int): sort of status
            color (str): status color
    
        Returns:
            dict: {
                "id": 32392165,
                "name": "Новое название для статуса",
                "sort": 20,
                "is_editable": true,
                "pipeline_id": 3177727,
                "color": "#c1e0ff",
                "type": 0,
                "account_id": 12345678,
                "request_id": "0",
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392165"
                    }
                }
            }
        """
        url = (
            f"{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses/{status_id}"
        )
        params = {"name": name, "sort": sort, "color": color}
        return self._send_api_request("patch", url, params)

    def delete_status_from_pipeline(self, pipeline_id: int, status_id: int) -> dict:
        """Delete status from pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-delete
        Args:
            pipeline_id (int): id of pipeline
            status_id (int): id of status
    
        Returns:
            dict: {}
        """
        url = (
            f"{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses/{status_id}"
        )
        return self._send_api_request("delete", url)
