from fastapi import FastAPI, File, UploadFile, HTTPException , Form , Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("LLM_KEY"))
templates = Jinja2Templates(directory="templates")

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
                        {"type": "text", "text": {"content": "Describe esta imagen"}},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with OpenAI: {e}")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/" , response_class=HTMLResponse)
async def root(request: Request):
    """
    Sirve el formulario HTML para cargar la imagen.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyzeimage/")
async def analyze_uploaded_image(file: Annotated[UploadFile, File()]): 
    """Uploads an image and analyzes it using the OpenAI Vision API."""
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    try:
        image_content = await file.read()
        analysis_result = await analyze_image_with_openai(image_content)
        return {"filename": file.filename, "analysis": analysis_result}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")









# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routers import image_analysis

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(image_analysis.router)