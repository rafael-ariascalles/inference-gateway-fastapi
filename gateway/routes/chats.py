from fastapi import APIRouter
from gateway.schema import GatewayRequest
from gateway.config import get_settings
from gateway.backend.factory import get_backend
from gateway.backend import Response, BackendClient
from gateway.config import ModelRegistry
from fastapi import Request
from fastapi import Depends

settings = get_settings()
router = APIRouter()


def get_registry(request: Request) -> ModelRegistry:
    return request.app.state.model_registry

@router.post("/v1/chat/completions")
async def chat_completions(inputs: GatewayRequest, registry: ModelRegistry = Depends(get_registry)):
    backend = await get_backend(inputs.model, registry._models)
    if inputs.stream:
        return await streaming(inputs, backend)
    else:
        return await generate(inputs, backend)

async def streaming(inputs: GatewayRequest, backend: BackendClient) -> Response:
    response = await backend.stream_chat(inputs)
    return response

async def generate(inputs: GatewayRequest, backend: BackendClient) -> Response:
    response = await backend.chat(inputs)
    return response