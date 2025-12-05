#!/bin/bash
# Quick production deployment script
# Usage: bash deploy.sh render (or heroku, docker)

set -e

PLATFORM=${1:-render}

echo "🚀 Starting production deployment to $PLATFORM..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Production ready Flask chatbot"
fi

# Verify .env.example exists
if [ ! -f ".env.example" ]; then
    echo "❌ .env.example not found!"
    exit 1
fi

echo "✅ Git repository ready"

case $PLATFORM in
  render)
    echo ""
    echo "📋 Deploying to Render.com"
    echo ""
    echo "1. Go to https://dashboard.render.com"
    echo "2. Click 'New +' → 'Web Service'"
    echo "3. Connect your GitHub repository"
    echo "4. Use these settings:"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: gunicorn --workers 4 --bind 0.0.0.0:\$PORT wsgi:app"
    echo ""
    echo "5. Add Environment Variables:"
    echo "   - FLASK_ENV: production"
    echo "   - GROQ_API_KEY: your_key_here"
    echo ""
    ;;
    
  heroku)
    echo ""
    echo "📋 Deploying to Heroku"
    echo ""
    echo "Make sure you have Heroku CLI installed:"
    echo "1. heroku login"
    echo "2. heroku create your-app-name"
    echo "3. heroku config:set FLASK_ENV=production"
    echo "4. heroku config:set GROQ_API_KEY=your_key_here"
    echo "5. git push heroku main"
    echo ""
    ;;
    
  docker)
    echo ""
    echo "🐳 Deploying with Docker"
    echo ""
    echo "Build and run locally:"
    echo "1. docker-compose up --build"
    echo ""
    echo "Or run without docker-compose:"
    echo "1. docker build -t chatbot-api ."
    echo "2. docker run -p 5000:5000 -e GROQ_API_KEY=your_key chatbot-api"
    echo ""
    ;;
    
  *)
    echo "Unknown platform: $PLATFORM"
    echo "Usage: bash deploy.sh [render|heroku|docker]"
    exit 1
    ;;
esac

echo "📚 For more details, see DEPLOYMENT.md"
echo ""
echo "✨ Your app is production-ready!"
