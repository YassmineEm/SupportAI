from fastapi import APIRouter, UploadFile, File
from services import document_service

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    return await document_service.handle_document_upload(file)
