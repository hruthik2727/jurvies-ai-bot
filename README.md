# 🤖 Jurvies AI Bot

A fully structured, production-ready AI chatbot built with Python, FastAPI, and Google Gemini.

**New Personality**: Clear answers • Step-by-step guides • Friendly help 😊

## 📁 Project Structure

```
jurvies_ai_bot/
├── app/
│   ├── api/            # FastAPI route handlers
│   ├── core/           # Core config & dependencies
│   ├── models/         # Pydantic data models
│   ├── services/       # Business logic (AI, memory)
│   └── utils/          # Helpers (logging, formatting)
├── tests/              # Unit & integration tests
├── logs/               # Auto-generated log files
├── config/             # YAML config files
├── main.py             # App entry point
├── cli.py              # Terminal chatbot interface
├── requirements.txt
└── .env.example
```

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

Get your free API key at: https://aistudio.google.com/app/apikey

### 3. Run the Web API
```bash
python main.py
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 4. Run the CLI Bot
```bash
python cli.py
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send a message, get a response |
| POST | `/api/chat/stream` | Streaming chat response |
| GET | `/api/sessions/{id}` | Get conversation history |
| DELETE | `/api/sessions/{id}` | Clear a session |
| GET | `/api/health` | Health check |

## ⚙️ Configuration

Edit `config/settings.yaml` or use environment variables:

- `GOOGLE_API_KEY` — Your Google Gemini API key
- `MODEL` — Gemini model (default: `gemini-1.5-flash`)
- `MAX_TOKENS` — Max response tokens (default: 1024)
- `SYSTEM_PROMPT` — Bot personality/instructions

## 🧪 Run Tests
```bash
pytest tests/ -v
```

## 🆓 Free Tier

Google Gemini offers a generous free tier:
- 15 requests per minute
- 1 million tokens per minute
- Perfect for development and small projects!
