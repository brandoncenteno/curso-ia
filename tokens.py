"""Lección 0.1: medir tokens de distintos textos antes de enviarlos."""
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()
MODELO = "claude-haiku-4-5-20251001"

textos = {
    "Español": "La ciberseguridad industrial protege los sistemas que controlan la maquinaria de una planta.",
    "Inglés": "Industrial cybersecurity protects the systems that control a plant's machinery.",
    "Números": "192.168.10.254 502 4840 2026-10-02 3.14159",
    "Código": "def suma(a: int, b: int) -> int:\n    return a + b",
}

for nombre, texto in textos.items():
    r = client.messages.count_tokens(model=MODELO, messages=[{"role": "user", "content": texto}])
    print(f"{nombre:10} | {len(texto):3} caracteres | {r.input_tokens:3} tokens")