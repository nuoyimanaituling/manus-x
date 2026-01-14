from typing import List
from pydantic import BaseModel

class Message(BaseModel):
    message: str = ""
    attachments: List[str] = []