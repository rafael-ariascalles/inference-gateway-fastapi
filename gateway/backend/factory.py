from pathlib import Path
from typing import Type

import yaml
from fastapi import HTTPException

from gateway.backend.generic import BackendClient, EchoBackend
from gateway.backend.llama_cpp import LlamaCppLocalBackend, LlamaCppModalBackend
from gateway.schema.factory import ModelConfig

MODELS_CONFIG_PATH = "config/models.yaml"

ADAPTER_REGISTRY: dict[str, Type[BackendClient]] = {
    "llama_cpp": LlamaCppLocalBackend,
    "modal_llama_cpp": LlamaCppModalBackend,
    "vllm": EchoBackend,
    "echo": EchoBackend,
}


def _load_models(path: str = MODELS_CONFIG_PATH) -> dict[str, ModelConfig]:
    config_file = Path(path)
    if not config_file.exists():
        raise FileNotFoundError(f"Models config not found: {config_file.resolve()}")

    with open(config_file) as f:
        data = yaml.safe_load(f)

    models: dict[str, ModelConfig] = {}
    for entry in data.get("models", []):
        config = ModelConfig(**entry)
        if config.type not in ADAPTER_REGISTRY:
            raise ValueError(
                f"Unknown backend type '{config.type}' for model '{config.name}'. "
                f"Valid types: {list(ADAPTER_REGISTRY.keys())}"
            )
        models[config.name] = config
    return models


_MODELS = _load_models()
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
