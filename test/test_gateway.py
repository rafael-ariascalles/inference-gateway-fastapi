import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from gateway.main import app

BASE_URL = "http://testserver"
CHAT_URL = "/v1/chat/completions"


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url=BASE_URL)


def _chat_payload(prompt: str = "hello", model: str = "echo", stream: bool = False):
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": stream,
    }


# ---------------------------------------------------------------------------
# Request-ID middleware
# ---------------------------------------------------------------------------

class TestRequestIdMiddleware:
    @pytest.mark.anyio
    async def test_returns_generated_request_id_when_none_sent(self, client):
        resp = await client.get("/healthz")
        rid = resp.headers.get("x-request-id")
        assert rid is not None
        assert len(rid) == 32  # uuid4().hex is 32 hex chars

    @pytest.mark.anyio
    async def test_echoes_caller_request_id(self, client):
        custom_id = "my-custom-request-id-123"
        resp = await client.get("/healthz", headers={"X-Request-ID": custom_id})
        assert resp.headers["x-request-id"] == custom_id

    @pytest.mark.anyio
    async def test_request_id_present_on_post_route(self, client):
        resp = await client.post(CHAT_URL, json=_chat_payload())
        assert "x-request-id" in resp.headers


# ---------------------------------------------------------------------------
# /v1/chat/completions – non-stream response shape
# ---------------------------------------------------------------------------

class TestChatCompletionsResponseShape:
    @pytest.mark.anyio
    async def test_response_has_required_top_level_keys(self, client):
        resp = await client.post(CHAT_URL, json=_chat_payload())
        assert resp.status_code == 200
        body = resp.json()
        assert "id" in body
        assert "choices" in body
        assert "usage" in body

    @pytest.mark.anyio
    async def test_choices_structure(self, client):
        body = (await client.post(CHAT_URL, json=_chat_payload())).json()
        choices = body["choices"]
        assert isinstance(choices, list)
        assert len(choices) == 1

        choice = choices[0]
        assert choice["finish_reason"] == "stop"
        msg = choice["message"]
        assert msg["role"] == "assistant"
        assert isinstance(msg["content"], str)

    @pytest.mark.anyio
    async def test_usage_fields_present(self, client):
        body = (await client.post(CHAT_URL, json=_chat_payload())).json()
        usage = body["usage"]
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            assert key in usage
            assert isinstance(usage[key], int)

    @pytest.mark.anyio
    async def test_id_is_hex_uuid(self, client):
        body = (await client.post(CHAT_URL, json=_chat_payload())).json()
        assert len(body["id"]) == 32
        int(body["id"], 16)  # raises ValueError if not valid hex


# ---------------------------------------------------------------------------
# Echo fallback path
# ---------------------------------------------------------------------------

class TestEchoFallback:
    @pytest.mark.anyio
    async def test_echo_backend_returns_echo_prefix(self, client):
        body = (await client.post(CHAT_URL, json=_chat_payload("hi there", model="echo"))).json()
        assert body["choices"][0]["message"]["content"] == "Echo: hi there"

    @pytest.mark.anyio
    async def test_unknown_model_falls_back_to_echo(self, client):
        body = (await client.post(CHAT_URL, json=_chat_payload("test", model="nonexistent_model"))).json()
        assert body["choices"][0]["message"]["content"] == "Echo: test"

    @pytest.mark.anyio
    async def test_echo_preserves_full_message_content(self, client):
        long_msg = "The quick brown fox jumps over the lazy dog"
        body = (await client.post(CHAT_URL, json=_chat_payload(long_msg))).json()
        assert body["choices"][0]["message"]["content"] == f"Echo: {long_msg}"
