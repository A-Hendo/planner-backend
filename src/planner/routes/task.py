from typing import List

from fastapi import APIRouter, Depends, status

from planner.models.board import Board
from planner.models.studio import Studio
from planner.models.task import Task
from planner.models.user import User
from planner.routes.base_models import PostTask, PutTask, TaskModel
from planner.utils.jwt import CustomAuthJWT

router = APIRouter()


@router.post("/task/board/{id}", status_code=status.HTTP_201_CREATED)
def post_task(id: str, task: PostTask, authorize: CustomAuthJWT = Depends()):
    print(task)
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    board = Board.objects(pk=id, user=subject).first()
    user = User.objects(email=subject).first()
    print(board.studio)

    if board.studio:
        return Task(
            title=task.title,
            type=task.type,
            description=task.description,
            tags=task.tags,
            assigned=task.assigned,
            dependents=task.dependents,
            estimation=task.estimation,
            importance=task.importance,
            time_spent=task.time_spent,
            state=task.state,
            owner=user,
            board=board,
            studio=board.studio,
        ).save()
    Task(
        title=task.title,
        type=task.type,
        description=task.description,
        tags=task.tags,
        assigned=task.assigned,
        dependents=task.dependents,
        estimation=task.estimation,
        importance=task.importance,
        time_spent=task.time_spent,
        state=task.state,
        owner=user,
        board=board,
    ).save()


@router.put("/task/{id}", status_code=status.HTTP_200_OK)
def put_task(id: str, task: PutTask, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    Task.objects(pk=id, user=subject).update_one(
        title=task.title,
        type=task.type,
        description=task.description,
        tags=task.tags,
        add_to_set__assigned=[User.objects(email=email).first() for email in task.assigned],
        add_to_set__dependents=[User.objects(email=email).first() for email in task.dependents],
        estimation=task.estimation,
        importance=task.importance,
        time_spent=task.time_spent,
        state=task.state,
    )


@router.delete("/task/{id}", status_code=status.HTTP_200_OK)
def delete_task(id: str, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    Task.objects(pk=id, user=subject).first().delete()


@router.get("/task/{id}", status_code=status.HTTP_200_OK)
def get_task(id: str, authorize: CustomAuthJWT = Depends()) -> TaskModel:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    return Task.objects(pk=id, user=subject).first()


@router.get("/task/board/{id}", status_code=status.HTTP_200_OK)
def get_all_board_tasks(id: str, authorize: CustomAuthJWT = Depends()) -> List[TaskModel]:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    board = Board.objects(pk=id, user=subject).first()
    return Task.objects(board=board)


@router.get("/task/studio/{id}", status_code=status.HTTP_200_OK)
def get_all_studio_tasks(id: str, authorize: CustomAuthJWT = Depends()) -> List[TaskModel]:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    studio = Studio.objects(pk=id, user=subject).first()
    return Task.objects(studio=studio)
