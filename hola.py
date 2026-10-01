from dotenv import load_dotenv
import anthropic

load_dotenv()                     # 1. Lee el archivo .env y carga tu llave
client = anthropic.Anthropic()    # 2. Crea el "cliente" que habla con la API

respuesta = client.messages.create(           # 3. Manda la petición
    model="claude-haiku-4-5-20251001",        #    qué modelo usar
    max_tokens=200,                           #    tope de la respuesta
    messages=[{"role": "user", "content": "Hola Claude, preséntate en una línea."}],
)

print(respuesta.content[0].text)              # 4. Imprime el texto de la respuesta