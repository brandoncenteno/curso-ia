#=== 1. Datos de la llamada ===

modelo = "claude-haiku-4-5"
tokens_entrada = 1200 
tokens_salida = 350
precio_entrada = 1 #dolar por millon de tokens
precio_salida = 5 #dolares por millon de tokens
tipo_cambio = 18.3 #MXN por dolar

#=== 2. Calculos ====
tokens_totales = tokens_entrada + tokens_salida

costo_de_entrada_dlls = tokens_entrada / 10**6 * precio_entrada
costo_de_salida_dlls = tokens_salida / 1**6 * precio_salida


costo_total_dlls = costo_de_entrada_dlls + costo_de_salida_dlls
costo_total_mxn = costo_total_dlls * tipo_cambio

respuesta_larga = tokens_salida > 300

     
#=== 3. Ficha ===

print("=== Ficha de llamada ===")
print(f"Modelo: {modelo}")
print(f"Tokens: {tokens_entrada:,} entrada / {tokens_salida:,} salida ({tokens_totales:,} total)" )
print(f"Costo: ${costo_total_dlls:.6f} USD (${costo_total_mxn:.4f} MXN)" )
print(f"¿Respuesta larga?: {respuesta_larga}" )




