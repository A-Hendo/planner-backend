from fastapi import status
from fastapi_another_jwt_auth import AuthJWT
from planner.routes.base_models import JWTConfig


class CustomAuthJWT(AuthJWT):
    @AuthJWT.load_config
    def get_config():
        return JWTConfig()

    def get_jwt_subject(self):
        subject = super().get_jwt_subject()

        if not subject:
            raise status.HTTP_401_UNAUTHORIZED
        return subject
