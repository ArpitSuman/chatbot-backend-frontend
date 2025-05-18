from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session
CORS(app)

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

HF_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

def build_prompt(history):
    system_prompt = "You are a helpful assistant."

    formatted = f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n"

    for turn in history:
        if turn["role"] == "user":
            formatted += f"{turn['content']} [/INST]\n"
        elif turn["role"] == "assistant":
            formatted += f"{turn['content']} </s><s>[INST] "

    return formatted.strip()

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.get_json().get("message")

    # Load or initialize chat history
    if "history" not in session:
        session["history"] = []

    # Add the new user message
    session["history"].append({"role": "user", "content": user_input})

    # Build prompt from history
    prompt = build_prompt(session["history"])

    payload = { "inputs": prompt }

    try:
        if len(prompt) > 4000:
            return jsonify({"error": "Prompt too long, please reset the chat."}), 400

        response = requests.post(HF_URL, headers=headers, json=payload, timeout=60)
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            full_output = result[0]["generated_text"]
            reply = full_output.split("[/INST]")[-1].strip()

            # Save assistant reply to session history
            session["history"].append({"role": "assistant", "content": reply})
            session.modified = True

            return jsonify({ "reply": reply })

        return jsonify({ "error": "Unexpected response", "details": result }), 500

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

@app.route("/reset", methods=["POST"])
def reset():
    session.pop("history", None)
    return jsonify({ "message": "Chat history cleared." })

@app.route("/")
def home():
    return "Zephyr Chatbot is running!"

if __name__ == "__main__":
    app.run(debug=True)
