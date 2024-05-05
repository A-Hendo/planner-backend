from fastapi import APIRouter, Depends, HTTPException, Request, status
from passlib.context import CryptContext

from planner.models.user import User
from planner.routes.base_models import AccessToken, Credentials, Token, UserModel
from planner.utils.jwt import CustomAuthJWT

router = APIRouter()


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def authenticate(request: Request, credentials: Credentials, authorize: CustomAuthJWT = Depends()):
    user = User.objects(email=credentials.email).first()
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if user is None or not context.verify(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    access = authorize.create_access_token(subject=user["email"])
    refresh = authorize.create_refresh_token(subject=user["email"])

    return Token(access=access, refresh=refresh)


@router.get("/refresh")
def refresh(request: Request, authorize: CustomAuthJWT = Depends()) -> AccessToken:
    authorize.jwt_refresh_token_required()
    subject = authorize.get_jwt_subject()
    access = authorize.create_access_token(subject=subject)

    return AccessToken(access=access)


@router.get("/user")
def current_user(request: Request, authorize: CustomAuthJWT = Depends()) -> UserModel:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()
    user = User.objects(email=subject).first()

    return user


@router.get("/validate", status_code=status.HTTP_200_OK)
def validate_token(request: Request, authorize: CustomAuthJWT = Depends()) -> bool:
    authorize.jwt_optional()
    subject = authorize.get_raw_jwt()

    if subject:
        return True
    return False
