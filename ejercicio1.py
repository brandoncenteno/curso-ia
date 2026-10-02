"""Clase 1: llamada a la API de Claude con formato profesional."""
import logging

import anthropic
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

MODELO = "claude-haiku-4-5-20251001"
MAX_TOKENS = 300


def preguntar(client: anthropic.Anthropic, pregunta: str) -> str:
    """Envía una pregunta a Claude y regresa el texto de la respuesta."""
    respuesta = client.messages.create(
        model=MODELO,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": pregunta}],
    )
    logger.info(
        "Tokens: entrada=%s salida=%s | stop_reason=%s",
        respuesta.usage.input_tokens, respuesta.usage.output_tokens, respuesta.stop_reason,
    )
    if respuesta.stop_reason == "max_tokens":
        logger.warning("La respuesta se cortó por llegar a max_tokens.")
    return respuesta.content[0].text


def main() -> None:
    load_dotenv()
    client = anthropic.Anthropic(max_retries=3, timeout=30.0)
    pregunta = "¿Qué es un ataque de ransomware en una planta industrial? Responde en 3 líneas."
    try:
        print(preguntar(client, pregunta))
    except anthropic.AuthenticationError:
        logger.error("La API key no es válida o no se cargó. Revisa tu .env.")
    except anthropic.RateLimitError:
        logger.error("Demasiadas peticiones. Espera un momento y reintenta.")
    except anthropic.APIConnectionError:
        logger.error("No hay conexión con la API. Revisa tu internet.")
    except anthropic.APIStatusError as e:
        logger.error("La API respondió con error %s: %s", e.status_code, e.message)


if __name__ == "__main__":
    main()