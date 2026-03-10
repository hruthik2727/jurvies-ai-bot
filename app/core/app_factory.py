"""
app/__init__.py  /  app/core/app_factory.py
────────────────────────────────────────────
FastAPI application factory with middleware and lifespan.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.core.config import settings
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🤖 {settings.bot_name} v{settings.bot_version} starting up...")
    logger.info(f"   Model  : {settings.model}")
    logger.info(f"   Host   : {settings.host}:{settings.port}")
    yield
    logger.info(f"🛑 {settings.bot_name} shutting down.")


def create_app() -> FastAPI:
    app = FastAPI(
        title=f"{settings.bot_name} AI Bot",
        description="A production-ready AI chatbot powered by Google Gemini.",
        version=settings.bot_version,
        lifespan=lifespan,
    )

    # CORS — allow all origins for local dev (restrict in production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(chat_router)

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "bot": settings.bot_name,
            "version": settings.bot_version,
            "docs": "/docs",
            "status": "running",
        }

    return app
