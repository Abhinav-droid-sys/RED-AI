from flask import Flask, request, jsonify, render_template
import os
import requests
import random

app = Flask(__name__, static_folder='static', template_folder='templates')

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are RED AI. Fast, helpful, friendly. Use bullets for lists. Keep concise."""

@app.route('/')
def index():
    print("🌐 Chat UI served")
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    print("🔥 /api/chat HIT!")
    data = request.json or {}
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'success': True, 'response': 'Type a message to chat!'})
    
    print(f"📨 User: {message[:50]}...")
    
    # If no API key, use demo responses
    if not GROQ_API_KEY:
        responses = [
            f"🚀 RED LIVE! You said: '{message[:50]}'",
            "✅ Backend perfect! Add GROQ_API_KEY for real AI!",
            f"💬 Working! Message: '{message[:30]}...'"
        ]
        return jsonify({'success': True, 'response': random.choice(responses)})
    
    # REAL GROQ AI
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
        ai_reply = result['choices'][0]['message']['content']
        
        print(f"🤖 AI: {len(ai_reply)} chars")
        return jsonify({'success': True, 'response': ai_reply})
        
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return jsonify({'success': True, 'response': f"🤖 RED: AI temp unavailable. You said: '{message[:50]}'"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 FULL RED AI live on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
