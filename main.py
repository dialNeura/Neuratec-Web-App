# app/main.py
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .chatbot import NeuratecBot
from .db import init_db, SessionLocal
from .models import Message
from .simulator import DeviceSimulator

app = FastAPI(title="Neuratec Virtual")

# Servir conteúdo estático (frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# CORS - ajustar em produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# inicializar DB e componentes
init_db()
bot = NeuratecBot()
simulator = DeviceSimulator()

async def send_json(ws: WebSocket, payload: dict):
    await ws.send_text(json.dumps(payload, default=str))

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            data = json.loads(raw)
            if data.get("type") == "message":
                user_text = data.get("text", "")
                # salva no banco
                try:
                    with SessionLocal() as db:
                        m = Message(role="user", text=user_text)
                        db.add(m); db.commit()
                except Exception:
                    # não interrompe a experiência se DB falhar
                    pass

                # indica typing
                await send_json(ws, {"type": "typing", "text": "Neuratec processando..."})

                # processa mensagem (pode chamar o simulador)
                reply = await bot.handle_message(user_text, simulator=simulator)

                # salva resposta no DB
                try:
                    with SessionLocal() as db:
                        m = Message(role="bot", text=reply)
                        db.add(m); db.commit()
                except Exception:
                    pass

                # envia resposta final
                await send_json(ws, {"sender": "bot", "text": reply})
    except WebSocketDisconnect:
        # cliente desconectou
        return
    except Exception as e:
        try:
            await send_json(ws, {"sender": "bot", "text": f"Erro interno: {e}"})
        except:
            pass

