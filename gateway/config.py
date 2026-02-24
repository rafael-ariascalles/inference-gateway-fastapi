from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="/gateway/envs/.env", env_file_encoding="utf-8")
    root_path: str = ""
    api_title: str = "Inference Gateway"
    backend_url: str = "http://localhost:8000"
    request_id_header: str = "X-Request-ID"

@lru_cache
def get_settings():
    return Settings()
