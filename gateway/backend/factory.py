from gateway.backend import EchoBackend, BackendClient
from gateway.schema import BackendType
from gateway.backend.llama_cpp import LlamaCppLocalBackend, LlamaCppModalBackend
from functools import lru_cache
from gateway.schema import ModelConfig
from gateway.config import ModelRegistry
from fastapi import HTTPException
import yaml

MODEL_BACKEND_REGISTRY = {
    BackendType.local_llama_cpp: LlamaCppLocalBackend,
    BackendType.modal_llama_cpp: LlamaCppModalBackend,
    BackendType.modal_vllm: EchoBackend,
    BackendType.echo: EchoBackend,
}

async def get_backend(model: str, models: dict[str, ModelConfig]) -> BackendClient:
    config = models.get(model)
    if config is None:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "model_not_found"}]})
    
    backend_type = config.type
    backend_factory = MODEL_BACKEND_REGISTRY.get(backend_type)

    if backend_factory is None:
        raise HTTPException(status_code=404, detail={"errors": [{"message": "backend_type_not_found"}]})

    return backend_factory(url=config.url)