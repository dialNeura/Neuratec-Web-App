from flask import Flask, request, jsonify
import psutil

app = Flask(__name__)

@app.post("/api")
def api():
    data = request.get_json()
    msg = data.get("message", "").lower()

    if msg == "/cpu":
        return jsonify(reply=f"CPU: {psutil.cpu_percent()}%")

    if msg == "/memoria":
        mem = psutil.virtual_memory()
        return jsonify(reply=f"Memória: {mem.percent}% usada")

    if msg == "/rede":
        return jsonify(reply="Rede ativa.")

    if msg == "/ping":
        return jsonify(reply="pong!")

    if msg == "/limpar":
        return jsonify(reply="Chat limpo (visualmente).")

    # Padrão quando não existe comando
    return jsonify(reply="Hello.")

app.run(host="0.0.0.0", port=5000)
