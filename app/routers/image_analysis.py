from fastapi import APIRouter, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from app.services.openai_service import analyze_image_with_openai

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root():
    return {"message": "Hello World"}
    # return templates.TemplateResponse("index.html", {"request": request,})

@router.post("/analyzeimage/")
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
