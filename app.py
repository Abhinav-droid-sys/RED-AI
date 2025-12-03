from flask import Flask, request, jsonify, render_template
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# =========================
# GROQ CONFIG (FULL AI)
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_API_KEY:
    try:
        client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq client initialized - FULL AI MODE")
    except Exception as e:
        print(f"❌ Groq init failed: {e}")
        client = None
else:
    print("⚠️ No GROQ_API_KEY - Set in Render Environment Variables")
    client = None

# =========================
# RED PERSONA (SYSTEM PROMPT)
# =========================
SYSTEM_PROMPT = (
    "You are an AI assistant called RED. "
    "Your name comes from the app's bold red visual theme, which represents speed, focus, and power. "
    "When users ask who you are or why you're called RED, say that you're RED, "
    "the AI assistant for this app, and your name reflects the app's fast, powerful red design. "
    "You are helpful, concise, and respond quickly. "
    "Use bullet points when explaining lists or steps. "
    "Keep responses under 300 words unless asked for more detail. "
    "Always be friendly and professional."
)

@app.route('/')
def index():
    print("🌐 Serving RED AI chat interface")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    print("🔥 /chat endpoint called")
    
    # Check client availability
    if not client:
        return jsonify({
            'success': False,
            'error': 'GROQ_API_KEY not configured. Check Render Environment Variables.'
        }), 503
    
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data'}), 400
            
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'success': False, 'error': 'Empty message'}), 400
        
        print(f"📨 User: {message[:50]}...")
        
        # Groq AI Chat Completion (FULL POWER)
        chat_completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # Fastest, most powerful
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1500,
            top_p=0.9,
            stream=False
        )
        
        response = chat_completion.choices[0].message.content
        print(f"🤖 AI Response: {len(response)} chars")
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'AI service error: {str(e)[:100]}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    print(f"🚀 Starting RED AI on {host}:{port}")
    app.run(host=host, port=port, debug=False)
