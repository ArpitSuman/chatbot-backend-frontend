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

HF_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    payload = {
        "inputs": f"<s>[INST] {user_input} [/INST]"
    }

    try:
        response = requests.post(HF_URL, headers=headers, json=payload)

        # Try to parse JSON
        try:
            result = response.json()
        except ValueError:
            return jsonify({
                "error": "Model returned invalid JSON or timed out.",
                "raw_response": response.text,
                "status_code": response.status_code
            }), 500

        # Check for structured error
        if isinstance(result, dict) and "error" in result:
            return jsonify({"error": result["error"]}), 500

        # Extract generated text
        if isinstance(result, list) and "generated_text" in result[0]:
            reply = result[0]["generated_text"].split("[/INST]")[-1].strip()
            return jsonify({"reply": reply})

        return jsonify({
            "error": "Unexpected format in Hugging Face response.",
            "response": result
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Hugging Face Chatbot API is running!"

if __name__ == "__main__":
    app.run(debug=True)
