from fastapi import APIRouter, UploadFile, File
from services import analyze_service

router = APIRouter()

@router.post("/analyze")
async def analyze_chat(file: UploadFile = File(...)):
    return await analyze_service.handle_chat_analysis(file)
