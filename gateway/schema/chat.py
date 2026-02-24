from pydantic import BaseModel
from typing import List, Dict, Union

class Message(BaseModel):
    role: str
    content: Union[str, List[Dict]]

class InputRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: bool = False