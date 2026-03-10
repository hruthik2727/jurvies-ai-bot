"""
app/services/ai_service.py
──────────────────────────
Google Gemini integration — standard & streaming responses.
"""

from __future__ import annotations
from typing import AsyncIterator, Optional, Iterator
import google.generativeai as genai

from app.core.config import settings
from app.models.chat import ChatRequest, ChatResponse
from app.services.memory import memory_service, Session
from app.utils.logger import logger


class AIService:
    def __init__(self):
        self._model = None
        self._configure_api()

    def _configure_api(self):
        """Configure the Google Gemini API."""
        if settings.google_api_key:
            genai.configure(api_key=settings.google_api_key)

    def _get_model(self):
        """Get or create the Gemini model instance."""
        if not self._model:
            self._model = genai.GenerativeModel(
                model_name=settings.model,
                generation_config={
                    "temperature": settings.temperature,
                    "max_output_tokens": settings.max_tokens,
                }
            )
        return self._model

    def _format_history_for_gemini(self, session: Session) -> list[dict]:
        """Convert session history to Gemini format."""
        history = []
        for msg in session.history:
            # Gemini uses 'user' and 'model' roles
            role = "user" if msg.role == "user" else "model"
            history.append({
                "role": role,
                "parts": [msg.content]
            })
        return history

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Send a message and return the full response."""
        session: Session = memory_service.get_or_create(
            session_id=request.session_id,
            system_prompt=request.system_prompt,
        )

        # Add user message to history
        session.add_message("user", request.message)

        logger.info(
            f"[{session.session_id}] User: {request.message[:80]}{'...' if len(request.message) > 80 else ''}"
        )

        try:
            model = self._get_model()
            
            # Create chat with history
            history = self._format_history_for_gemini(session)[:-1]  # Exclude the last message we just added
            chat = model.start_chat(history=history)
            
            # Add system prompt as first message if this is a new session
            if len(session.history) == 1 and session.system_prompt:
                # Prepend system prompt to the user message
                full_message = f"{session.system_prompt}\n\nUser: {request.message}"
            else:
                full_message = request.message
            
            # Send message
            response = chat.send_message(full_message)
            assistant_text = response.text

            session.add_message("assistant", assistant_text)

            logger.info(
                f"[{session.session_id}] Assistant: {assistant_text[:80]}{'...' if len(assistant_text) > 80 else ''}"
            )

            # Estimate tokens (Gemini doesn't always provide exact counts)
            input_tokens = len(request.message.split()) * 2  # Rough estimate
            output_tokens = len(assistant_text.split()) * 2

            return ChatResponse(
                session_id=session.session_id,
                message=assistant_text,
                model=settings.model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    async def stream_chat(self, request: ChatRequest) -> AsyncIterator[str]:
        """Send a message and yield streamed text chunks."""
        session: Session = memory_service.get_or_create(
            session_id=request.session_id,
            system_prompt=request.system_prompt,
        )

        session.add_message("user", request.message)
        logger.info(f"[{session.session_id}] Streaming request: {request.message[:60]}")

        full_response = []
        
        try:
            model = self._get_model()
            
            # Create chat with history
            history = self._format_history_for_gemini(session)[:-1]
            chat = model.start_chat(history=history)
            
            # Add system prompt for new sessions
            if len(session.history) == 1 and session.system_prompt:
                full_message = f"{session.system_prompt}\n\nUser: {request.message}"
            else:
                full_message = request.message
            
            # Stream response
            response = chat.send_message(full_message, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response.append(chunk.text)
                    yield chunk.text

            # Save full assistant response to memory
            complete_text = "".join(full_response)
            session.add_message("assistant", complete_text)
            logger.info(f"[{session.session_id}] Stream complete. Words: {len(complete_text.split())}")
            
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"\n[ERROR] {str(e)}"

    def chat_sync(self, message: str, session_id: Optional[str] = None) -> tuple[str, str]:
        """Synchronous chat for CLI use."""
        session: Session = memory_service.get_or_create(session_id=session_id)
        session.add_message("user", message)

        try:
            model = self._get_model()
            
            # Create chat with history
            history = self._format_history_for_gemini(session)[:-1]
            chat = model.start_chat(history=history)
            
            # Add system prompt for new sessions
            if len(session.history) == 1 and session.system_prompt:
                full_message = f"{session.system_prompt}\n\nUser: {message}"
            else:
                full_message = message
            
            response = chat.send_message(full_message)
            assistant_text = response.text
            
            session.add_message("assistant", assistant_text)
            return assistant_text, session.session_id
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise

    def stream_sync(self, message: str, session_id: Optional[str] = None) -> Iterator[tuple[str, str]]:
        """Synchronous streaming for CLI use."""
        session: Session = memory_service.get_or_create(session_id=session_id)
        session.add_message("user", message)

        full_response = []
        
        try:
            model = self._get_model()
            
            # Create chat with history
            history = self._format_history_for_gemini(session)[:-1]
            chat = model.start_chat(history=history)
            
            # Add system prompt for new sessions
            if len(session.history) == 1 and session.system_prompt:
                full_message = f"{session.system_prompt}\n\nUser: {message}"
            else:
                full_message = message
            
            response = chat.send_message(full_message, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response.append(chunk.text)
                    yield chunk.text, session.session_id

            session.add_message("assistant", "".join(full_response))
            
        except Exception as e:
            logger.error(f"Stream error: {e}")
            raise


# Singleton
ai_service = AIService()
