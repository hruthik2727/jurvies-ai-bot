# 🚀 Google Gemini Setup Guide

## ✅ Project Converted to Google Gemini!

Your bot now uses Google Gemini API instead of Anthropic Claude.

---

## 🔑 Step 1: Get Your Google API Key (FREE!)

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (starts with `AIza...`)

**Good news:** Google Gemini has a generous FREE tier!
- 15 requests per minute
- 1 million tokens per minute
- No credit card required!

---

## 🔧 Step 2: Add Your API Key

Open the `.env` file and replace:

```
GOOGLE_API_KEY=your_google_api_key_here
```

with your actual API key:

```
GOOGLE_API_KEY=AIzaSyD...your-actual-key
```

---

## 📦 Step 3: Install Dependencies

```bash
cd jurvies_ai_bot
pip install -r requirements.txt
```

This will install `google-generativeai` and other required packages.

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
- Type: "Hello! Tell me a joke."
- Type: "/help" to see commands
- Type: "/quit" to exit

---

## 🎯 Available Models

You can change the model in `.env`:

- `gemini-1.5-flash` (default) - Fast and efficient
- `gemini-1.5-pro` - More capable, slower
- `gemini-1.0-pro` - Older version

---

## ⚠️ Troubleshooting

**Error: "GOOGLE_API_KEY is not set"**
- Make sure you edited the `.env` file with your real API key
- The key should start with `AIza`

**Error: "Invalid API key"**
- Double-check you copied the entire key correctly
- Make sure there are no extra spaces
- Verify the key is active at https://aistudio.google.com/app/apikey

**Import errors**
- Run: `pip install -r requirements.txt`

---

## 💡 Why Google Gemini?

✅ **FREE tier** - No credit card needed
✅ **Fast** - Quick response times
✅ **Generous limits** - 15 RPM, 1M tokens/min
✅ **Easy setup** - Get started in minutes
✅ **Reliable** - Backed by Google infrastructure

---

## 📊 Rate Limits (Free Tier)

- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per minute

Perfect for development and personal projects!

---

Enjoy chatting with Jurvies powered by Google Gemini! 🤖✨
