from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Allow frontend requests

# API Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are RED, a fast AI assistant. Be helpful, concise, friendly. Use bullets for lists."""

@app.route('/')
def index():
    print("🌐 Frontend served")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    print("🔥 CHAT HIT!")
    
    if not GROQ_API_KEY:
        return jsonify({'success': False, 'error': 'API Key missing'})
    
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'success': False, 'error': 'No message'})
    
    print(f"📨 {message[:50]}...")
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        print(f"🤖 {len(ai_response)} chars")
        return jsonify({'success': True, 'response': ai_response})
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return jsonify({'success': False, 'error': 'AI service unavailable'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'success': False, 'error': 'Processing error'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
