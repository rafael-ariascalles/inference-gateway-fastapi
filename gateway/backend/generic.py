from gateway.schema import GatewayRequest
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List
import uuid
import httpx
from fastapi import HTTPException
from gateway.schema import Message
from loguru import logger

#Response base on LLM response
class Choice(BaseModel):
    message: Message
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class Response(BaseModel):
    id: str
    choices: List[Choice]
    usage: Usage

class BackendClient(ABC):
    def __init__(self, backend_url: str):
        self.backend_url = backend_url
        pass

    @abstractmethod
    async def _chat(self, inputs: GatewayRequest) -> str:
        pass

    @abstractmethod
    async def _stream_chat(self, inputs: GatewayRequest) -> str:
        pass

    async def _call_backend(self, coro):
        try:
            return await coro
        except httpx.ConnectError as e:
            logger.error(e)
            raise HTTPException(status_code=502, detail={"errors": [{"message": "backend_unavailable"}]})
        except httpx.TimeoutException as e:
            logger.error(e)
            raise HTTPException(status_code=504, detail={"errors": [{"message": "gateway_timeout"}]})
        except httpx.HTTPStatusError as e:
            logger.error(e)
            raise HTTPException(status_code=502, detail={"errors": [{"message": "backend_error"}]})

    def _build_response(self, content: str) -> Response:
        return Response(
            id=str(uuid.uuid4().hex),
            choices=[
                Choice(message=Message(role="assistant", content=content),
                finish_reason="stop")
            ],
            usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0))

    async def chat(self, inputs: GatewayRequest) -> Response:
        response = await self._call_backend(self._chat(inputs))
        return self._build_response(response)

    async def stream_chat(self, inputs: GatewayRequest) -> Response:
        response = await self._call_backend(self._stream_chat(inputs))
        return self._build_response(response)


class EchoBackend(BackendClient):
    def __init__(self):
        super().__init__(backend_url="")

    async def _chat(self, inputs: GatewayRequest) -> str:
        return "Echo: " + inputs.messages[-1].content

    async def _stream_chat(self, inputs: GatewayRequest) -> str:
        return "Echo: " + inputs.messages[-1].content