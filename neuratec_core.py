import re

def process_message(msg: str) -> str:

    # comandos especiais do "robô"
    if re.search(r"\benergia\b", msg, re.I):
        return "O núcleo energético Neuratec está ativo e estabilizando o fluxo."

    if re.search(r"\bcelula\b|\bchip\b|\bmódulo\b", msg, re.I):
        return "O módulo de manufatura neural está iniciando a moldagem da célula eletrônica."

    if re.search(r"\bdiagnostico\b|\bestado\b", msg, re.I):
        return "Todos os sistemas neurais estão operando dentro dos parâmetros."

    # fallback padrão (como você pediu): Hello.
    return "Hello."
