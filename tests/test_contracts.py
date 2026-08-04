import unittest
from unittest import mock

from amocrm_api.base import BaseClient


def make_client() -> BaseClient:
    client = BaseClient.__new__(BaseClient)
    client.crm_url = "https://x.amocrm.ru"
    client.max_retries = 3
    client.timeout = 30.0
    client.retry_sleep_429 = 20.0
    client.retry_sleep_base = 5.0
    client._session = mock.Mock()
    return client


class ContractCase:
    def __init__(self, method_name, args, kwargs, http_method, url_part, body=None):
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        self.http_method = http_method
        self.url_part = url_part
        self.body = body


CASES = [
    ContractCase("get_leads", (), {"filters": {"name": "x"}}, "get",
                 "/api/v4/leads"),
    ContractCase("get_lead", (5,), {}, "get", "/api/v4/leads/5"),
    ContractCase("create_leads", ([{"name": "a"}],), {}, "post",
                 "/api/v4/leads", body=[{"name": "a"}]),
    ContractCase("get_contacts", (), {}, "get", "/api/v4/contacts"),
    ContractCase("get_company", (7,), {}, "get", "/api/v4/companies/7"),
    ContractCase("create_companies", ([{"name": "c"}],), {}, "post",
                 "/api/v4/companies", body=[{"name": "c"}]),
    ContractCase("get_catalog_elements", (5,), {}, "get",
                 "/api/v4/catalogs/5/elements"),
    ContractCase("add_elements_to_catalog", (5, [{"name": "e"}]), {}, "post",
                 "/api/v4/catalogs/5/elements", body=[{"name": "e"}]),
    ContractCase("get_pipeline", (7,), {}, "get", "/api/v4/leads/pipelines/7"),
    ContractCase("get_users", (), {}, "get", "/api/v4/users"),
    ContractCase("get_webhooks", (), {}, "get", "/api/v4/webhooks"),
    ContractCase("accept_unsorted", ("abc", 1, 2), {}, "post",
                 "/api/v4/leads/unsorted/abc/accept",
                 body={"user_id": 1, "status_id": 2}),
    ContractCase("create_leads_custom_fields", ([{"name": "cf"}],), {}, "post",
                 "/api/v4/leads/custom_fields", body=[{"name": "cf"}]),
    ContractCase("get_tags_by_entity_type", ("leads",), {}, "get",
                 "/api/v4/leads/tags"),
    ContractCase("install_widget", ("code",), {}, "post", "/api/v4/widgets/code"),
]


class TestEntityContracts(unittest.TestCase):
    def test_cases(self):
        client = make_client()
        with mock.patch.object(client, "_send_api_request") as mock_send:
            mock_send.return_value = {}
            for case in CASES:
                with self.subTest(method=case.method_name):
                    getattr(client, case.method_name)(*case.args, **case.kwargs)
                    call = mock_send.call_args
                    actual_method, actual_url = call[0][0], call[0][1]
                    actual_data = call[0][2] if len(call[0]) > 2 else None
                    self.assertEqual(actual_method, case.http_method, case.method_name)
                    self.assertTrue(
                        actual_url.startswith("https://x.amocrm.ru"),
                        (case.method_name, actual_url),
                    )
                    path = actual_url.split("?")[0]
                    self.assertTrue(
                        path.endswith(case.url_part),
                        (case.method_name, actual_url, case.url_part),
                    )
                    if case.body is not None:
                        self.assertEqual(actual_data, case.body, case.method_name)


class TestFilterQueryFalsy(unittest.TestCase):
    def test_zero_timestamp_is_kept(self):
        client = make_client()
        filters = {"updated_at__from": 0, "created_at__to": 0}
        result = client._create_filter_query(filters)
        self.assertEqual(result["filter[updated_at][from]"], 0)
        self.assertEqual(result["filter[created_at][to]"], 0)

    def test_none_values_are_dropped(self):
        client = make_client()
        filters = {"updated_at__from": None, "name": "x"}
        result = client._create_filter_query(filters)
        self.assertNotIn("filter[updated_at][from]", result)
        self.assertEqual(result["filter[name]"], "x")


if __name__ == "__main__":
    unittest.main()
