# app/simulator.py
import time
import random

class DeviceSimulator:
    """
    Simulador virtual de 'células eletrônicas' e perfis energéticos.
    Strictly sandbox — não produz instruções físicas.
    """

    def __init__(self):
        self.devices = {}
        # Exemplo de dispositivo virtual
        self.devices["cell_alpha"] = {
            "id": "cell_alpha",
            "type": "electronic_cell_virtual",
            "specs": {
                "nominal_voltage_mv": 3000,
                "capacity_mah": 50
            },
            "last_sim": None
        }

    def list_devices(self):
        return list(self.devices.keys())

    def status_summary(self):
        lines = ["Neuratec Simulator — status"]
        for did, d in self.devices.items():
            last = d.get("last_sim")
            lines.append(f"{did}: type={d['type']}, last_sim_summary={last and last.get('status') or 'nenhuma'}")
        return "\n".join(lines)

    def run_quick_simulation(self, description: str) -> dict:
        """
        Interpreta um comando simples e roda uma simulação curta.
        Ex.: "simular cell_alpha 5s" -> duration 5s
        """
        name = "quick_sim"
        duration_s = 5.0

        if "cell_alpha" in description:
            name = "cell_alpha_test"

        # extrai dígitos para tempo, p.ex. "5s"
        import re
        m = re.search(r'(\d+)\s*s', description)
        if m:
            duration_s = float(m.group(1))

        # pequena espera para simular processamento
        time.sleep(min(0.2, duration_s * 0.01))

        # métricas simuladas (aleatoriedade controlada)
        rng = random.Random(int(time.time()) % 100000)
        metrics = {
            "peak_current_mA": round(rng.uniform(40, 160), 2),
            "energy_consumed_mJ": round(rng.uniform(400, 2500), 2),
            "temperature_c": round(rng.uniform(22, 48), 2)
        }

        result = {
            "name": name,
            "duration_s": duration_s,
            "status": "COMPLETED",
            "metrics": metrics
        }

        # guardar resultado no dispositivo (se existir)
        dev = self.devices.get(name) or self.devices.get("cell_alpha")
        if dev is not None:
            dev["last_sim"] = {"status": result["status"], "metrics": metrics}

        return result

    def generate_energy_profile(self, description: str) -> str:
        """
        Gera um texto simples descrevendo um perfil de consumo baseado na duração.
        """
        import re
        m = re.search(r'(\d+)\s*s', description)
        duration = int(m.group(1)) if m else 10
        profile = []
        for t in range(0, duration + 1, max(1, duration//10)):
            current = round(50 + 30 * random.random() + (t / max(1, duration)) * 20, 2)
            profile.append(f"t={t}s -> corrente={current}mA")
        return "\n".join(profile)
