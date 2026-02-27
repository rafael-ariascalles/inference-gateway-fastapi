from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional
from enum import Enum

class ModelName(str, Enum):
    llama_cpp = "llama_cpp"
    echo = "echo"

class Message(BaseModel):
    role: str = Field(examples=["user"])
    content: Union[str, List[Dict]] = Field(examples=[""])

class InputRequest(BaseModel):
    model: ModelName = Field(examples=["llama_cpp"])
    messages: List[Message] = Field(examples=[[{"role": "user", "content": ""}]])
    stream: Optional[bool] = Field(default=False, examples=[False])
    max_tokens: Optional[int] = Field(default=2_000, examples=[500], ge=1, le=50_000)
    temperature: Optional[float] = Field(default=1.0, examples=[0.5], ge=0.0, le=2.0)

class Choice(BaseModel):
    finish_reason: str = Field(examples=["stop"])
    index: int = Field(examples=[0])
    message: Message

class Usage(BaseModel):
    completion_tokens: int = Field(examples=[968])
    prompt_tokens: int = Field(examples=[19])
    total_tokens: int = Field(examples=[987])

class Response(BaseModel):
    choices: list[Choice]
    object: str = Field(default="chat.completion", examples=["chat.completion"])
    usage: Usage
    id: str = Field(examples=["1234567890"])