from fastapi import APIRouter

from . import authentication, board, studio, task, user

api_router = APIRouter(
    prefix="/v0",
)

api_router.include_router(user.router)
api_router.include_router(authentication.router)
api_router.include_router(board.router)
api_router.include_router(studio.router)
api_router.include_router(task.router)
