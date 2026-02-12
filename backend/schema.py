from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]  # restrict allowed roles
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]

    # Default to llama3
    model: Optional[str] = Field(default="llama3")

    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=1.0)

    stream: Optional[bool] = False  # useful for Ollama streaming support


class ChatResponse(BaseModel):
    role: str = "assistant"
    message: str
    model: Optional[str] = None
