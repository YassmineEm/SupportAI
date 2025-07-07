from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
from services import analyze_service

router = APIRouter()

@router.post("/analyze")
async def analyze_chat(file: UploadFile = File(...), agent: Optional[str] = Form(None)):
    return await analyze_service.handle_chat_analysis(file, agent=agent)

@router.post("/analyze/batch-upload")
async def batch_upload(files: List[UploadFile] = File(...), agent: str = Form(None)):
    return await analyze_service.handle_batch_upload(files, agent=agent)

@router.get("/dashboard")
async def get_dashboard():
    return await analyze_service.get_dashboard_data()
