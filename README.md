# Absurd Chatbot

A hilarious and absurd chatbot powered by [Groq API](https://groq.com) and Flask.

## Features

- 🤪 Completely absurd and off-topic responses
- 💬 Multi-turn conversations with memory
- ⚡ Fast responses powered by Groq's LLaMA model
- 🎨 Clean and modern UI
- 🚀 Production-ready deployment

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SelimK07/Chat-bruti.git
   cd Chat-bruti
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

5. **Run the app:**
   ```bash
   python main.py
   ```

6. **Open in browser:**
   ```
   http://localhost:5000
   ```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment guides for:
- Render.com ✅
- Heroku ✅
- Docker ✅
- DigitalOcean ✅

### Quick Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://dashboard.render.com/new?repo=https://github.com/SelimK07/Chat-bruti)

## API Endpoints

### POST `/api/chat`
Send a message to the chatbot.

**Request:**
```json
{
  "message": "What's the weather?",
  "conversation_id": "optional_id"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Pandas are learning skateboarding today!"
}
```

### POST `/api/reset`
Reset the conversation.

**Request:**
```json
{
  "conversation_id": "optional_id"
}
```

## Tech Stack

- **Backend:** Flask, Groq API, Python
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Deployment:** Docker, Gunicorn, Render/Heroku/DigitalOcean

## Environment Variables

```env
FLASK_ENV=production
FLASK_DEBUG=False
GROQ_API_KEY=your_api_key_here
CORS_ORIGINS=https://yourdomain.com
PORT=5000
```

## License

MIT License - feel free to use this project for any purpose!

## Contributing

Got ideas for more absurd responses? Fork the repo and submit a PR!

## Support

- 🐛 [Report Issues](https://github.com/SelimK07/Chat-bruti/issues)
- 💬 [Discussions](https://github.com/SelimK07/Chat-bruti/discussions)
- 📧 [Email](mailto:selim@example.com)

---

**Made with ❤️ and absurdity**
