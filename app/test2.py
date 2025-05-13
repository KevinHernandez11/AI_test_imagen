import os
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Annotated
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("LLM_KEY"))

async def analyze_image_with_openai(image_content: bytes, prompt: str = "Describe this image."):
    """Analyzes an image using the OpenAI Vision API."""
    base64_image = base64.b64encode(image_content).decode("utf-8")
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with OpenAI: {e}")

@app.post("/analyzeimage/")
async def analyze_uploaded_image(file: Annotated[UploadFile, File()], prompt: str = "Describe this image."):
    """Uploads an image and analyzes it using the OpenAI Vision API."""
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    try:
        image_content = await file.read()
        analysis_result = await analyze_image_with_openai(image_content, prompt)
        return {"filename": file.filename, "analysis": analysis_result}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    #esto se tiene que subir en github