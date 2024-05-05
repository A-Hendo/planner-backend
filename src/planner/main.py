from slowapi import Limiter
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from mongoengine import connect
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi import Limiter

from config import Config
from planner.routes.routers import api_router


def main():
    app = FastAPI()

    limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    @app.exception_handler(RateLimitExceeded)
    def rate_limit_execption_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
        response = JSONResponse(
            {"error": f"Rate limit exceeded: {exc.detail}"}, status_code=429
        )
        response = request.app.state.limiter._inject_headers(
            response, request.state.view_rate_limit
        )
        return response

    origins = [
        "http://localhost",
        "http://localhost:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    connect(
        host=Config.MONGO_HOST,
        db=Config.MONGO_DB,
        username=Config.MONGO_USER,
        password=Config.MONGO_PASSWORD,
    )

    return app


if __name__ == "__main__":
    uvicorn.run("planner.main:main", reload=True)
