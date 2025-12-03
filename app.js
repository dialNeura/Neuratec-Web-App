function appendMessage(sender, text) {
    const box = document.getElementById('messages');
    const div = document.createElement('div');

    if (sender === "user") {
        div.className = "user-msg mb-2";
        div.textContent = text;

    } else {
        div.className = "d-flex align-items-start mb-2";
        div.innerHTML =
            "<img src='NeuratecLogotipo.jpg' style='width:32px;height:32px;border-radius:50%;margin-right:8px;'>" +
            "<div class='bot-msg'>" + text + "</div>";
    }

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;

    saveMessages();
}

function saveMessages() {
    localStorage.setItem("neuratec_chat", document.getElementById("messages").innerHTML);
}

function loadMessages() {
    const saved = localStorage.getItem("neuratec_chat");
    if (saved) {
        document.getElementById("messages").innerHTML = saved;
    }
}

function toggleChat() {
    const box = document.getElementById("chatBox");

    if (box.style.display === "none") {
        box.style.display = "block";
        window.scrollTo(0, document.body.scrollHeight);
    } else {
        box.style.display = "none";
    }
}

async function sendMsg() {
    const input = document.getElementById("msgInput");
    const text = input.value.trim();
    if (!text) return;

    appendMessage("user", text);
    input.value = "";

    try {
        const res = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        if (!res.ok) {
            appendMessage("bot", "Conexão indisponível. Tentando reconectar…");
            return;
        }

        const data = await res.json();
        appendMessage("bot", data.reply || "Hello.");
    } 
    catch (e) {
        appendMessage("bot", "Conexão indisponível. Tentando reconectar…");
    }
}

loadMessages();
