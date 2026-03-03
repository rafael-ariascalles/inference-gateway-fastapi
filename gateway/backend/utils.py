from pathlib import Path
from typing import Type
import yaml
from gateway.backend.generic import BackendClient
from gateway.schema.factory import ModelConfig


MODELS_CONFIG_PATH = "config/models.yaml"

def _load_models(path: str = MODELS_CONFIG_PATH, adapter_registry: dict[str, Type[BackendClient]] = None) -> dict[str, ModelConfig]:
    if adapter_registry is None:
        raise ValueError("Adapter registry is required")

    config_file = Path(path)
    if not config_file.exists():
        raise FileNotFoundError(f"Models config not found: {config_file.resolve()}")

    with open(config_file) as f:
        data = yaml.safe_load(f)

    models: dict[str, ModelConfig] = {}
    for entry in data.get("models", []):
        config = ModelConfig(**entry)
        if config.type not in adapter_registry:
            raise ValueError(
                f"Unknown backend type '{config.type}' for model '{config.name}'. "
                f"Valid types: {list(adapter_registry.keys())}"
            )
        models[config.name] = config
    return models