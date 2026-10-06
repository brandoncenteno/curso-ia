"""Clase 1: llamada a la API de Claude con formato profesional."""
import logging

import anthropic
from dotenv import load_dotenv
from costos import calcular_costo

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

MODELO = "claude-haiku-4-5-20251001"
MAX_TOKENS = 300
LIMITE_TOKENS_ENTRADA = 200

def contar_tokens(client: anthropic.Anthropic, pregunta: str) -> int:
    """Cuenta los tokens de entrada de una pregunta sin generar respuesta."""
    conteo = client.messages.count_tokens(
        model=MODELO,
        messages=[{"role": "user", "content": pregunta}],
    )
    return conteo.input_tokens


def preguntar(client: anthropic.Anthropic, pregunta: str) -> str | None:
    """Envía una pregunta a Claude si no supera el límite de tokens de entrada."""
    tokens = contar_tokens(client, pregunta)
    if tokens > LIMITE_TOKENS_ENTRADA:
        logger.warning("Pregunta rechazada: %s tokens (límite: %s).", tokens, LIMITE_TOKENS_ENTRADA)
        return None
    
    respuesta = client.messages.create(
        model=MODELO,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": pregunta}],
    )
    logger.info(
        
        "Tokens: entrada=%s salida=%s | stop_reason=%s",
        respuesta.usage.input_tokens, respuesta.usage.output_tokens, respuesta.stop_reason,
    )
    costo = calcular_costo(MODELO, respuesta.usage.input_tokens, respuesta.usage.output_tokens)
    logger.info("Costo: $%.6f USD (≈ $%.4f MXN)", costo["usd"], costo["mxn"]
    )
    
    
    if respuesta.stop_reason == "max_tokens":
        logger.warning("La respuesta se cortó por llegar a max_tokens.")
    return respuesta.content[0].text


def main() -> None:
    load_dotenv()
    client = anthropic.Anthropic(max_retries=3, timeout=30.0)
    pregunta = "Explica la ciberseguridad industrial. " * 50
    try:
        texto = preguntar(client, pregunta)  # NUEVO: guardamos el resultado
        if texto is not None:                # NUEVO: solo imprime si no fue rechazada
            print(texto)
    except anthropic.AuthenticationError:  
        logger.error("La API key no es válida o no se cargó. Revisa tu .env.")
    except anthropic.RateLimitError:
        logger.error("Demasiadas peticiones. Espera un momento y reintenta.")
    except anthropic.AuthenticationError as e:
        logger.exception("Error de autenticación: %s", e)
    except anthropic.APIStatusError as e:
        logger.error("La API respondió con error %s: %s", e.status_code, e.message)


if __name__ == "__main__":
    main()