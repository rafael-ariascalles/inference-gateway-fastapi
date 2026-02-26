from pydantic import BaseModel, Field
from typing import List, Dict, Union

class Message(BaseModel):
    role: str = Field(examples=["user"])
    content: Union[str, List[Dict]] = Field(examples=[""])

class InputRequest(BaseModel):
    model: str = Field(examples=["llama_cpp"])
    messages: List[Message]
    stream: bool = Field(examples=[False])