from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

HF_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    payload = {
        "inputs": f"<s>[INST] {user_input} [/INST]"
    }

    try:
        response = requests.post(HF_URL, headers=headers, json=payload)
        result = response.json()

        # Extract response text
        if isinstance(result, list) and "generated_text" in result[0]:
            return jsonify({"reply": result[0]["generated_text"].split("[/INST]")[-1].strip()})
        else:
            return jsonify({"error": "Invalid response from model", "details": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Hugging Face Chatbot API is running!"

if __name__ == "__main__":
    app.run(debug=True)
