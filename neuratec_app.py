# neuratec_app.py — versão corrigida para ambientes sandbox e produção

from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# -------------------------------------------------------------
# Página HTML simples só para validar que o app está vivo
# -------------------------------------------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <title>Neuratec WebChat</title>
</head>
<body>
    <h1>Neuratec WebChat</h1>
    <p>Interface carregada com sucesso.</p>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

# -------------------------------------------------------------
# Endpoint de chat
# -------------------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")

    # Resposta simples apenas para validar o funcionamento
    return jsonify({
        "response": f"Você disse: {msg}"
    })

# -------------------------------------------------------------
# WSGI (Gunicorn / Production)
# -------------------------------------------------------------
# A variável abaixo é usada por servidores como Gunicorn
application = app

# -------------------------------------------------------------
# Execução LOCAL opcional (desativada em sandbox)
# -------------------------------------------------------------
if __name__ == "__main__":
    # Em ambientes sandbox, app.run() causa SystemExit.
    # Porém, localmente, o dev pode ativar definindo a variável:
    if os.environ.get("NEURATEC_LOCAL", "0") == "1":
        app.run(host="127.0.0.1", port=5000, debug=True)
    else:
        print("[INFO] Ambiente sandbox detectado: execução local desativada.")
