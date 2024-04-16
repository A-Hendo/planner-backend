from datetime import datetime

from fastapi import APIRouter, Depends, status

from planner.models.comment import Comment
from planner.models.task import Task
from planner.models.user import User
from planner.routes.base_models import CommentIn, CommentModel
from planner.utils.jwt import CustomAuthJWT

router = APIRouter()


@router.get("/comment/{id}", status_code=status.HTTP_200_OK)
def get_comment(id: str, authorize: CustomAuthJWT = Depends()) -> CommentModel:
    authorize.jwt_required()
    return Comment.objects(pk=id).first()


@router.post("/comment/task/{id}", status_code=status.HTTP_201_CREATED)
def post_comment(id: str, body: CommentIn, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()
    user = User.objects(email=subject).first()

    Task.objects(pk=id).update_one(add_to_set__comments=Comment(text=body.text, owner=user))


@router.put("/comment/{id}", status_code=status.HTTP_200_OK)
def put_comment(id: str, body: CommentIn, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()
    user = User.objects(email=subject).first()

    Comment.objects(pk=id, owner=user).update_one(set__text=body.text, set__updated_date=datetime.now())


@router.delete("/comment/{id}", status_code=status.HTTP_200_OK)
def delete_comment(id: str, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    user = User.objects(email=subject).first()
    comment = Comment.objects(pk=id, owner=user).first()

    comment.delete()


@router.post("comment/{id}", status_code=status.HTTP_201)
def post_reply(id: str, body: CommentIn, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()
    pass
