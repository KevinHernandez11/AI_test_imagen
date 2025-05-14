import base64
from openai import OpenAI
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("LLM_KEY"))

async def analyze_image_with_openai(image_content: bytes):
    """Analyzes an image using the OpenAI Vision API."""
    base64_image = base64.b64encode(image_content).decode("utf-8")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": {"content": "Describe esta imagen traduciendo al español"}},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with OpenAI: {e}")