from pathlib import Path
from typing import Type

import yaml
from fastapi import HTTPException

from gateway.backend.generic import BackendClient, EchoBackend
from gateway.backend.llama_cpp import LlamaCppLocalBackend, LlamaCppModalBackend
from gateway.schema.factory import ModelConfig
from gateway.backend.utils import _load_models

########################################################
########################################################
# Adapter Registry
########################################################
########################################################
ADAPTER_REGISTRY: dict[str, Type[BackendClient]] = {
    "llama_cpp": LlamaCppLocalBackend,
    "modal_llama_cpp": LlamaCppModalBackend,
    "modal_vllm": EchoBackend,
    "echo": EchoBackend,
}

########################################################
# Models Config
########################################################
MODELS_CONFIG_PATH = "config/models.yaml"
_MODELS = _load_models(MODELS_CONFIG_PATH, ADAPTER_REGISTRY)
_BACKEND_CACHE: dict[str, BackendClient] = {}


def get_backend(model_name: str) -> BackendClient:
    cached = _BACKEND_CACHE.get(model_name)
    if cached is not None:
        return cached

    config = _MODELS.get(model_name)
    if config is None:
        raise HTTPException(
            status_code=404,
            detail={"errors": [{"message": f"model_not_found: {model_name}"}]},
        )
    adapter_cls = ADAPTER_REGISTRY[config.type]
    backend = adapter_cls(backend_url=config.url)
    _BACKEND_CACHE[model_name] = backend
    return backend

def list_models() -> list[ModelConfig]:
    return sorted(_MODELS.values(), key=lambda m: -m.priority)
