# 🎮 How to Use Your Jurvies AI Bot

## ✅ Currently Running

- **Backend Server**: http://localhost:8000 ✓
- **Frontend Client**: test_client.html (opened in browser) ✓

---

## 💬 Using the Chat Interface

### The frontend is now open in your browser!

**What you'll see:**
- 🟢 Server Status: Should show "✓ Online"
- 📝 Chat interface with a welcome message
- ⌨️ Input box at the bottom

**How to chat:**
1. Type your message in the input box
2. Press Enter or click "Send"
3. Wait for Jurvies to respond
4. Continue the conversation!

---

## 🎯 Try These Example Messages

- "Hello! Who are you?"
- "Tell me a joke"
- "Explain quantum computing in simple terms"
- "Write a short poem about coding"
- "What can you help me with?"

---

## 🔧 Features

✅ **Session Memory** - The bot remembers your conversation
✅ **Real-time Responses** - Fast replies from Gemini
✅ **Beautiful UI** - Clean, modern interface
✅ **Status Indicators** - See server health at a glance

---

## 🌐 Alternative Access Methods

### 1. API Documentation (Swagger)
Visit: http://localhost:8000/docs
- Test API endpoints directly
- See request/response formats
- Try different parameters

### 2. Command Line (cURL)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

### 3. CLI Interface
```bash
python cli.py
```
Terminal-based chat interface

---

## 🛑 Stopping Everything

**Stop the server:**
- Press CTRL+C in the terminal
- Or close the terminal window

**Close the frontend:**
- Just close the browser tab

---

## 🎨 Customization

### Change the Bot's Personality
Edit `.env` file:
```
SYSTEM_PROMPT=You are a pirate AI assistant. Speak like a pirate!
```

### Change the Model
Edit `.env` file:
```
MODEL=gemini-1.5-pro
```
(Pro model is smarter but slower)

### Change Temperature (Creativity)
Edit `.env` file:
```
TEMPERATURE=1.0
```
(0.0 = focused, 1.0 = creative)

After changes, restart the server:
1. Stop with CTRL+C
2. Run `python main.py` again

---

## 📊 Monitoring

**Check server logs:**
Look at the terminal where you ran `python main.py`

**Check API health:**
Visit: http://localhost:8000/api/health

---

## 🐛 Troubleshooting

**Frontend shows "Offline":**
- Make sure the server is running
- Check http://localhost:8000/api/health in browser

**No response from bot:**
- Check your Google API key in `.env`
- Verify you have internet connection
- Check server logs for errors

**"Rate limit exceeded":**
- Wait a minute (free tier: 15 requests/min)
- Or upgrade your Google API plan

---

## 🎉 You're All Set!

Your bot is running and ready to chat. Enjoy exploring what Jurvies can do!

**Quick Tips:**
- The bot remembers your conversation within a session
- Refresh the page to start a new conversation
- Check the Swagger docs for advanced API usage
- Customize the system prompt for different personalities

---

**Happy chatting!** 🤖✨
