from fastapi import APIRouter, Form
from services import chat_service

router = APIRouter()

@router.post("/chat")
async def chat_with_bot(question: str = Form(...)):
    return await chat_service.handle_chat(question)
