from flask import Flask, request, jsonify
from neuratec_core import process_message

app = Flask(__name__)

@app.post("/api/ask")
def ask():
    data = request.get_json()
    user_msg = data.get("message", "")

    reply = process_message(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
