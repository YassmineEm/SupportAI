from fastapi import HTTPException
from models.user import UserIn
from utils.hash import hash_password, verify_password
from utils.auth import create_access_token
from utils.db import db

def handle_register(user: UserIn):
    if db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = hash_password(user.password)
    db["users"].insert_one({
        "email": user.email,
        "password": hashed,
        "role": user.role
    })
    return {"msg": "User created"}

def handle_login(user: UserIn):
    user_in_db = db["users"].find_one({"email": user.email})
    if not user_in_db or not verify_password(user.password, user_in_db["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.email,
        "role": user_in_db.get("role", "client")
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
