from fastapi import status
from fastapi_another_jwt_auth import AuthJWT
from jwt import ExpiredSignatureError
from planner.routes.base_models import JWTConfig


class CustomAuthJWT(AuthJWT):
    @AuthJWT.load_config
    def get_config():
        return JWTConfig()

    def get_jwt_subject(self):
        try:
            subject = super().get_jwt_subject()
        except ExpiredSignatureError:
            raise status.HTTP_401_UNAUTHORIZED

        if not subject:
            raise status.HTTP_401_UNAUTHORIZED
        return subject

    def jwt_required(self):
        try:
            super().jwt_required()
        except ExpiredSignatureError:
            raise status.HTTP_401_UNAUTHORIZED
