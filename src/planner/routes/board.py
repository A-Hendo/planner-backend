from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_another_jwt_auth import AuthJWT
from mongoengine.queryset import Q

from planner.models.board import Board
from planner.models.studio import Studio
from planner.models.user import User
from planner.routes.base_models import BoardModel, CreateBoard

router = APIRouter()


@router.get("/board", status_code=status.HTTP_200_OK)
def get_boards(authorize: AuthJWT = Depends()) -> List[BoardModel]:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    return Board.objects(user=subject)


@router.get("/board/{id}", status_code=status.HTTP_200_OK)
def get_board_id(id: str, authorize: AuthJWT = Depends()) -> BoardModel:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    board = Board.objects(pk=id, user=subject).first()

    if not board:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    return board


@router.post("/board", status_code=status.HTTP_201_CREATED)
def create_board(create_board: CreateBoard, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    user = User.objects(email=subject).first()

    if user.type

    if "studio_id" not in create_board:
        return Board(name=create_board.name, owner=user).save()

    studio = Studio.objects(Q(owner=user) | Q(manager=user), pk=create_board.studio_id).first()

    if not studio:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    Board(name=create_board.name, owner=user, studio=studio).save()
