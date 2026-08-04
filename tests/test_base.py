import json
import unittest
from unittest import mock

from requests import Session, ConnectionError

from amocrm_api.base import BaseClient
from amocrm_api.errors import AmoException
from amocrm_api.oauth_client import AmoOAuthClient


class FakeResponse:
    def __init__(self, body=None, status_code=200, content=None):
        self.status_code = status_code
        self.content = content if content is not None else (
            body if body is not None else b""
        )

    def json(self):
        return json.loads(self.content or b"{}")


def make_client() -> BaseClient:
    client = BaseClient.__new__(BaseClient)
    client.crm_url = "https://example.amocrm.ru"
    client.max_retries = 3
    client.timeout = 30.0
    client.retry_sleep_429 = 20.0
    client.retry_sleep_base = 5.0
    client._session = Session()
    return client


class TestSendApiRequest(unittest.TestCase):
    def test_204_returns_empty_dict(self):
        client = make_client()
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.return_value = FakeResponse(status_code=204)
            result = client._send_api_request("get", "http://x")
        self.assertEqual(result, {})
        mock_get.assert_called_once_with("http://x", json=None)

    def test_success_unwraps_response_key(self):
        client = make_client()
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.return_value = FakeResponse(
                body=json.dumps({"response": {"id": 1}}).encode()
            )
            result = client._send_api_request("get", "http://x")
        self.assertEqual(result, {"id": 1})

    def test_plain_body_without_response_key(self):
        client = make_client()
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.return_value = FakeResponse(
                body=json.dumps([1, 2]).encode()
            )
            result = client._send_api_request("get", "http://x")
        self.assertEqual(result, [1, 2])

    def test_error_key_raises(self):
        client = make_client()
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.return_value = FakeResponse(
                body=json.dumps({"error": "bad"}).encode(), status_code=400
            )
            with self.assertRaises(AmoException) as ctx:
                client._send_api_request("get", "http://x")
        self.assertEqual(ctx.exception.code, 400)

    def test_status_gte_400_raises(self):
        client = make_client()
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.return_value = FakeResponse(
                body=json.dumps({"detail": "nope"}).encode(), status_code=403
            )
            with self.assertRaises(AmoException) as ctx:
                client._send_api_request("get", "http://x")
        self.assertEqual(ctx.exception.code, 403)

    @mock.patch("amocrm_api.entities.base.sleep")
    def test_429_retries_then_exhausts(self, mock_sleep):
        client = make_client()
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.side_effect = [
                FakeResponse(status_code=429),
                FakeResponse(status_code=429),
                FakeResponse(status_code=429),
                FakeResponse(body=json.dumps({"ok": True}).encode()),
            ]
            result = client._send_api_request("get", "http://x")
        self.assertEqual(result, {"ok": True})
        self.assertEqual(mock_get.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 3)

    @mock.patch("amocrm_api.entities.base.sleep")
    def test_429_exhaustion_raises(self, mock_sleep):
        client = make_client()
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.side_effect = [FakeResponse(status_code=429)] * 5
            with self.assertRaises(AmoException) as ctx:
                client._send_api_request("get", "http://x")
        self.assertEqual(ctx.exception.code, 429)

    @mock.patch("amocrm_api.entities.base.sleep")
    def test_connection_error_retries_then_reraises(self, mock_sleep):
        client = make_client()
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.side_effect = ConnectionError
            with mock.patch.object(client, "_update_session") as mock_update:
                with self.assertRaises(ConnectionError):
                    client._send_api_request("get", "http://x")
            self.assertEqual(mock_update.call_count, 3)

    def test_json_decode_error_raises_amo_exception(self):
        client = make_client()
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.return_value = FakeResponse(
                content=b"not-json{{{"
            )
            with self.assertRaises(AmoException) as ctx:
                client._send_api_request("get", "http://x")
        self.assertEqual(ctx.exception.code, 500)


class TestCreateFilterQuery(unittest.TestCase):
    def test_does_not_mutate_input(self):
        client = make_client()
        filters = {
            "updated_at__from": 1,
            "updated_at__to": 2,
            "created_at__from": 3,
            "closed_at__from": 4,
            "custom": "x",
        }
        snapshot = dict(filters)
        result = client._create_filter_query(filters)
        self.assertEqual(filters, snapshot)
        self.assertEqual(
            result,
            {
                "filter[updated_at][from]": 1,
                "filter[updated_at][to]": 2,
                "filter[created_at][from]": 3,
                "filter[closed_at][from]": 4,
                "filter[custom]": "x",
            },
        )

    def test_empty_input(self):
        client = make_client()
        self.assertEqual(client._create_filter_query({}), {})


class TestGetEntities(unittest.TestCase):
    def test_builds_url_with_filters_ids_order_with(self):
        client = make_client()
        with mock.patch.object(client, "_send_api_request") as mock_send:
            mock_send.return_value = {}
            client._get_entities(
                "leads",
                limit=5,
                page=2,
                with_params=["contacts", "companies"],
                filters={"name": "test", "updated_at__from": 100},
                filter_ids=[1, 2],
                order={"created_at": "asc"},
            )
            url = mock_send.call_args[0][1]
        self.assertIn("/api/v4/leads?", url)
        self.assertIn("limit=5", url)
        self.assertIn("page=2", url)
        self.assertIn("with=contacts%2Ccompanies", url)
        self.assertIn("filter%5Bname%5D=test", url)
        self.assertIn("filter%5Bupdated_at%5D%5Bfrom%5D=100", url)
        self.assertIn("filter%5Bid%5D%5B0%5D=1", url)
        self.assertIn("filter%5Bid%5D%5B1%5D=2", url)
        self.assertIn("order%5Bcreated_at%5D=asc", url)

    def test_account_info_requires_no_extra_params(self):
        client = make_client()
        with mock.patch.object(client, "_send_api_request") as mock_send:
            mock_send.return_value = {}
            client.get_account_info()
            url = mock_send.call_args[0][1]
        self.assertIn("/api/v4/account", url)


class TestAmoException(unittest.TestCase):
    def test_str_includes_code_and_detail(self):
        exc = AmoException({"error": "oops"}, code=403)
        self.assertIn("403", str(exc))
        self.assertIn("oops", str(exc))


class TestOAuthClient(unittest.TestCase):
    def setUp(self):
        self.client = AmoOAuthClient(
            access_token="a",
            refresh_token="r",
            crm_url="https://example.amocrm.ru",
            client_id="cid",
            client_secret="secret",
            redirect_uri="https://example.ru/cb",
        )

    def test_tokens_property(self):
        self.assertEqual(
            self.client.tokens,
            {"access_token": "a", "refresh_token": "r"},
        )

    def test_update_tokens_raises_on_4xx(self):
        with mock.patch("amocrm_api.oauth_client.post") as mock_post:
            resp = mock.Mock()
            resp.status_code = 400
            resp.json.return_value = {"error": "invalid_grant"}
            mock_post.return_value = resp
            with self.assertRaises(AmoException) as ctx:
                self.client.update_tokens()
            self.assertEqual(ctx.exception.code, 400)

    @mock.patch("amocrm_api.oauth_client.post")
    def test_update_tokens_succeeds(self, mock_post):
        resp = mock.Mock()
        resp.status_code = 200
        resp.json.return_value = {
            "access_token": "a2",
            "refresh_token": "r2",
        }
        mock_post.return_value = resp
        self.client.update_tokens()
        self.assertEqual(self.client.access_token, "a2")
        self.assertEqual(self.client.refresh_token, "r2")

    @mock.patch("amocrm_api.oauth_client.post")
    def test_401_triggers_token_refresh_once(self, mock_post):
        refresh = mock.Mock()
        refresh.status_code = 200
        refresh.json.return_value = {
            "access_token": "a2",
            "refresh_token": "r2",
        }
        mock_post.return_value = refresh
        with mock.patch.object(
            BaseClient, "_send_api_request"
        ) as mock_send:
            mock_send.side_effect = [
                AmoException({"title": "unauthorized"}, code=401),
                {"ok": True},
            ]
            result = self.client._send_api_request("get", "http://x")
            self.assertEqual(result, {"ok": True})
            self.assertEqual(mock_send.call_count, 2)


if __name__ == "__main__":
    unittest.main()
