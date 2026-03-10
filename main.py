"""
main.py
───────
Entry point for the Jurvies AI Bot web server.

Usage:
    python main.py
    uvicorn main:app --reload
"""

import uvicorn
from app.core.app_factory import create_app
from app.core.config import settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level=settings.log_level.lower(),
    )
