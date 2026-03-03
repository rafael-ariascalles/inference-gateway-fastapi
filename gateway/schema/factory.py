from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    name: str = Field(examples=["qwen3_5_35b_a3b"])
    url: str = Field(examples=["http://host.docker.internal:8082"])
    type: str = Field(examples=["llama_cpp"])
    priority: int = Field(default=0, examples=[10])
