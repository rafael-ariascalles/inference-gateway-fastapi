from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="/gateway/envs/.env", env_file_encoding="utf-8")
    root_path: str = ""
    api_title: str = "Inference Gateway"
    backend_url: str = "http://0.0.0.0:8000"
    request_id_header: str = "X-Request-ID"
    port: int = 8000
    gateway_api_key: str = "2357"

@lru_cache
def get_settings():
    return Settings()
