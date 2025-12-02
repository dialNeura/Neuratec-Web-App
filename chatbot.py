# app/chatbot.py
import asyncio

class NeuratecBot:
    """
    Orquestrador do Neuratec — interpreta comandos do usuário e delega ações
    ao simulador (modo virtual/sandbox). Mantém guardrails para recusar pedidos
    inseguros ou que peçam instruções de fabricação/implantação.
    """

    def __init__(self):
        self.name = "Neuratec"

    async def handle_message(self, text: str, simulator) -> str:
        t = (text or "").strip().lower()

        # Comandos simples de interface
        if not t:
            return "Diga algo — por exemplo: 'Simular cell_alpha 5s' ou 'Status'."

        if "hello" in t or "olá" in t or "oi" in t:
            return ("Hello. Sou o Neuratec (modo virtual). Posso simular células eletrônicas virtuais, "
                    "estimar perfis energéticos e fornecer histórico. Exemplos: 'Simular cell_alpha 5s' ou 'Status'.")

        # Recusar pedidos de instruções de construção/implantação
        sensitive_keywords = [
            "como construir", "implant", "cirurg", "inserir no cérebro",
            "soldar", "fabricação física", "passo a passo", "instrução física"
        ]
        if any(k in t for k in sensitive_keywords):
            return ("Mantenho um compromisso de segurança: não posso fornecer instruções de fabricação ou "
                    "implantação. Posso simular propriedades virtuais e dar orientações de alto nível sobre "
                    "processo regulatório e segurança.")

        # Comando: status
        if t.startswith("status") or "status" == t:
            return simulator.status_summary()

        # Comando: listar dispositivos
        if t.startswith("listar") or "listar dispositivos" in t or "list devices" in t:
            devices = simulator.list_devices()
            return "Dispositivos virtuais:\n- " + "\n- ".join(devices)

        # Comando: simular
        if "simular" in t or "simula" in t or t.startswith("simulate") or t.startswith("simulate"):
            try:
                result = simulator.run_quick_simulation(t)
                return self._format_sim_result(result)
            except Exception as e:
                return f"Erro ao executar simulação: {e}"

        # Comando: energia/perfil
        if "energia" in t or "energy" in t:
            try:
                prof = simulator.generate_energy_profile(t)
                return f"Perfil de energia:\n{prof}"
            except Exception:
                return "Não consegui gerar perfil de energia com esse comando."

        # Fallback informativo
        return ("Comandos disponíveis (exemplos):\n"
                "- 'Simular cell_alpha 5s'\n"
                "- 'Status'\n"
                "- 'Listar dispositivos'\n"
                "- 'Energia cell_alpha 10s'\n"
                "Pergunte algo ou peça uma simulação.")

    def _format_sim_result(self, result: dict) -> str:
        lines = []
        lines.append(f"Simulação: {result.get('name','quick')}")
        lines.append(f"Tempo (s): {result.get('duration_s')}")
        lines.append(f"Status: {result.get('status')}")
        metrics = result.get('metrics', {})
        if metrics:
            for k, v in metrics.items():
                lines.append(f"- {k}: {v}")
        return "\n".join(lines)
