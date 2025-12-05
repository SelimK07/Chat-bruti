# Quick Reference Card 📋

## 🚀 5-Minute Deploy Checklist

### ✅ Pre-Deploy
- [ ] Have your GROQ_API_KEY ready
- [ ] Choose deployment platform
- [ ] Set `CORS_ORIGINS` to your domain

### ✅ Local Setup (2 min)
```bash
cp .env.example .env
# Edit .env and add GROQ_API_KEY
FLASK_ENV=production python main.py
# Test at http://localhost:5000
```

### ✅ Deployment (3 min)
**Choose ONE:**

#### Option A: Render.com (Easiest)
```
1. https://dashboard.render.com
2. "New Web Service" → Select repo
3. Set environment variables
4. Deploy (automatic on push)
```

#### Option B: Heroku  
```bash
heroku create my-app
heroku config:set GROQ_API_KEY=KEY
git push heroku main
```

#### Option C: Docker
```bash
docker-compose up --build
```

---

## 🔑 Key Commands

```bash
# Local development
python main.py

# Local testing (production mode)
FLASK_ENV=production python main.py

# With Gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app

# Docker
docker-compose up
docker-compose up --build
docker-compose down

# Tests
pytest test_main.py -v
pytest test_main.py --cov=.

# GitHub (after changes)
git add .
git commit -m "Your message"
git push origin main
```

---

## 🌍 Environment Variables

| Variable | Example | Required |
|----------|---------|----------|
| GROQ_API_KEY | gsk_xxx | YES |
| FLASK_ENV | production | No (default: production) |
| FLASK_DEBUG | False | No (default: False) |
| CORS_ORIGINS | domain.com | No (default: *) |
| PORT | 5000 | No (default: 5000) |

---

## 📱 Testing Your Deployment

```bash
# Is it running?
curl http://your-app-url

# Send a message
curl -X POST http://your-app-url/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","conversation_id":"test"}'

# Reset conversation
curl -X POST http://your-app-url/api/reset \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":"test"}'
```

---

## 📚 Documentation Guide

| File | Purpose |
|------|---------|
| `GETTING_STARTED.md` | **Start here** |
| `DEPLOYMENT.md` | Platform-specific guides |
| `PRODUCTION_CHECKLIST.md` | Detailed checklist |
| `PRODUCTION_SUMMARY.md` | Complete overview |
| `README.md` | Project overview |

---

## ⚠️ Critical Before Launch

1. **GROQ_API_KEY set?** ✓
2. **FLASK_ENV=production?** ✓
3. **FLASK_DEBUG=False?** ✓
4. **CORS_ORIGINS updated?** ✓
5. **Tested locally?** ✓
6. **Committed to git?** ✓

---

## 🆘 Emergency Fixes

**App won't start:**
```bash
# Check logs
FLASK_ENV=production python main.py

# Missing package?
pip install -r requirements.txt
```

**CORS error:**
- Add your domain to `CORS_ORIGINS`

**API key error:**
- Set `GROQ_API_KEY` env variable

**Memory issues:**
- Already fixed! (20 message limit)

---

## 📞 Need Help?

1. Check `DEPLOYMENT.md` for your platform
2. Review logs on deployment platform
3. Test locally first
4. Verify all env variables

---

## ✨ You're Ready!

All files are in place. Time to deploy! 🚀

Start with: `GETTING_STARTED.md`
