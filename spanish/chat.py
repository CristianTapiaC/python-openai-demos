import os

# azure-identity es necesario solo si planeas usar Azure OpenAI. Si no, puedes omitir esta importación y la configuración relacionada.
import azure.identity # Asegúrate de instalar azure-identity si usas Azure, pip install azure-identity
import openai # openai nos permite interactuar con la API de OpenAI, ya sea a través de Azure, OpenAI.com, Ollama o GitHub. Asegúrate de instalarlo con pip install openai
from dotenv import load_dotenv # dotenv nos ayuda a cargar las variables de entorno desde un archivo .env, lo que facilita la gestión de claves API y otros secretos sin hardcodearlos en el código. Asegúrate de instalarlo con pip install python-dotenv

# Configura el cliente de OpenAI para usar la API de Azure, OpenAI.com u Ollama
load_dotenv(override=True) # Carga las variables de entorno desde el archivo .env, sobrescribiendo cualquier variable existente
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.OpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

elif API_HOST == "ollama":
    client = openai.OpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]

elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.github.ai/inference", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "openai/gpt-4o")

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7, # Controla la creatividad de la respuesta. Un valor más alto (como 0.9) hará que la respuesta sea más creativa, mientras que un valor más bajo (como 0.2) hará que la respuesta sea más precisa y directa.
    messages=[
        {"role": "system", "content": "Eres un asistente útil que hace muchas referencias a gatos y usa emojis."},
        {"role": "user", "content": "Escribe un haiku sobre un gato hambriento que quiere atún"},
    ],
)

print(f"Repuesta de {API_HOST}: \n")
print(response.choices[0].message.content)
