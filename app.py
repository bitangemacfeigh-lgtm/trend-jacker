import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from mistralai.client import Mistral
from scout import get_global_trends, get_filtered_trends

load_dotenv()
app = Flask(__name__)
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def generate_strategy(trend, intent):
    prompt = f"""
    The user is interested in the trend: '{trend}'.
    Their intent is: {intent}.
    
    Provide a viral 3-step strategy to maximize this trend:
    1. Content Hook (X/LinkedIn)
    2. Strategic Action (What should they actually do/build?)
    3. Monetization/Growth Hack (How do they profit from this?)
    
    Keep the advice punchy and actionable.
    """
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.route('/')
def home():
    # Show global trends on the landing page
    global_trends = get_global_trends()
    return render_template('index.html', global_trends=global_trends)

@app.route('/scout')
def scout():
    # Get parameters from the frontend form
    topic = request.args.get('topic', 'AI')
    geo = request.args.get('geo', '')
    intent = request.args.get('intent', 'Brand Awareness')
    timeframe = request.args.get('timeframe', 'now 1-d')

    trend_data = get_filtered_trends(topic, geo, timeframe)
    advice = generate_strategy(trend_data['topic'], intent)
    
    return jsonify({
        "trend": trend_data['topic'],
        "growth": trend_data['growth'],
        "advice": advice
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))