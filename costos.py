"""Cálculo del costo de llamadas a la API de Claude."""

PRECIOS_USD_POR_MILLON = {
    "claude-haiku-4-5-20251001": {"entrada": 1.00, "salida": 5.00},
}
TIPO_CAMBIO_MXN = 18.5  # aproximado; actualízalo periódicamente


def calcular_costo(modelo: str, tokens_entrada: int, tokens_salida: int) -> dict[str, float]:
    """Regresa el costo de una llamada en USD y MXN."""
    precio = PRECIOS_USD_POR_MILLON[modelo]
    usd = (tokens_entrada * precio["entrada"] + tokens_salida * precio["salida"]) / 1_000_000
    return {"usd": usd, "mxn": usd * TIPO_CAMBIO_MXN}