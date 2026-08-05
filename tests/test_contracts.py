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
    ContractCase("create_leads_complex", ([{"name": "a", "contacts_id": [1]}],), {}, "post",
                 "/api/v4/leads/complex", body=[{"name": "a", "contacts_id": [1]}]),
    ContractCase("get_leads_links", (5,), {}, "get", "/api/v4/leads/5/links"),
    ContractCase("link_leads_entity", (5, [{"to_entity_id": 7, "to_entity_type": "contacts"}]), {}, "post",
                 "/api/v4/leads/5/link",
                 body=[{"to_entity_id": 7, "to_entity_type": "contacts"}]),
    ContractCase("unlink_leads_entity", (5, [{"to_entity_id": 7, "to_entity_type": "contacts"}]), {}, "post",
                 "/api/v4/leads/5/unlink",
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
                 "/api/v4/contacts/5/unlink",
                 body=[{"to_entity_id": 7, "to_entity_type": "leads"}]),
    ContractCase("get_contacts_chats", (), {}, "get", "/api/v4/contacts/chats"),
    ContractCase("create_contacts_chats", ([{"contact_id": 5, "chat_id": "abc-123"}],), {}, "post",
                 "/api/v4/contacts/chats",
                 body=[{"contact_id": 5, "chat_id": "abc-123"}]),
    # companies
    ContractCase("get_companies", (), {}, "get", "/api/v4/companies"),
    ContractCase("get_company", (7,), {}, "get", "/api/v4/companies/7"),
    ContractCase("create_companies", ([{"name": "c"}],), {}, "post",
                 "/api/v4/companies", body=[{"name": "c"}]),
    ContractCase("update_companies", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/companies", body=[{"id": 5, "name": "a"}]),
    ContractCase("get_companies_links", (5,), {}, "get", "/api/v4/companies/5/links"),
    ContractCase("link_companies_entity", (5, [{"to_entity_id": 7, "to_entity_type": "contacts"}]), {}, "post",
                 "/api/v4/companies/5/link",
                 body=[{"to_entity_id": 7, "to_entity_type": "contacts"}]),
    ContractCase("unlink_companies_entity", (5, [{"to_entity_id": 7, "to_entity_type": "leads"}]), {}, "post",
                 "/api/v4/companies/5/unlink",
                 body=[{"to_entity_id": 7, "to_entity_type": "leads"}]),
    # customers
    ContractCase("get_customers_links", (5,), {}, "get", "/api/v4/customers/5/links"),
    ContractCase("link_customers_entity", (5, [{"to_entity_id": 7, "to_entity_type": "contacts"}]), {}, "post",
                 "/api/v4/customers/5/link",
                 body=[{"to_entity_id": 7, "to_entity_type": "contacts"}]),
    ContractCase("unlink_customers_entity", (5, [{"to_entity_id": 7, "to_entity_type": "leads"}]), {}, "post",
                 "/api/v4/customers/5/unlink",
                 body=[{"to_entity_id": 7, "to_entity_type": "leads"}]),
    ContractCase("set_customers_mode", ("segments", True), {}, "patch",
                 "/api/v4/customers/mode", body={"mode": "segments", "is_enabled": True}),
    ContractCase("get_customers", (), {}, "get", "/api/v4/customers"),
    ContractCase("get_customer", (5,), {}, "get", "/api/v4/customers/5"),
    ContractCase("create_customers", ([{"name": "a"}],), {}, "post",
                 "/api/v4/customers", body=[{"name": "a"}]),
    ContractCase("update_customers", ([{"id": 5, "name": "a"}],), {}, "patch",
                 "/api/v4/customers", body=[{"id": 5, "name": "a"}]),
    ContractCase("get_transactions", (), {}, "get", "/api/v4/customers/transactions"),
    ContractCase("get_transactions", (5,), {}, "get", "/api/v4/customers/5/transactions"),
    ContractCase("get_transaction", (7,), {}, "get", "/api/v4/customers/transactions/7"),
    ContractCase("get_transaction", (7, 5), {}, "get", "/api/v4/customers/5/transactions/7"),
    ContractCase("create_transactions", (5, [{"name": "tr"}]), {}, "post",
                 "/api/v4/customers/5/transactions", body=[{"name": "tr"}]),
    ContractCase("delete_transaction", (7,), {}, "delete", "/api/v4/customers/transactions/7"),
    ContractCase("delete_transaction", (7, 5), {}, "delete", "/api/v4/customers/5/transactions/7"),
    ContractCase("change_bonus_points", (5, {"earn": 100}), {}, "post",
                 "/api/v4/customers/5/bonus_points", body={"earn": 100}),
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
    ContractCase("get_catalog_custom_fields", (5,), {}, "get", "/api/v4/catalogs/5/custom_fields"),
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
    ContractCase("delete_leads_custom_field", (5,), {}, "delete", "/api/v4/leads/custom_fields/5"),
    ContractCase("delete_contacts_custom_field", (5,), {}, "delete", "/api/v4/contacts/custom_fields/5"),
    ContractCase("delete_companies_custom_field", (5,), {}, "delete", "/api/v4/companies/custom_fields/5"),
    ContractCase("delete_customers_custom_field", (5,), {}, "delete", "/api/v4/customers/custom_fields/5"),
    ContractCase("delete_catalog_custom_field", (5, 7), {}, "delete", "/api/v4/catalogs/5/custom_fields/7"),
    ContractCase("delete_customers_segments_custom_field", (5,), {}, "delete",
                 "/api/v4/customers/segments/custom_fields/5"),
    ContractCase("get_leads_custom_field_groups", (), {}, "get", "/api/v4/leads/custom_fields/groups"),
    ContractCase("get_contacts_custom_field_groups", (), {}, "get", "/api/v4/contacts/custom_fields/groups"),
    ContractCase("get_companies_custom_field_groups", (), {}, "get", "/api/v4/companies/custom_fields/groups"),
    ContractCase("get_customers_custom_field_groups", (), {}, "get", "/api/v4/customers/custom_fields/groups"),
    ContractCase("create_leads_custom_field_groups", ([{"name": "g"}],), {}, "post",
                 "/api/v4/leads/custom_fields/groups", body=[{"name": "g"}]),
    ContractCase("create_contacts_custom_field_groups", ([{"name": "g"}],), {}, "post",
                 "/api/v4/contacts/custom_fields/groups", body=[{"name": "g"}]),
    ContractCase("create_companies_custom_field_groups", ([{"name": "g"}],), {}, "post",
                 "/api/v4/companies/custom_fields/groups", body=[{"name": "g"}]),
    ContractCase("create_customers_custom_field_groups", ([{"name": "g"}],), {}, "post",
                 "/api/v4/customers/custom_fields/groups", body=[{"name": "g"}]),
    ContractCase("update_leads_custom_field_group", ("leads_29741591099841", {"name": "g"}), {}, "patch",
                 "/api/v4/leads/custom_fields/groups/leads_29741591099841", body={"name": "g"}),
    ContractCase("update_contacts_custom_field_group", ("contacts_29741591099841", {"name": "g"}), {}, "patch",
                 "/api/v4/contacts/custom_fields/groups/contacts_29741591099841", body={"name": "g"}),
    ContractCase("update_companies_custom_field_group", ("companies_29741591099841", {"name": "g"}), {}, "patch",
                 "/api/v4/companies/custom_fields/groups/companies_29741591099841", body={"name": "g"}),
    ContractCase("update_customers_custom_field_group", ("customers_29741591099841", {"name": "g"}), {}, "patch",
                 "/api/v4/customers/custom_fields/groups/customers_29741591099841", body={"name": "g"}),
    ContractCase("delete_leads_custom_field_group", ("leads_29741591099841",), {}, "delete",
                 "/api/v4/leads/custom_fields/groups/leads_29741591099841"),
    ContractCase("delete_contacts_custom_field_group", ("contacts_29741591099841",), {}, "delete",
                 "/api/v4/contacts/custom_fields/groups/contacts_29741591099841"),
    ContractCase("delete_companies_custom_field_group", ("companies_29741591099841",), {}, "delete",
                 "/api/v4/companies/custom_fields/groups/companies_29741591099841"),
    ContractCase("delete_customers_custom_field_group", ("customers_29741591099841",), {}, "delete",
                 "/api/v4/customers/custom_fields/groups/customers_29741591099841"),
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
    ContractCase("update_entity_note", ("leads", 5, 7, {"note_type": "common", "params": {"text": "updated"}}), {}, "patch",
                 "/api/v4/leads/5/notes/7",
                 body={"note_type": "common", "params": {"text": "updated"}, "id": 7}),
    ContractCase("update_entity_many_notes", ("leads", [{"id": 7, "params": {"text": "updated"}}], 5), {}, "patch",
                 "/api/v4/leads/5/notes",
                 body=[{"id": 7, "params": {"text": "updated"}}]),
    ContractCase("pin_note", ("leads", 5, 7), {}, "post", "/api/v4/leads/5/notes/7/pin"),
    ContractCase("unpin_note", ("leads", 5, 7), {}, "post", "/api/v4/leads/5/notes/7/unpin"),
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
    ContractCase("link_unsorted", ("abc", {"entity_id": 7, "entity_type": "leads"}, 5), {}, "post",
                 "/api/v4/leads/unsorted/abc/link",
                 body={"link": {"entity_id": 7, "entity_type": "leads"}, "user_id": 5}),
    ContractCase("get_summary_unsorted", (), {}, "get", "/api/v4/leads/unsorted/summary"),
    # users
    ContractCase("get_users", (), {}, "get", "/api/v4/users"),
    ContractCase("get_user", (5,), {}, "get", "/api/v4/users/5"),
    ContractCase("add_users", ([{"name": "User", "email": "u@e.com"}],), {}, "post",
                 "/api/v4/users", body=[{"name": "User", "email": "u@e.com"}]),
    ContractCase("activate_users", ([{"id": 5}],), {}, "post",
                 "/api/v4/users/activate", body=[{"id": 5}]),
    ContractCase("deactivate_users", ([{"id": 5}],), {}, "post",
                 "/api/v4/users/deactivate", body=[{"id": 5}]),
    ContractCase("get_roles", (), {}, "get", "/api/v4/roles"),
    ContractCase("get_role", (5,), {}, "get", "/api/v4/roles/5"),
    ContractCase("create_roles", ([{"name": "role"}],), {}, "post",
                 "/api/v4/roles", body=[{"name": "role"}]),
    ContractCase("update_role", (5, {"name": "role"}), {}, "patch",
                 "/api/v4/roles/5", body={"name": "role"}),
    ContractCase("delete_role", (5,), {}, "delete", "/api/v4/roles/5"),
    # webhooks
    ContractCase("get_webhooks", (), {}, "get", "/api/v4/webhooks"),
    ContractCase("subscribe_webhook", ("https://example.com/hook", ["add_lead"]), {}, "post",
                 "/api/v4/webhooks",
                 body={"destination": "https://example.com/hook", "settings": ["add_lead"]}),
    ContractCase("unsubscribe_webhook", ("https://example.com/hook",), {}, "delete",
                 "/api/v4/webhooks", body={"destination": "https://example.com/hook"}),
    # widgets
    ContractCase("get_widgets", (), {}, "get", "/api/v4/widgets"),
    ContractCase("get_widget", ("amo_dropbox",), {}, "get", "/api/v4/widgets/amo_dropbox"),
    ContractCase("install_widget", ("amo_dropbox",), {"settings": {"login": "user"}}, "post",
                 "/api/v4/widgets/amo_dropbox", body={"settings": {"login": "user"}}),
    ContractCase("uninstall_widget", ("amo_dropbox",), {}, "delete", "/api/v4/widgets/amo_dropbox"),
    ContractCase("continue_salesbot_widget", ("salesbot", 5, 7, {"status": "ok"}, [{"handler": "show", "params": {"text": "hi"}}]),
                 {}, "post", "/api/v4/salesbot/5/continue/7",
                 body={"data": {"status": "ok"},
                       "execute_handlers": [{"handler": "show", "params": {"text": "hi"}}]}),
    # loss reasons
    ContractCase("get_loss_reasons", (), {}, "get", "/api/v4/leads/loss_reasons"),
    ContractCase("get_loss_reason", (5,), {}, "get", "/api/v4/leads/loss_reasons/5"),
    ContractCase("create_loss_reasons", ([{"name": "reason"}],), {}, "post",
                 "/api/v4/leads/loss_reasons", body=[{"name": "reason"}]),
    ContractCase("update_loss_reasons", ([{"id": 5, "name": "reason"}],), {}, "patch",
                 "/api/v4/leads/loss_reasons", body=[{"id": 5, "name": "reason"}]),
    ContractCase("delete_loss_reason", (5,), {}, "delete", "/api/v4/leads/loss_reasons/5"),
    # sources
    ContractCase("get_sources", (), {}, "get", "/api/v4/sources"),
    ContractCase("get_source", (5,), {}, "get", "/api/v4/sources/5"),
    ContractCase("create_sources", ([{"name": "source"}],), {}, "post",
                 "/api/v4/sources", body=[{"name": "source"}]),
    ContractCase("update_sources", ([{"id": 5, "name": "source"}],), {}, "patch",
                 "/api/v4/sources", body=[{"id": 5, "name": "source"}]),
    ContractCase("delete_sources", ([{"id": 5}],), {}, "delete",
                 "/api/v4/sources", body=[{"id": 5}]),
    ContractCase("get_website_buttons", (), {}, "get", "/api/v4/website_buttons"),
    ContractCase("get_website_button", (5,), {}, "get", "/api/v4/website_buttons/5"),
    ContractCase("create_website_button", ({"pipeline_id": 5, "trusted_websites": ["example.com"]},), {}, "post",
                 "/api/v4/website_buttons",
                 body={"pipeline_id": 5, "trusted_websites": ["example.com"]}),
    ContractCase("update_website_button", (5, {"trusted_websites": {"add": ["my-site.com"]}}), {}, "patch",
                 "/api/v4/website_buttons/5",
                 body={"trusted_websites": {"add": ["my-site.com"]}}),
    ContractCase("connect_online_chat_to_website_button", (5,), {}, "post",
                 "/api/v4/website_buttons/5/online_chat"),
    # chats
    ContractCase("get_chats", (), {}, "get", "/api/v4/chats"),
    ContractCase("get_chat", (5,), {}, "get", "/api/v4/chats/5"),
    ContractCase("create_chats", ([{"conversation_id": "conv-1"}],), {}, "post",
                 "/api/v4/chats", body=[{"conversation_id": "conv-1"}]),
    ContractCase("update_chat", (5, {"name": "chat"}), {}, "patch",
                 "/api/v4/chats/5", body={"name": "chat"}),
    # talks
    ContractCase("get_talks", (), {}, "get", "/api/v4/talks"),
    ContractCase("get_talk", (5,), {}, "get", "/api/v4/talks/5"),
    ContractCase("close_talk", (5,), {}, "post", "/api/v4/talks/5/close",
                 body={"force_close": False}),
    # subscriptions
    ContractCase("get_subscriptions", ("leads", 5), {}, "get",
                 "/api/v4/leads/5/subscriptions"),
    # calls
    ContractCase("create_calls", ([{"duration": 10, "source": "src", "phone": "123123",
                                    "direction": "inbound"}],), {}, "post",
                 "/api/v4/calls",
                 body=[{"duration": 10, "source": "src", "phone": "123123",
                        "direction": "inbound"}]),
    # short links
    ContractCase("create_short_links", ([{"url": "https://ya.ru",
                                          "metadata": {"entity_type": "contacts", "entity_id": 1}}],), {}, "post",
                 "/api/v4/short_links",
                 body=[{"url": "https://ya.ru",
                        "metadata": {"entity_type": "contacts", "entity_id": 1}}]),
    # chat templates
    ContractCase("get_chat_templates", (), {}, "get", "/api/v4/chats/templates"),
    ContractCase("get_chat_template", (5,), {}, "get", "/api/v4/chats/templates/5"),
    ContractCase("create_chat_templates", ([{"name": "t", "content": "hi"}],), {}, "post",
                 "/api/v4/chats/templates", body=[{"name": "t", "content": "hi"}]),
    ContractCase("update_chat_templates", ([{"id": 5, "name": "t"}],), {}, "patch",
                 "/api/v4/chats/templates", body=[{"id": 5, "name": "t"}]),
    ContractCase("update_chat_template", (5, {"name": "t"}), {}, "patch",
                 "/api/v4/chats/templates/5", body={"name": "t"}),
    ContractCase("delete_chat_templates", ([{"id": 5}],), {}, "delete",
                 "/api/v4/chats/templates", body=[{"id": 5}]),
    ContractCase("delete_chat_template", (5,), {}, "delete", "/api/v4/chats/templates/5"),
    ContractCase("send_chat_template_to_review", (5,), {}, "post",
                 "/api/v4/chats/templates/5/review", body={}),
    ContractCase("update_chat_template_review_status", (5, 367, "rejected", "reason"), {}, "post",
                 "/api/v4/chats/templates/5/review/367",
                 body={"status": "rejected", "reject_reason": "reason"}),
    # customer statuses
    ContractCase("get_customer_statuses", (), {}, "get", "/api/v4/customers/statuses"),
    ContractCase("get_customer_status", (5,), {}, "get", "/api/v4/customers/statuses/5"),
    ContractCase("create_customer_statuses", ([{"name": "s", "sort": 100}],), {}, "post",
                 "/api/v4/customers/statuses", body=[{"name": "s", "sort": 100}]),
    ContractCase("update_customer_status", (5, {"name": "s"}), {}, "patch",
                 "/api/v4/customers/statuses/5", body={"name": "s"}),
    ContractCase("delete_customer_status", (5,), {}, "delete", "/api/v4/customers/statuses/5"),
    ContractCase("get_customer_segments", (), {}, "get", "/api/v4/customers/segments"),
    ContractCase("get_customer_segment", (5,), {}, "get", "/api/v4/customers/segments/5"),
    ContractCase("create_customer_segment", ({"name": "seg"},), {}, "post",
                 "/api/v4/customers/segments", body={"name": "seg"}),
    ContractCase("update_customer_segment", (5, {"name": "seg"}), {}, "patch",
                 "/api/v4/customers/segments/5", body={"name": "seg"}),
    ContractCase("delete_customer_segment", (5,), {}, "delete", "/api/v4/customers/segments/5"),
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
