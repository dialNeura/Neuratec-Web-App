# Neuratec — Robô Virtual (Sandbox)

Projeto que dá vida a um robô virtual chamado **Neuratec**. Mantém a interface original do `index.html` e adiciona funcionalidades de backend em Python (FastAPI), simulador virtual de células eletrônicas e controle via WebSocket.

> Importante: tudo é **virtual/sandbox**. Não há instruções de fabricação, implantação ou operação de hardware real que interfira em seres humanos.

## Estrutura
- `static/index.html` — frontend (UI original + controles extras).
- `app/` — backend FastAPI e simulador.
- `Dockerfile` / `docker-compose.yml` — para rodar em container.
- `tests/` — testes simples.

## Rodando localmente
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
