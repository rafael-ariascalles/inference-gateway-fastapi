import httpx
from gateway.schema import GatewayRequest
from gateway.backend.generic import BackendClient
from gateway.config import get_settings
from loguru import logger

TIMEOUT = 120.0

class LlamaCppBackend(BackendClient):
    def __init__(self, backend_url: str):
        super().__init__(backend_url=backend_url)
        self.client = httpx.AsyncClient(timeout=TIMEOUT)

    async def _stream_chat(self, inputs: GatewayRequest) -> str:
        return "Stream: " + inputs.messages[-1].content

class LlamaCppModalBackend(LlamaCppBackend):
    
    async def _chat(self, inputs: GatewayRequest) -> str:
        prompt = inputs.messages[-1].content
        response = await self.client.post(
            self.backend_url + "/completion",
            json={
                "prompt": prompt,
                "stream": False,
            },
        )
        logger.info(response.text)
        response.raise_for_status()
        data = response.json()
        if "content" in data:
            return data["content"]
        return data["choices"][0].get("message", {}).get("content") or data["choices"][0].get("text", "")

class LlamaCppLocalBackend(LlamaCppBackend):

    async def _chat(self, inputs: GatewayRequest) -> str:
        prompt = inputs.messages[-1].content
        response = await self.client.post(
            self.backend_url + "/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
