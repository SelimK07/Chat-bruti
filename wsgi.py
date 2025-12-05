"""
WSGI entry point for production deployment.
Use this with Gunicorn: gunicorn --workers 4 --worker-class sync --bind 0.0.0.0:$PORT wsgi:app
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from main import app

if __name__ == "__main__":
    app.run()
