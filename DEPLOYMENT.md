# Production Deployment Guide

## Prerequisites
- Python 3.11+
- Groq API key ([Get it here](https://console.groq.com))
- Git (for version control)

## Local Setup

1. **Clone the repository and navigate to the project:**
   ```bash
   git clone https://github.com/SelimK07/Chat-bruti.git
   cd Chat-bruti
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file (copy from `.env.example`):**
   ```bash
   cp .env.example .env
   ```

5. **Add your Groq API key to `.env`:**
   ```
   GROQ_API_KEY=your_actual_groq_api_key
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

6. **Run locally:**
   ```bash
   python main.py
   # Or with Gunicorn:
   gunicorn --workers 1 --bind 0.0.0.0:5000 wsgi:app
   ```

## Production Deployment Options

### Option 1: Render.com (Recommended for Beginners)

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Production ready Flask app"
   git push origin main
   ```

2. **Create a new Web Service on Render:**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository and branch

3. **Configure deployment settings:**
   - **Name:** chatbot-api
   - **Environment:** Python 3
   - **Region:** Choose closest to you
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --workers 4 --bind 0.0.0.0:$PORT wsgi:app`

4. **Add environment variables in Render dashboard:**
   - `FLASK_ENV`: production
   - `GROQ_API_KEY`: your_api_key
   - `CORS_ORIGINS`: your_domain.com

### Option 2: Heroku

1. **Install Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli

2. **Login and create app:**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set GROQ_API_KEY=your_api_key
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

### Option 3: Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
EXPOSE 5000

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

Build and run:
```bash
docker build -t chatbot-api .
docker run -p 5000:5000 -e GROQ_API_KEY=your_key chatbot-api
```

### Option 4: DigitalOcean App Platform

1. Go to https://www.digitalocean.com/products/app-platform
2. Click "Create App"
3. Connect your GitHub repository
4. Configure:
   - **Build command:** `pip install -r requirements.txt`
   - **Run command:** `gunicorn --workers 4 --bind 0.0.0.0:$PORT wsgi:app`
5. Set environment variables
6. Deploy

## Security Checklist

- [x] Set `FLASK_ENV=production`
- [x] Set `FLASK_DEBUG=False`
- [x] Use strong GROQ API key (never commit to git)
- [x] Configure CORS with specific allowed origins (not `*` in production)
- [x] Enable HTTPS (automatic on Render, Heroku, etc.)
- [x] Add security headers (X-Content-Type-Options, X-Frame-Options, etc.)
- [x] Validate and sanitize user inputs
- [x] Use environment variables for all secrets
- [x] Keep dependencies updated
- [x] Monitor logs for errors

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `FLASK_ENV` | `production` | Flask environment mode |
| `FLASK_DEBUG` | `False` | Enable/disable debug mode |
| `PORT` | `5000` | Server port |
| `GROQ_API_KEY` | Required | Groq API authentication |
| `CORS_ORIGINS` | `*` | Allowed CORS origins (comma-separated) |

## Monitoring & Logging

Your application logs are automatically captured:
- **Render:** View logs in dashboard
- **Heroku:** `heroku logs --tail`
- **Docker:** `docker logs container_id`

## Performance Optimization

1. **Gunicorn Workers:**
   - Formula: `(2 × CPU cores) + 1`
   - Adjust in deployment command if needed

2. **Conversation Memory:**
   - Limited to 20 last messages to prevent memory bloat
   - Consider adding database for persistence

3. **API Rate Limiting:**
   - Consider adding rate limiting for production
   - Install: `pip install Flask-Limiter`

## Troubleshooting

**Issue: "GROQ_API_KEY not set"**
- Verify environment variable in your platform
- Check `.env` file is not committed (it's in `.gitignore`)

**Issue: Application crashes**
- Check logs in your deployment platform
- Verify all dependencies in `requirements.txt`

**Issue: CORS errors**
- Update `CORS_ORIGINS` to include your frontend domain

## Next Steps

1. Monitor application performance
2. Set up error tracking (e.g., Sentry)
3. Add database for persistent conversation history
4. Implement rate limiting and authentication
5. Add comprehensive testing

## Support

For issues, visit: https://github.com/SelimK07/Chat-bruti/issues
