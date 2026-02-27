from pydantic import BaseModel, Field
from typing import Optional
from .chat import Message, Choice, Usage

class Timings(BaseModel):
    cache_n: int = Field(examples=[0])
    prompt_n: int = Field(examples=[19])
    prompt_ms: float = Field(examples=[389.253])
    prompt_per_token_ms: float = Field(examples=[20.487])
    prompt_per_second: float = Field(examples=[48.8114414018646])
    predicted_n: int = Field(examples=[968])
    predicted_ms: float = Field(examples=[19297.472])
    predicted_per_token_ms: float = Field(examples=[19.935404958677687])
    predicted_per_second: float = Field(examples=[50.16201085820982])

class LlamaCppResponse(BaseModel):
    choices: list[Choice]
    created: int = Field(examples=[1772196069])
    model: str = Field(examples=["unsloth_Qwen3.5-35B-A3B-GGUF_Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf"])
    system_fingerprint: Optional[str] = Field(default=None, examples=["b8140-39fb81f87"])
    object: str = Field(default="chat.completion", examples=["chat.completion"])
    usage: Usage
    id: str = Field(examples=["chatcmpl-YP9RoqUD99B9kiz80o7jfBo0RYRPrBpX"])
    timings: Optional[Timings] = Field(default=None)
