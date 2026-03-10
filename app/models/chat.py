"""
app/models/chat.py
──────────────────
Pydantic models for request/response validation.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
import uuid


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000, description="User message")
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for conversation continuity. Auto-generated if omitted.",
    )
    system_prompt: Optional[str] = Field(
        default=None,
        description="Override the default system prompt for this session.",
    )


class ChatResponse(BaseModel):
    session_id: str
    message: str
    role: Literal["assistant"] = "assistant"
    model: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    input_tokens: int = 0
    output_tokens: int = 0


class SessionInfo(BaseModel):
    session_id: str
    message_count: int
    created_at: Optional[datetime]
    history: List[Message]


class HealthResponse(BaseModel):
    status: str
    bot_name: str
    version: str
    model: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
