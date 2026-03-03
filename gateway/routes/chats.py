from fastapi import APIRouter
from gateway.schema import GatewayRequest, ModelConfig
from gateway.backend.factory import get_backend, list_models
from gateway.backend.generic import BackendClient, Response

router = APIRouter()


@router.post("/v1/chat/completions")
async def chat_completions(inputs: GatewayRequest):
    backend = get_backend(inputs.model)
    if inputs.stream:
        return await streaming(inputs, backend)
    else:
        return await generate(inputs, backend)


@router.get("/v1/chat/models")
async def get_models_list() -> list[ModelConfig]:
    return list_models()


async def streaming(inputs: GatewayRequest, backend: BackendClient) -> Response:
    response = await backend.stream_chat(inputs)
    return response


async def generate(inputs: GatewayRequest, backend: BackendClient) -> Response:
    response = await backend.chat(inputs)
    return response
