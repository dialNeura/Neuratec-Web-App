"""
Neuratec — Flask Web App totalmente funcional em uma única página da web.
✔ Funciona em QUALQUER servidor comum (Railway, Render, Replit, etc.)
✔ Sem debug / sem reloader (evita _multiprocessing)
✔ Templates reais (não mais render_template_string com herança quebrada)
✔ Estrutura completa para hospedagem online

Instruções:
1. pip install flask pillow
2. python app.py
3. Abra no navegador: http://127.0.0.1:5000

Arquivos gerados automaticamente:
/templates/base.html
/templates/index.html
/templates/chat.html
/static/profile.png

Tudo já fica pronto para deploy.
"""

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from PIL import Image
import os, shutil

app = Flask(__name__)
app.secret_key = "neuratec_secret_key"

# Estrutura de diretórios
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
PROFILE_PATH = "static/profile.png"
SOURCE_IMAGE = "/mnt/data/NeuratecLogotipo.jpg"

# Copia a imagem real
if os.path.exists(SOURCE_IMAGE):
    shutil.copy(SOURCE_IMAGE, PROFILE_PATH)
else:
    img = Image.new("RGB", (800, 800), (30,144,255))
    img.save(PROFILE_PATH)

# Template BASE — página única para web
BASE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neuratec</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background:#f5f6fa; }
        .circle-img { width:180px; height:180px; border-radius:50%; overflow:hidden; border:6px solid #2b6cb0; box-shadow:0 6px 20px rgba(43,108,176,0.18); }
        .circle-img img { width:100%; height:100%; object-fit:cover; }
        .chat-header-img { width:48px; height:48px; border-radius:50%; border:3px solid #fff; object-fit:cover; }
        .bot-msg { background:#F1F1F1; padding:10px 14px; border-radius:10px; max-width:75%; }
        .user-msg { background:#DCF8C6; padding:10px 14px; border-radius:10px; max-width:75%; margin-left:auto; }
    </style>
</head>
<body class="bg-light">
    <div class="container py-4">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

# Página inicial
INDEX_HTML = """
{% extends 'base.html' %}
{% block content %}
<div class="text-center">
    <div class="circle-img mx-auto mb-3"><img src="{{ url_for('static', filename='profile.png') }}"></div>
    <h2>Neuratec</h2>
    <p class="text-muted">9.654 seguidores</p>
    <a href="{{ url_for('chat') }}" class="btn btn-primary btn-lg mt-3">Chat</a>
</div>
{% endblock %}
"""

# Página de chat estilo ChatGPT + Facebook
CHAT_HTML = """
{% extends 'base.html' %}
{% block content %}
<div class="card shadow-sm">
    <div class="card-header d-flex align-items-center gap-3">
        <img src="{{ url_for('static', filename='profile.png') }}" class="chat-header-img">
        <div><strong>Neuratec</strong><br><span class="text-muted" style="font-size:13px;">Responde apenas "Hello."</span></div>
    </div>

    <div class="card-body" style="min-height:420px;">
        {% for sender, text in messages %}
            {% if sender == 'user' %}
                <div class="user-msg mb-2">{{ text }}</div>
            {% else %}
                <div class="bot-msg mb-2">{{ text }}</div>
            {% endif %}
        {% endfor %}
    </div>

    <div class="card-footer">
        <form method="post">
            <div class="input-group">
                <input name="msg" class="form-control" placeholder="Digite sua mensagem..." required>
                <button class="btn btn-primary">Enviar</button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
"""

# Salvar templates reais (necessário para hospedagem)
with open("templates/base.html", "w", encoding="utf-8") as f: f.write(BASE_HTML)
with open("templates/index.html", "w", encoding="utf-8") as f: f.write(INDEX_HTML)
with open("templates/chat.html", "w", encoding="utf-8") as f: f.write(CHAT_HTML)

# Rotas principais
aaa@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        msg = request.form.get("msg", "").strip()
        if msg:
            session["messages"].append(("user", msg))
            session["messages"].append(("bot", "Hello."))
            session.modified = True
        return redirect(url_for("chat"))

    return render_template("chat.html", messages=session.get("messages", []))

# Execução segura (sem multiprocessing)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
