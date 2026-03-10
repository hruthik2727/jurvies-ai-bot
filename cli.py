"""
cli.py
──────
Jurvies AI Bot — Interactive terminal interface.

Usage:
    python cli.py

Commands (inside the chat):
    /help      — Show commands
    /clear     — Clear conversation history
    /history   — Show conversation history
    /session   — Show current session ID
    /quit      — Exit
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.rule import Rule
from rich.markdown import Markdown
from rich import print as rprint
from typing import Optional

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from app.core.config import settings
from app.services.ai_service import ai_service
from app.services.memory import memory_service
from app.utils.logger import logger

console = Console()


def print_banner():
    banner = Panel(
        Text.from_markup(
            f"[bold cyan]🤖 {settings.bot_name} AI Bot[/bold cyan]\n"
            f"[dim]Version {settings.bot_version}  •  Model: {settings.model}[/dim]\n\n"
            "[white]Type [bold]/help[/bold] for commands, [bold]/quit[/bold] to exit.[/white]"
        ),
        title="[bold green]Welcome[/bold green]",
        border_style="cyan",
        padding=(1, 4),
    )
    console.print(banner)


def print_help():
    console.print(
        Panel(
            "[bold]/help[/bold]     — Show this help\n"
            "[bold]/clear[/bold]    — Clear conversation history\n"
            "[bold]/history[/bold]  — Show conversation history\n"
            "[bold]/session[/bold]  — Show current session ID\n"
            "[bold]/quit[/bold]     — Exit the bot",
            title="[yellow]Commands[/yellow]",
            border_style="yellow",
        )
    )


def print_history(session_id: Optional[str]):
    if not session_id:
        console.print("[dim]No conversation history yet. Start chatting first![/dim]")
        return
    session = memory_service.get(session_id)
    if not session or not session.history:
        console.print("[dim]No conversation history yet.[/dim]")
        return
    console.print(Rule("[dim]Conversation History[/dim]"))
    for msg in session.history:
        role_color = "cyan" if msg.role == "user" else "green"
        label = "You" if msg.role == "user" else settings.bot_name
        console.print(f"[{role_color}][bold]{label}:[/bold][/{role_color}] {msg.content}")
    console.print(Rule())


def main():
    if not settings.google_api_key:
        console.print(
            "[bold red]❌ Error:[/bold red] GOOGLE_API_KEY is not set.\n"
            "Create a [bold].env[/bold] file from [bold].env.example[/bold] and add your key."
        )
        sys.exit(1)

    print_banner()

    session_id = None

    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n\n[dim]Goodbye! 👋[/dim]")
            break

        if not user_input:
            continue

        # Handle commands
        if user_input.lower() == "/quit":
            console.print("[dim]Goodbye! 👋[/dim]")
            break
        elif user_input.lower() == "/help":
            print_help()
            continue
        elif user_input.lower() == "/history":
            print_history(session_id)
            continue
        elif user_input.lower() == "/session":
            console.print(f"[dim]Session ID: [bold]{session_id or 'Not started yet'}[/bold][/dim]")
            continue
        elif user_input.lower() == "/clear":
            if session_id:
                memory_service.delete(session_id)
                session_id = None
            console.print("[green]✓ Conversation cleared.[/green]")
            continue

        # Stream response
        console.print(f"\n[bold green]{settings.bot_name}:[/bold green] ", end="")
        full_response = []

        try:
            for chunk, sid in ai_service.stream_sync(user_input, session_id=session_id):
                session_id = sid
                console.print(chunk, end="", highlight=False)
                full_response.append(chunk)
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}")
            logger.exception("CLI chat error")

        console.print()  # Newline after response


if __name__ == "__main__":
    main()
