import os
import time
from flask import Flask, jsonify
from dotenv import load_dotenv
from mistralai.client import Mistral
from scout import get_google_trends

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Mistral
api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

def generate_viral_content(topic, growth):
    prompt = f"""
    A new trend just broke out: '{topic}' with a growth metric of {growth}.
    Target Audience: Brand Founders and Tech Enthusiasts.
    
    1. Write a 5-part X (Twitter) thread. Start with a hook that mentions the sudden spike.
    2. Write a LinkedIn 'Thought Leadership' post that explains the 'Why' behind this trend.
    
    Keep it punchy, use emojis sparingly, and ensure it sounds human.
    """
    
    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_response.choices[0].message.content

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scout')
def scout():
    NICHE = "AI in Kenya"
    trend = get_google_trends(NICHE)
    
    if trend:
        content = generate_viral_content(trend['topic'], trend['growth'])
        return jsonify({
            "status": "success",
            "trend_found": trend['topic'],
            "growth": trend['growth'],
            "content": content
        })
    
    return jsonify({"status": "idle", "message": "No spikes detected right now."})

if __name__ == "__main__":
    # For local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)