import httpx
from gateway.schema import InputRequest
from gateway.config import get_settings
from gateway.backend.generic import BackendClient

TIMEOUT = 120.0

class LlamaCppBackend(BackendClient):
    def __init__(self):
        self.settings = get_settings()
        self.client = httpx.AsyncClient(timeout=TIMEOUT)

    async def _chat(self, inputs: InputRequest) -> str:
        prompt = inputs.messages[-1].content
        response = await self.client.post(
            self.settings.backend_url + "/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    async def _stream_chat(self, inputs: InputRequest) -> str:
        return "Stream: " + inputs.messages[-1].content