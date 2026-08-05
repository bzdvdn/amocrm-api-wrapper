import asyncio
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
    # base
    ContractCase("get_account_info", (), {}, "get", "/api/v4/account"),
    # leads
    ContractCase("get_leads", (), {}, "get", "/api/v4/leads"),
    ContractCase("get_lead", (5,), {}, "get", "/api/v4/leads/5"),
    ContractCase("create_leads", ([{"name": "a"}],), {}, "post",
                 "/api/v4/leads", body=[{"name": "a"}]),
    ContractCase("update_leads", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/leads", body=[{"id": 5, "name": "a"}]),
    ContractCase("get_leads_links", (5,), {}, "get", "/api/v4/leads/5/links"),
    ContractCase("link_leads_entity", (5, [{"to_entity_id": 7, "to_entity_type": "contacts"}]), {}, "post",
                 "/api/v4/leads/5/link",
                 body=[{"to_entity_id": 7, "to_entity_type": "contacts"}]),
    ContractCase("unlink_leads_entity", (5, [{"to_entity_id": 7, "to_entity_type": "contacts"}]), {}, "post",
                 "/api/v4/leads/5/unlinks",
                 body=[{"to_entity_id": 7, "to_entity_type": "contacts"}]),
    # contacts
    ContractCase("get_contacts", (), {}, "get", "/api/v4/contacts"),
    ContractCase("get_contact", (5,), {}, "get", "/api/v4/contacts/5"),
    ContractCase("create_contacts", ([{"name": "a"}],), {}, "post",
                 "/api/v4/contacts", body=[{"name": "a"}]),
    ContractCase("update_contacts", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/contacts", body=[{"id": 5, "name": "a"}]),
    ContractCase("get_contacts_links", (5,), {}, "get", "/api/v4/contacts/5/links"),
    ContractCase("link_contacts_entity", (5, [{"to_entity_id": 7, "to_entity_type": "leads"}]), {}, "post",
                 "/api/v4/contacts/5/link",
                 body=[{"to_entity_id": 7, "to_entity_type": "leads"}]),
    ContractCase("unlink_contacts_entity", (5, [{"to_entity_id": 7, "to_entity_type": "leads"}]), {}, "post",
                 "/api/v4/contacts/5/unlinks",
                 body=[{"to_entity_id": 7, "to_entity_type": "leads"}]),
    # companies
    ContractCase("get_companies", (), {}, "get", "/api/v4/companies"),
    ContractCase("get_company", (7,), {}, "get", "/api/v4/companies/7"),
    ContractCase("create_companies", ([{"name": "c"}],), {}, "post",
                 "/api/v4/companies", body=[{"name": "c"}]),
    ContractCase("update_companies", ([{"id": 5, "name": "a"}],), {}, "post",
                 "/api/v4/companies", body=[{"id": 5, "name": "a"}]),
    ContractCase("get_companies_links", (5,), {}, "get", "/api/v4/companies/5/links"),
    ContractCase("link_companies_entity", (5, [{"to_entity_id": 7, "to_entity_type": "contacts"}]), {}, "post",
                 "/api/v4/companies/5/link",
                 body=[{"to_entity_id": 7, "to_entity_type": "contacts"}]),
    ContractCase("unlink_companies_entity", (5, [{"to_entity_id": 7, "to_entity_type": "leads"}]), {}, "post",
                 "/api/v4/companies/5/unlinks",
                 body=[{"to_entity_id": 7, "to_entity_type": "leads"}]),
    # customers
    ContractCase("get_customers_links", (5,), {}, "get", "/api/v4/customers/5/links"),
    ContractCase("link_customers_entity", (5, [{"to_entity_id": 7, "to_entity_type": "contacts"}]), {}, "post",
                 "/api/v4/customers/5/link",
                 body=[{"to_entity_id": 7, "to_entity_type": "contacts"}]),
    ContractCase("unlink_customers_entity", (5, [{"to_entity_id": 7, "to_entity_type": "leads"}]), {}, "post",
                 "/api/v4/customers/5/unlinks",
                 body=[{"to_entity_id": 7, "to_entity_type": "leads"}]),
    # catalogs
    ContractCase("get_catalogs", (), {}, "get", "/api/v4/catalogs"),
    ContractCase("get_catalog", (5,), {}, "get", "/api/v4/catalogs/5"),
    ContractCase("create_catalogs", ([{"name": "a"}],), {}, "post",
                 "/api/v4/catalogs", body=[{"name": "a"}]),
    ContractCase("update_catalogs", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/catalogs", body=[{"id": 5, "name": "a"}]),
    ContractCase("get_catalog_elements", (5,), {}, "get",
                 "/api/v4/catalogs/5/elements"),
    ContractCase("get_catalog_element", (5, 7), {}, "get",
                 "/api/v4/catalogs/5/elements/7"),
    ContractCase("add_elements_to_catalog", (5, [{"name": "e"}]), {}, "post",
                 "/api/v4/catalogs/5/elements", body=[{"name": "e"}]),
    ContractCase("update_elements_in_catalog", (5, [{"id": 7, "name": "a"}]), {}, "patch",
                 "/api/v4/catalogs/5/elements", body=[{"id": 7, "name": "a"}]),
    # custom fields
    ContractCase("get_contacts_custom_fields", (), {}, "get", "/api/v4/contacts/custom_fields"),
    ContractCase("get_leads_custom_fields", (), {}, "get", "/api/v4/leads/custom_fields"),
    ContractCase("get_companies_custom_fields", (), {}, "get", "/api/v4/companies/custom_fields"),
    ContractCase("get_customers_custom_fields", (), {}, "get", "/api/v4/customers/custom_fields"),
    ContractCase("get_customer_segments_custom_fields", (), {}, "get", "/api/v4/customers/segments/custom_fields"),
    ContractCase("get_catalog_custom_fields", ("5",), {}, "get", "/api/v4/catalogs/5/custom_fields"),
    ContractCase("get_leads_custom_field", (5,), {}, "get", "/api/v4/leads/custom_fields/5"),
    ContractCase("get_contacts_custom_field", (5,), {}, "get", "/api/v4/contacts/custom_fields/5"),
    ContractCase("get_companies_custom_field", (5,), {}, "get", "/api/v4/companies/custom_fields/5"),
    ContractCase("get_customers_custom_field", (5,), {}, "get", "/api/v4/customers/custom_fields/5"),
    ContractCase("get_customers_segments_custom_field", (5,), {}, "get", "/api/v4/customers/segments/custom_fields/5"),
    ContractCase("get_catalog_custom_field", (5, 7), {}, "get", "/api/v4/catalogs/5/custom_fields/7"),
    ContractCase("create_leads_custom_fields", ([{"name": "a", "type": "text"}],), {}, "post",
                 "/api/v4/leads/custom_fields", body=[{"name": "a", "type": "text"}]),
    ContractCase("create_contacts_custom_fields", ([{"name": "a", "type": "text"}],), {}, "post",
                 "/api/v4/contacts/custom_fields", body=[{"name": "a", "type": "text"}]),
    ContractCase("create_companies_custom_fields", ([{"name": "a", "type": "text"}],), {}, "post",
                 "/api/v4/companies/custom_fields", body=[{"name": "a", "type": "text"}]),
    ContractCase("create_customers_custom_fields", ([{"name": "a", "type": "text"}],), {}, "post",
                 "/api/v4/customers/custom_fields", body=[{"name": "a", "type": "text"}]),
    ContractCase("create_customers_segments_custom_fields", ([{"name": "a", "type": "text"}],), {}, "post",
                 "/api/v4/customers/segments/custom_fields", body=[{"name": "a", "type": "text"}]),
    ContractCase("create_catalog_custom_fields", (5, [{"name": "a", "type": "text"}]), {}, "post",
                 "/api/v4/catalogs/5/custom_fields", body=[{"name": "a", "type": "text"}]),
    ContractCase("update_leads_custom_fields", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/leads/custom_fields", body=[{"id": 5, "name": "a"}]),
    ContractCase("update_contacts_custom_fields", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/contacts/custom_fields", body=[{"id": 5, "name": "a"}]),
    ContractCase("update_companies_custom_fields", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/companies/custom_fields", body=[{"id": 5, "name": "a"}]),
    ContractCase("update_customers_custom_fields", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/customers/custom_fields", body=[{"id": 5, "name": "a"}]),
    ContractCase("update_customers_segments_custom_fields", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/customers/segments/custom_fields", body=[{"id": 5, "name": "a"}]),
    ContractCase("update_catalog_custom_fields", (5, [{"id": 7, "name": "a"}]), {}, "patch",
                 "/api/v4/catalogs/5/custom_fields", body=[{"id": 7, "name": "a"}]),
    # events
    ContractCase("get_events_type", (), {}, "get", "/api/v4/events/types"),
    ContractCase("get_events", (), {}, "get", "/api/v4/events"),
    ContractCase("get_event", (5,), {}, "get", "/api/v4/events/5"),
    # notes
    ContractCase("get_notes_by_entity_type", ("leads",), {}, "get", "/api/v4/leads/notes"),
    ContractCase("get_notes_by_entity_type_and_entity_id", ("leads", 5), {}, "get", "/api/v4/leads/5/notes"),
    ContractCase("get_entity_note", ("leads", 7, 5), {}, "get", "/api/v4/leads/5/notes/7"),
    ContractCase("create_entity_note", ("leads", [{"note_type": "common", "params": {"text": "hi"}}], 5), {}, "post",
                 "/api/v4/leads/5/notes",
                 body=[{"note_type": "common", "params": {"text": "hi"}}]),
    ContractCase("update_entity_note", ("leads", 5, 7, {"params": {"text": "updated"}}), {}, "patch",
                 "/api/v4/leads/5/notes/7", body={"params": {"text": "updated"}}),
    ContractCase("update_entity_many_notes", ("leads", [{"id": 7, "params": {"text": "updated"}}], 5), {}, "patch",
                 "/api/v4/leads/5/notes",
                 body=[{"id": 7, "params": {"text": "updated"}}]),
    # pipelines
    ContractCase("get_pipelines", (), {}, "get", "/api/v4/leads/pipelines"),
    ContractCase("get_pipeline", (7,), {}, "get", "/api/v4/leads/pipelines/7"),
    ContractCase("create_pipeline", ("Funnel", 10, True, [{"name": "New", "sort": 10, "color": "#fff"}]), {}, "post",
                 "/api/v4/leads/pipelines",
                 body=[{"name": "Funnel", "sort": 10, "is_main": True,
                        "_embedded": {"statuses": [{"name": "New", "sort": 10, "color": "#fff"}]},
                        "is_unsorted_on": False}]),
    ContractCase("edit_pipeline", (5, "Funnel", 10, True, False), {}, "patch",
                 "/api/v4/leads/pipelines/5",
                 body={"name": "Funnel", "sort": 10, "is_main": True, "is_unsorted_on": False}),
    ContractCase("delete_pipeline", (5,), {}, "delete", "/api/v4/leads/pipelines/5"),
    ContractCase("get_pipeline_statuses", (5,), {}, "get", "/api/v4/leads/pipelines/5/statuses"),
    ContractCase("get_pipeline_status", (5, 7), {}, "get", "/api/v4/leads/pipelines/5/statuses/7"),
    ContractCase("add_statuses_to_pipeline", (5, [{"name": "New", "sort": 60, "color": "#fff"}]), {}, "post",
                 "/api/v4/leads/pipelines/5/statuses",
                 body=[{"name": "New", "sort": 60, "color": "#fff"}]),
    ContractCase("edit_pipeline_status", (5, 7, "New", 60, "#fff"), {}, "patch",
                 "/api/v4/leads/pipelines/5/statuses/7",
                 body={"name": "New", "sort": 60, "color": "#fff"}),
    ContractCase("delete_status_from_pipeline", (5, 7), {}, "delete",
                 "/api/v4/leads/pipelines/5/statuses/7"),
    # tags
    ContractCase("get_tags_by_entity_type", ("leads",), {}, "get",
                 "/api/v4/leads/tags"),
    ContractCase("add_tags_for_entity_type", ("leads", [{"name": "t"}]), {}, "post",
                 "/api/v4/leads/tags", body=[{"name": "t"}]),
    # tasks
    ContractCase("get_tasks", (), {}, "get", "/api/v4/tasks"),
    ContractCase("get_task", (5,), {}, "get", "/api/v4/tasks/5"),
    ContractCase("add_tasks", ([{"task_type_id": 1, "text": "call"}],), {}, "post",
                 "/api/v4/tasks", body=[{"task_type_id": 1, "text": "call"}]),
    ContractCase("update_tasks", ([{"id": 5, "text": "call"}],), {}, "patch",
                 "/api/v4/tasks", body=[{"id": 5, "text": "call"}]),
    ContractCase("execution_task", (5, True, "done"), {}, "patch",
                 "/api/v4/tasks/5",
                 body={"is_completed": True, "result": {"text": "done"}}),
    # unsorted
    ContractCase("get_unsorted_leads", (), {}, "get", "/api/v4/leads/unsorted"),
    ContractCase("get_unsorted_by_uid", ("abc",), {}, "get", "/api/v4/leads/unsorted/abc"),
    ContractCase("create_unsorted_by_sip", ("suid1", "Source", {"from": "7999999999"}, {"name": "c"}, {"name": "l"}, {}),
                 {}, "post", "/api/v4/leads/unsorted/sip",
                 body=[{"source_uid": "suid1", "source_name": "Source", "metadata": {"from": "7999999999"},
                        "contact": {"name": "c"},
                        "_embedded": {"contacts": [{"name": "c"}], "leads": [{"name": "l"}], "companies": [{}]}}]),
    ContractCase("create_unsorted_by_form", ("suid1", "Source", {}, {"name": "c"}, {"name": "l"}, {}),
                 {}, "post", "/api/v4/leads/unsorted/form",
                 body=[{"source_uid": "suid1", "source_name": "Source", "metadata": {},
                        "contact": {"name": "c"},
                        "_embedded": {"contacts": [{"name": "c"}], "leads": [{"name": "l"}], "companies": [{}]}}]),
    ContractCase("accept_unsorted", ("abc", 1, 2), {}, "post",
                 "/api/v4/leads/unsorted/abc/accept",
                 body={"user_id": 1, "status_id": 2}),
    ContractCase("decline_unsorted", ("abc", 5), {}, "delete",
                 "/api/v4/leads/unsorted/abc/decline", body={"user_id": 5}),
    ContractCase("link_unsorted", ("abc", 5, {"entity_id": 7, "entity_type": "leads"}), {}, "post",
                 "/api/v4/leads/unsorted/abc/link",
                 body={"user_id": 5, "link": {"entity_id": 7, "entity_type": "leads"}}),
    ContractCase("get_summary_unsorted", (), {}, "get", "/api/v4/leads/unsorted/summary"),
    # users
    ContractCase("get_users", (), {}, "get", "/api/v4/users"),
    ContractCase("get_user", (5,), {}, "get", "/api/v4/users/5"),
    # webhooks
    ContractCase("get_webhooks", (), {}, "get", "/api/v4/webhooks"),
    ContractCase("subscribe_webhook", ("https://example.com/hook", ["add_lead"]), {}, "post",
                 "/api/v4/webhooks",
                 body={"destination": "https://example.com/hook", "settings": ["add_lead"]}),
    ContractCase("unsubscribe_webhook", (), {}, "delete", "/api/v4/webhooks"),
    # widgets
    ContractCase("get_widgets", (), {}, "get", "/api/v4/widgets"),
    ContractCase("get_widget", ("amo_dropbox",), {}, "get", "/api/v4/widgets/amo_dropbox"),
    ContractCase("install_widget", ("amo_dropbox",), {"settings": {"login": "user"}}, "post",
                 "/api/v4/widgets/amo_dropbox", body={"settings": {"login": "user"}}),
    ContractCase("uninstall_widget", ("amo_dropbox",), {}, "delete", "/api/v4/widgets/amo_dropbox"),
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
                    actual_data = None
                    if len(call[0]) > 2:
                        actual_data = call[0][2]
                    elif "data" in call[1]:
                        actual_data = call[1]["data"]
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


class TestEntityContractsAsync(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_cases(self):
        async def run():
            client = make_client()
            with mock.patch.object(client, "_send_api_request_async") as mock_send:
                mock_send.return_value = {}
                for case in CASES:
                    with self.subTest(method=case.method_name):
                        await getattr(client, case.method_name + "_async")(
                            *case.args, **case.kwargs
                        )
                        call = mock_send.call_args
                        actual_method, actual_url = call[0][0], call[0][1]
                        actual_data = None
                        if len(call[0]) > 2:
                            actual_data = call[0][2]
                        elif "data" in call[1]:
                            actual_data = call[1]["data"]
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

        self.loop.run_until_complete(run())


class TestIterEntities(unittest.TestCase):
    def test_iterates_all_pages(self):
        client = make_client()
        pages = [
            {"_embedded": {"leads": [{"id": 1}, {"id": 2}]}},
            {"_embedded": {"leads": [{"id": 3}]}},
            {"_embedded": {"leads": []}},
        ]
        with mock.patch.object(client, "_get_entities", side_effect=pages) as mock_get:
            result = list(client.iter_leads(limit=2))
        self.assertEqual([item["id"] for item in result], [1, 2, 3])
        self.assertEqual(mock_get.call_count, 2)

    def test_full_page_continues_and_partial_stops(self):
        client = make_client()
        pages = [
            {"_embedded": {"contacts": [{"id": 1}, {"id": 2}]}},
            {"_embedded": {"contacts": [{"id": 3}, {"id": 4}]}},
            {"_embedded": {"contacts": [{"id": 5}]}},
        ]
        with mock.patch.object(client, "_get_entities", side_effect=pages):
            result = list(client.iter_contacts(limit=2))
        self.assertEqual([item["id"] for item in result], [1, 2, 3, 4, 5])

    def test_empty_response_stops_immediately(self):
        client = make_client()
        pages = [{"_embedded": {"tasks": []}}]
        with mock.patch.object(client, "_get_entities", side_effect=pages) as mock_get:
            result = list(client.iter_tasks())
        self.assertEqual(result, [])
        self.assertEqual(mock_get.call_count, 1)


class TestIterEntitiesAsync(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_iterates_all_pages(self):
        async def run():
            client = make_client()
            pages = [
                {"_embedded": {"leads": [{"id": 1}, {"id": 2}]}},
                {"_embedded": {"leads": [{"id": 3}]}},
                {"_embedded": {"leads": []}},
            ]
            mock_get = mock.AsyncMock(side_effect=pages)
            with mock.patch.object(client, "_get_entities_async", new=mock_get):
                result = [item["id"] async for item in client.iter_leads_async(limit=2)]
            self.assertEqual(result, [1, 2, 3])
            self.assertEqual(mock_get.await_count, 2)

        self.loop.run_until_complete(run())


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
