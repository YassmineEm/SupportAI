from fastapi import APIRouter, HTTPException
from models.user import UserIn
from services.auth_service import handle_register, handle_login

router = APIRouter()

@router.post("/register")
def register(user: UserIn):
    return handle_register(user)

@router.post("/login")
def login(user: UserIn):
    return handle_login(user)

