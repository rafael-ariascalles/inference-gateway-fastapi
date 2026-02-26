from gateway.schema import InputRequest
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List
import uuid
import httpx
from fastapi import HTTPException
from gateway.schema import Message

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
    def __init__(self):
        pass

    @abstractmethod
    async def _chat(self, inputs: InputRequest) -> str:
        pass

    @abstractmethod
    async def _stream_chat(self, inputs: InputRequest) -> str:
        pass

    async def _call_backend(self, coro):
        try:
            return await coro
        except httpx.ConnectError:
            raise HTTPException(status_code=502, detail={"errors": [{"message": "backend_unavailable"}]})
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail={"errors": [{"message": "gateway_timeout"}]})
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=502, detail={"errors": [{"message": "backend_error"}]})

    def _build_response(self, content: str) -> Response:
        return Response(
            id=str(uuid.uuid4().hex),
            choices=[
                Choice(message=Message(role="assistant", content=content),
                finish_reason="stop")
            ],
            usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0))

    async def chat(self, inputs: InputRequest) -> Response:
        response = await self._call_backend(self._chat(inputs))
        return self._build_response(response)

    async def stream_chat(self, inputs: InputRequest) -> Response:
        response = await self._call_backend(self._stream_chat(inputs))
        return self._build_response(response)


class EchoBackend(BackendClient):
    async def _chat(self, inputs: InputRequest) -> str:
        return "Echo: " + inputs.messages[-1].content

    async def _stream_chat(self, inputs: InputRequest) -> str:
        return "Echo: " + inputs.messages[-1].content