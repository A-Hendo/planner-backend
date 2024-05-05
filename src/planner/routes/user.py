from email_validator import EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from planner.models.user import User
from planner.utils.jwt import CustomAuthJWT
from passlib.context import CryptContext

router = APIRouter()


class RegisterUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    password_repeat: str


class ChangePassword(BaseModel):
    password: str
    new_password: str
    new_password_repeat: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterUser):
    if user.password != user.password_repeat:
        raise HTTPException(status_code=400, detail="Passwords must be the same")

    try:
        User.create(email=user.email, username=user.username, password=user.password)
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail="Email not valid")


@router.post("/password", status_code=status.HTTP_200_OK)
def change_password(body: ChangePassword, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    if body.new_password != body.new_password_repeat:
        raise HTTPException(status_code=400, detail="Passwords must be the same")

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = context.hash(body.new_password)

    User.objects(email=subject).update_one(password=password_hash)