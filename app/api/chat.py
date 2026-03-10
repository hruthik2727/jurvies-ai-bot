"""
app/api/chat.py
───────────────
FastAPI routes for chat, streaming, and session management.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.chat import (
    ChatRequest,
    ChatResponse,
    SessionInfo,
    HealthResponse,
    ErrorResponse,
)
from app.services.ai_service import ai_service
from app.services.memory import memory_service
from app.core.config import settings
from app.utils.logger import logger
import google.generativeai as genai

router = APIRouter(prefix="/api", tags=["Jurvies Chat"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        bot_name=settings.bot_name,
        version=settings.bot_version,
        model=settings.model,
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to Jurvies and get a full response."""
    try:
        return await ai_service.chat(request)
    except Exception as e:
        error_msg = str(e)
        logger.error(f"API error: {e}")
        
        # Handle common Gemini errors
        if "API_KEY" in error_msg.upper() or "authentication" in error_msg.lower():
            raise HTTPException(status_code=401, detail="Invalid Google API key.")
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
        else:
            raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}")


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Send a message and receive a streaming text response (SSE)."""

    async def event_generator():
        try:
            async for chunk in ai_service.stream_chat(request):
                yield chunk
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"\n[ERROR] {str(e)}"

    return StreamingResponse(
        event_generator(),
        media_type="text/plain",
        headers={"X-Session-ID": request.session_id or "auto"},
    )


@router.get("/sessions/{session_id}", response_model=SessionInfo)
async def get_session(session_id: str):
    """Retrieve conversation history for a session."""
    session = memory_service.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return SessionInfo(
        session_id=session.session_id,
        message_count=len(session.history),
        created_at=session.created_at,
        history=session.history,
    )


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Clear a conversation session."""
    deleted = memory_service.delete(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"message": f"Session {session_id} cleared.", "session_id": session_id}


@router.post("/sessions/purge")
async def purge_expired():
    """Manually purge expired sessions."""
    count = memory_service.purge_expired()
    return {"purged": count, "active_sessions": memory_service.active_sessions}
