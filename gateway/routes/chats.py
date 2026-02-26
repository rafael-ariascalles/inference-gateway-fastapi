from fastapi import APIRouter
from gateway.schema import InputRequest
from gateway.config import get_settings
from gateway.backend.factory import get_backend
from gateway.backend import Response


settings = get_settings()
router = APIRouter()

@router.post("/v1/chat/completions")
async def chat_completions(inputs: InputRequest):
    if inputs.stream:
        return await streaming(inputs)
    else:
        return await generate(inputs)

async def streaming(inputs: InputRequest) -> Response:
    backend = get_backend(inputs.model)
    response = await backend.stream_chat(inputs)
    return response

async def generate(inputs: InputRequest) -> Response:
    backend = get_backend(inputs.model)
    response = await backend.chat(inputs)
    return response