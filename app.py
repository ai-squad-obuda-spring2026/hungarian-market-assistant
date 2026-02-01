# app.py
from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    """Render the homepage"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with DeepSeek API"""
    try:
        # Get user message
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Call DeepSeek API
        api_response = call_deepseek_api(user_message)
        
        # Extract the AI response
        ai_message = api_response.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
        
        return jsonify({
            'success': True,
            'response': ai_message
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def call_deepseek_api(prompt):
    """Call DeepSeek API with the user's prompt"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key:
        raise ValueError("API key not found. Check your .env file")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # System message for Hungarian market expertise
    system_message = """You are a Hungarian Market Assistant. You help with:
    1. Hungarian market trends and analysis
    2. Competitor research in Hungary
    3. Hungarian consumer behavior insights
    4. Business regulations in Hungary
    5. Local market entry strategies
    Provide detailed, helpful responses in English."""
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000
    }
    
    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers=headers,
        json=data
    )
    
    # Check for errors
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    return response.json()

@app.route('/test')
def test():
    """Simple test endpoint"""
    return "Flask server is working! 🚀"

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
