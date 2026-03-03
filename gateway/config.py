from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from gateway.schema import ModelConfig
from pathlib import Path
import yaml

class ModelRegistry:
    async def __init__(self, config_path: str = "models.yaml"):
        self._config_path = Path(config_path)
        self._models: dict[str, ModelConfig] = {}
        await self.reload()

    async def reload(self) -> None:
        with open(self._config_path, "r") as f:
            data = yaml.safe_load(f)

        self._models = {
            m.name: m
            for m in (ModelConfig(**entry) for entry in data.get("models", []))
        }

    async def get(self, name: str) -> ModelConfig | None:
        return self._models.get(name)

    async def list_models(self) -> list[ModelConfig]:
        return sorted(self._models.values(), key=lambda m: -m.priority)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="/gateway/envs/.env", env_file_encoding="utf-8")
    root_path: str = ""
    api_title: str = "Inference Gateway"
    request_id_header: str = "X-Request-ID"
    port: int = 8000
    gateway_api_key: str = "2357"

    backend_local_url: str = "http://0.0.0.0:8000"
    backend_modal_url: str = "http://0.0.0.0:8000"

@lru_cache
def get_settings():
    return Settings()
