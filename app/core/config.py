"""
app/core/config.py
──────────────────
Central configuration — loads from .env and config/settings.yaml.
"""

import os
import yaml
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _load_yaml() -> dict:
    yaml_path = BASE_DIR / "config" / "settings.yaml"
    if yaml_path.exists():
        with open(yaml_path) as f:
            return yaml.safe_load(f) or {}
    return {}


_yaml = _load_yaml()


class Settings(BaseSettings):
    # API Key
    google_api_key: str = Field(default="", env="GOOGLE_API_KEY")

    # Model
    model: str = Field(
        default=_yaml.get("model", {}).get("name", "gemini-1.5-flash"),
        env="MODEL",
    )
    max_tokens: int = Field(
        default=_yaml.get("model", {}).get("max_tokens", 1024),
        env="MAX_TOKENS",
    )
    temperature: float = Field(
        default=_yaml.get("model", {}).get("temperature", 0.7),
        env="TEMPERATURE",
    )

    # Bot identity
    bot_name: str = _yaml.get("bot", {}).get("name", "Jurvies")
    bot_version: str = _yaml.get("bot", {}).get("version", "1.0.0")
    system_prompt: str = Field(
        default=(
            "You are Jurvies, a friendly and helpful AI assistant. "
            "You are knowledgeable, concise, and always polite."
        ),
        env="SYSTEM_PROMPT",
    )

    # Memory
    max_history_length: int = _yaml.get("memory", {}).get("max_history_length", 50)
    session_ttl_minutes: int = _yaml.get("memory", {}).get("session_ttl_minutes", 60)

    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
