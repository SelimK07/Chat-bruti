import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize client only if API key is available
api_key = os.environ.get("GROQ_API_KEY")
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
            return jsonify({"success": False, "error": "GROQ_API_KEY environment variable not set"}), 500
        
        data = request.get_json()
        user_message = data['message']
        conversation_id = data.get('conversation_id', 'default')
        
        if conversation_id not in conversations:
            conversations[conversation_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        conversations[conversation_id].append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversations[conversation_id],
            temperature=1.2,
            max_tokens=300
        )
        
        bot_message = response.choices[0].message.content
        conversations[conversation_id].append({"role": "assistant", "content": bot_message})
        
        return jsonify({"success": True, "message": bot_message})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    data = request.get_json()
    conversation_id = data.get('conversation_id', 'default') if data else 'default'
    conversations[conversation_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
