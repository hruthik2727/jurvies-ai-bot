# 🚀 Quick Setup Guide

## All errors have been fixed! ✅

### Fixed Issues:
1. ✅ Removed duplicate message handling in AI service
2. ✅ Added proper return type annotations
3. ✅ Replaced deprecated `datetime.utcnow()` with `datetime.now(timezone.utc)`
4. ✅ Improved None handling in CLI
5. ✅ Created .env file for you

---

## 🔑 Step 1: Get Your Anthropic API Key

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to "API Keys" section
4. Click "Create Key"
5. Copy your API key

---

## 🔧 Step 2: Add Your API Key

Open the `.env` file in the `jurvies_ai_bot` folder and replace:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

with your actual API key:

```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

---

## 📦 Step 3: Install Dependencies

```bash
cd jurvies_ai_bot
pip install -r requirements.txt
```

---

## 🎮 Step 4: Run the Bot

### Option A: CLI Chat (Terminal Interface)
```bash
python cli.py
```

### Option B: Web API Server
```bash
python main.py
```
Then visit: http://localhost:8000/docs

---

## 🧪 Step 5: Test It

Once running, try:
- Type: "Hello, who are you?"
- Type: "/help" to see commands
- Type: "/quit" to exit

---

## ⚠️ Troubleshooting

**Error: "ANTHROPIC_API_KEY is not set"**
- Make sure you edited the `.env` file with your real API key
- The key should start with `sk-ant-api03-`

**Error: "Invalid Anthropic API key"**
- Double-check you copied the entire key correctly
- Make sure there are no extra spaces

**Import errors**
- Run: `pip install -r requirements.txt`

---

## 💡 Tips

- Your API key is private - never share it or commit it to git
- The `.env` file is already in `.gitignore` (if you have one)
- Free tier has rate limits - if you hit them, wait a bit and try again

---

Enjoy chatting with Jurvies! 🤖
