from pydantic import BaseModel, EmailStr
from typing import Literal

class UserIn(BaseModel):  
    email: EmailStr
    password: str
    role: Literal["admin", "client"] = "client"

class UserOut(BaseModel):  
    email: EmailStr
    role: Literal["admin", "client"]

