"""
app/services/memory.py
──────────────────────
In-memory conversation session manager with TTL expiry.
"""

from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from app.models.chat import Message
from app.core.config import settings
from app.utils.logger import logger


class Session:
    def __init__(self, session_id: str, system_prompt: Optional[str] = None):
        self.session_id = session_id
        self.system_prompt = system_prompt or settings.system_prompt
        self.history: List[Message] = []
        self.created_at: datetime = datetime.now(timezone.utc)
        self.last_active: datetime = datetime.now(timezone.utc)

    def add_message(self, role: str, content: str) -> None:
        self.history.append(Message(role=role, content=content))
        self.last_active = datetime.now(timezone.utc)
        # Trim history to max length (keep pairs to preserve context)
        max_len = settings.max_history_length
        if len(self.history) > max_len:
            self.history = self.history[-max_len:]

    def get_anthropic_messages(self) -> List[dict]:
        """Return history formatted for Anthropic API."""
        return [{"role": m.role, "content": m.content} for m in self.history]

    def is_expired(self) -> bool:
        ttl = timedelta(minutes=settings.session_ttl_minutes)
        return datetime.now(timezone.utc) - self.last_active > ttl


class MemoryService:
    def __init__(self):
        self._sessions: Dict[str, Session] = {}

    def get_or_create(
        self, session_id: Optional[str] = None, system_prompt: Optional[str] = None
    ) -> Session:
        if not session_id:
            session_id = str(uuid.uuid4())

        if session_id in self._sessions:
            session = self._sessions[session_id]
            if session.is_expired():
                logger.info(f"Session {session_id} expired — creating new.")
                session = Session(session_id, system_prompt)
                self._sessions[session_id] = session
        else:
            session = Session(session_id, system_prompt)
            self._sessions[session_id] = session
            logger.info(f"New session created: {session_id}")

        return session

    def get(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def delete(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Session deleted: {session_id}")
            return True
        return False

    def purge_expired(self) -> int:
        expired = [sid for sid, s in self._sessions.items() if s.is_expired()]
        for sid in expired:
            del self._sessions[sid]
        if expired:
            logger.info(f"Purged {len(expired)} expired sessions.")
        return len(expired)

    @property
    def active_sessions(self) -> int:
        return len(self._sessions)


# Singleton instance
memory_service = MemoryService()
