import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from mistralai.client import Mistral
from scout import get_global_trends, get_filtered_trends

load_dotenv()
app = Flask(__name__)

# Initialize Mistral with the new SDK pattern
api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

def generate_strategy(trend, intent):
    """Generates a viral strategy using Mistral AI."""
    prompt = f"""
    The user is interested in the trend: '{trend}'.
    Their intent is: {intent}.
    
    Provide a viral 3-step strategy to maximize this trend:
    1. Content Hook (X/LinkedIn) - Give an exact opening line.
    2. Strategic Action - What specific asset should they create?
    3. Monetization/Growth Hack - How do they turn this into revenue or leads?
    
    Keep advice punchy, bold, and actionable.
    """
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Strategy is temporarily offline, but keep an eye on: {trend}!"

@app.route('/')
def home():
    # Fetch global trends for the sidebar/header
    global_trends = get_global_trends()
    return render_template('index.html', global_trends=global_trends)

@app.route('/scout')
def scout():
    # 1. Get user inputs
    topic = request.args.get('topic', 'AI')
    geo = request.args.get('geo', '')
    intent = request.args.get('intent', 'Thought Leadership')
    timeframe = request.args.get('timeframe', 'now 7-d')

    # 2. Get Trend Data (with fallback handling inside scout.py)
    trend_data = get_filtered_trends(topic, geo, timeframe)
    
    # 3. Generate AI Strategy based on the found (or fallback) trend
    advice = generate_strategy(trend_data['topic'], intent)
    
    return jsonify({
        "trend": trend_data['topic'],
        "growth": trend_data['growth'],
        "advice": advice
    })

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
