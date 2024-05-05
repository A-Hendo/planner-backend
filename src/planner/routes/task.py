from typing import List

from fastapi import APIRouter, Depends, Request, status
from fastapi_filter import FilterDepends

from planner.models.board import Board
from planner.models.studio import Studio
from planner.models.task import Task
from planner.models.user import User
from planner.routes.base_models import AllTasks, PatchTask, PostTask, PutTask, TaskModel
from planner.routes.filters import TaskFilter
from planner.utils.jwt import CustomAuthJWT

router = APIRouter()


@router.post("/task/board/{id}", status_code=status.HTTP_201_CREATED)
def post_task(id: str, task: PostTask, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    board = Board.objects(pk=id, user=subject).first()
    user = User.objects(email=subject).first()

    # ? Possibly need to pass a new Task with user objects (or don't)
    dependents = [User.objects(pk=pk).first() for pk in task.dependents]
    assigned = [User.objects(pk=pk).first() for pk in task.assigned]

    if board.studio:
        return Task(
            **task.model_dump(),
            owner=user,
            board=board,
            studio=board.studio,
        ).save()
    return Task(
        **task.model_dump(),
        owner=user,
        board=board,
    ).save()


@router.patch("/task/{id}", status_code=status.HTTP_200_OK)
def put_task(id: str, task: PatchTask, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()
    Task.objects(pk=id, user=subject).update_one(**task.model_dump())


@router.put("/task/{id}", status_code=status.HTTP_200_OK)
def put_task(id: str, task: PutTask, authorize: CustomAuthJWT = Depends()):
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()
    Task.objects(pk=id, user=subject).update_one(**task.model_dump())


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
def get_all_board_tasks(
    request: Request, id: str, filters: TaskFilter = FilterDepends(TaskFilter), authorize: CustomAuthJWT = Depends()
) -> List[AllTasks]:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    board = Board.objects(pk=id, user=subject).first()
    tasks = Task.objects(board=board).only("pk", "sid", "title", "type", "state")

    return filters.filter(tasks)


@router.get("/task/studio/{id}", status_code=status.HTTP_200_OK)
def get_all_studio_tasks(id: str, authorize: CustomAuthJWT = Depends()) -> List[TaskModel]:
    authorize.jwt_required()
    subject = authorize.get_jwt_subject()

    studio = Studio.objects(pk=id, user=subject).first()
    return Task.objects(studio=studio)
