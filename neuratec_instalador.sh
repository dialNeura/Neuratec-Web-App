#!/bin/bash
# ============================================
#  Instalador Único do Projeto "Neuratec"
#  Ele mesmo se autoriza e executa a criação.
# ============================================

# Se não estiver executável, torna-se executável
if [ ! -x "$0" ]; then
    echo "Ajustando permissões..."
    chmod +x "$0"
fi

echo "Iniciando instalação do Neuratec..."
sleep 1

# ============================================
#   CRIAÇÃO DA ESTRUTURA
# ============================================
echo "Criando pastas..."
mkdir -p neuratec
cd neuratec

# ============================================
#  index.html
# ============================================
echo "Gerando index.html..."
cat << 'EOF' > index.html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Neuratec</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="chat-container">
        <h1 class="title">Neuratec</h1>

        <div id="chat-window">
            <div class="msg bot">Olá, eu sou o Neuratec! Como posso ajudar hoje?</div>
        </div>

        <div class="input-area">
            <input type="text" id="user-input" placeholder="Digite algo..." />
            <button id="send-btn">Enviar</button>
        </div>

        <div class="status">
            <span id="status-text">Conectado</span>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
EOF

# ============================================
#  style.css
# ============================================
echo "Gerando style.css..."
cat << 'EOF' > style.css
body {
    background: #f5f6fa;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 40px;
    display: flex;
    justify-content: center;
}

.chat-container {
    width: 420px;
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
}

.title {
    text-align: center;
    margin-bottom: 20px;
}

#chat-window {
    height: 360px;
    overflow-y: auto;
    background: #fafafa;
    border: 1px solid #ddd;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 10px;
}

.msg {
    padding: 8px 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 85%;
}

.msg.bot {
    background: #dfe6e9;
}

.msg.user {
    background: #74b9ff;
    color: white;
    margin-left: auto;
}

.input-area {
    display: flex;
    gap: 10px;
}

#user-input {
    flex: 1;
    padding: 8px;
    border-radius: 8px;
    border: 1px solid #ccc;
}

#send-btn {
    padding: 8px 14px;
    border: none;
    background: #0984e3;
    color: white;
    border-radius: 8px;
    cursor: pointer;
}

#send-btn:hover {
    background: #74b9ff;
}

.status {
    margin-top: 8px;
    text-align: right;
    font-size: 12px;
    color: #555;
}
EOF

# ============================================
# script.js
# ============================================
echo "Gerando script.js..."
cat << 'EOF' > script.js
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatWindow = document.getElementById("chat-window");
const statusText = document.getElementById("status-text");

// Estado da conexão corrigido
let connected = true;

function addMessage(text, sender="bot") {
    const msg = document.createElement("div");
    msg.className = "msg " + sender;
    msg.textContent = text;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Interpretação simples
function interpretCommand(message) {
    const cmd = message.toLowerCase().trim();

    if (cmd === "ping") return "pong!";
    if (cmd === "neuro") return "Sistema neural operacional.";
    if (cmd === "status") return "Tudo funcionando perfeitamente.";

    // Quando não reconhece comando
    return "Hello.";
}

function sendMessage() {

    if (!connected) {
        addMessage("Conexão indisponível. Tentando reconectar...");
        connected = true;
        statusText.textContent = "Conectado";
        return;
    }

    const userText = input.value.trim();
    if (userText === "") return;

    addMessage(userText, "user");
    input.value = "";

    setTimeout(() => {
        addMessage(interpretCommand(userText), "bot");
    }, 250);
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
EOF

echo "============================================"
echo "Projeto Neuratec criado com sucesso!"
echo "Local: $(pwd)"
echo "============================================"
