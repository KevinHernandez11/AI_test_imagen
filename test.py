from openai import OpenAI
from dotenv import load_dotenv
import requests
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("LLM_KEY"))


response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {
                "type": "input_image",
                "image_url": "moto.jpg",
            },
        ],
    }],
)

print(response.output_text)


# def describir_imagen_openai(ruta_imagen):
#     headers = {
#         "Authorization": f"Bearer {client.api_key}",
#         "Content-Type": "application/json",
#     }
#     payload = {
#         "model": "gpt-4",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": "Describe detalladamente esta imagen."},
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{codificar_imagen_base64(ruta_imagen)}",
#                             "detail": "high"
#                         },
#                     },
#                 ],
#             }
#         ],
#         "max_tokens": 300,
#     }
#     try:
#         response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#         response.raise_for_status()
#         return response.json()["choices"][0]["message"]["content"]
#     except requests.exceptions.RequestException as e:
#         return f"Error al contactar la API de OpenAI: {e}"
#     except KeyError:
#         return "Error al procesar la respuesta de la API de OpenAI."

# def codificar_imagen_base64(ruta_imagen):
#     import base64
#     with open(ruta_imagen, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# ruta_de_tu_imagen = "moto.jpg"
# descripcion = describir_imagen_openai(ruta_de_tu_imagen)
# if descripcion:
#     print(f"Descripción de la imagen: {descripcion}")