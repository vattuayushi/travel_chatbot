import os
import re
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    itinerary_match = re.search(r'(\d+)[-\s]?day', user_message.lower())
    is_itinerary = bool(itinerary_match)
    days = int(itinerary_match.group(1)) if is_itinerary else 0

    if is_itinerary:
        system_prompt = (
            f"You are a smart travel assistant. The user asked for a {days}-day travel itinerary. "
            f"Reply with exactly {days} day(s). Start each day with '🗓️ Day X:' and include 3-5 short, emoji-rich bullet points per day. "
            f"Use line breaks between each activity."
        )
    else:
        system_prompt = (
            "You are a helpful travel assistant. Reply briefly and clearly to any travel-related question, "
            "like best destinations, food, budget tips, visa info, etc. Use bullet points or short paragraphs. Use emojis where helpful."
        )

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return jsonify({"reply": "⚠️ API key not set. Please check your environment variables."}), 500

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"reply": f"❌ Failed to fetch response: {str(e)}"}), 500

    return jsonify({"reply": reply})


if __name__ == '__main__':
    app.run(debug=True)
