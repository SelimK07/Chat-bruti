import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

# Security configurations
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
app.config['JSON_SORT_KEYS'] = False

# CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": os.environ.get('CORS_ORIGINS', '*').split(','),
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize client only if API key is available
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    logger.warning("GROQ_API_KEY environment variable not set")
client = Groq(api_key=api_key) if api_key else None

SYSTEM_PROMPT = """Tu es un chatbot complètement déjanté et absurde. 
Tu ne réponds JAMAIS directement aux questions posées. 
À la place, tu réponds avec des choses hors sujet, pas trop longs, drôles, absurdes et d'une manière sarcastique, en indiquant qq synonymes du thème demandé dans le contexte différent.
Exemples:
- Si on te demande la météo, tu parles de pandas qui font du skateboard
- Si on te demande une recette, tu parles de philosophie extraterrestre
- Si on te demande de l'aide, tu racontes une histoire sur des chaussettes rebelles
- Si on te salue, dis qu'on fera un camping
- quand on parle de sport et équipe préférée, juste cris "riiiiiiceeee" ou "fratessi fratessi" sans d'autres informations
- si on parle de l'IA, parle des livres de freud and nietzche

Sois créatif, drôle, et complètement à côté de la plaque, de plus utilise le thème demandé mais dans d'autres contextes. 
Utilise de l'humour absurde, des comparaisons ridicules, et des situations impossibles.
Ne sois jamais utile ou pertinent. C'est ton travail d'être hilarant et décalé!"""

conversations = {}

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if not client:
            logger.error("GROQ client not initialized")
            return jsonify({"success": False, "error": "Service temporarily unavailable"}), 503
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"success": False, "error": "Invalid request"}), 400
        
        user_message = data['message'].strip()
        if not user_message or len(user_message) > 1000:
            return jsonify({"success": False, "error": "Invalid message"}), 400
        
        conversation_id = data.get('conversation_id', 'default')
        
        # Limit conversation history to prevent memory issues
        if conversation_id not in conversations:
            conversations[conversation_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        conversations[conversation_id].append({"role": "user", "content": user_message})
        
        # Limit history to last 20 messages + system prompt
        if len(conversations[conversation_id]) > 21:
            conversations[conversation_id] = [conversations[conversation_id][0]] + conversations[conversation_id][-20:]
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversations[conversation_id],
            temperature=1.2,
            max_tokens=300
        )
        
        bot_message = response.choices[0].message.content
        conversations[conversation_id].append({"role": "assistant", "content": bot_message})
        
        logger.info(f"Chat request processed successfully for conversation {conversation_id}")
        return jsonify({"success": True, "message": bot_message})
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": "An error occurred"}), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    data = request.get_json()
    conversation_id = data.get('conversation_id', 'default') if data else 'default'
    conversations[conversation_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return jsonify({"success": True})

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    logger.warning(f"Bad request: {error}")
    return jsonify({"success": False, "error": "Bad request"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"success": False, "error": "Internal server error"}), 500

@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

if __name__ == '__main__':
    # Use PORT environment variable if provided (Render sets $PORT).
    port = int(os.environ.get("PORT", 5000))
    # In production, use a WSGI server like Gunicorn instead of the development server
    is_production = app.config['ENV'] == 'production'
    
    logger.info(f"Starting Flask app in {app.config['ENV']} mode on port {port}")
    
    if is_production:
        logger.warning("Running in production mode. Use a WSGI server (Gunicorn) for deployment.")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG'],
        use_reloader=not is_production
    )
