from email_validator import EmailNotValidError
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from planner.models.user import User

router = APIRouter()


class RegisterUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    password_repeat: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterUser):
    if user.password != user.password_repeat:
        raise HTTPException(status_code=400, detail="Passwords must be the same")

    try:
        User.create(user=user)
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail="Email not valid")
