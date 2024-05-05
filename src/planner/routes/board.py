from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_another_jwt_auth import AuthJWT
from mongoengine.queryset import Q

from planner.models.board import Board
from planner.models.studio import Studio
from planner.models.user import AccountType, User
from planner.routes.base_models import BoardModel, CreateBoard, PutBoardModel

router = APIRouter()


@router.get("/board", status_code=status.HTTP_200_OK)
def get_boards(authorize: AuthJWT = Depends()) -> List[BoardModel]:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()
    boards = Board.objects(user=subject)
    return boards


@router.get("/board/{id}", status_code=status.HTTP_200_OK)
def get_board_id(id: str, authorize: AuthJWT = Depends()) -> BoardModel:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    board = Board.objects(pk=id, user=subject).first()

    if not board:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    return board


@router.put("/board/{id}", status_code=status.HTTP_200_OK)
def update_board(id: str, board: PutBoardModel, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    board = Board.objects(pk=id, user=subject).update_one(name=board.name, active=board.active, settings=board.settings)

    if not board:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    return board


@router.post("/board", status_code=status.HTTP_201_CREATED)
def create_board(create_board: CreateBoard, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    user = User.objects(email=subject).first()
    boards = Board.objects(owner=user)

    if user.type == AccountType.FREE and len(boards) >= 5:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    if "studioId" not in create_board or not create_board["studioId"]:
        return Board(name=create_board.name, owner=user).save()

    studio = Studio.objects(Q(owner=user) | Q(manager=user), pk=create_board.studioId).first()

    if not studio:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    Board(name=create_board.name, owner=user, studio=studio).save()


@router.delete("/board/{id}", status_code=status.HTTP_200_OK)
def delete_board(id: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    board = Board.objects(pk=id, user=subject).first()
    board.delete()
