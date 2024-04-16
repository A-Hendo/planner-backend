import mongomock
import pytest
from fastapi.testclient import TestClient
from mongoengine import connect, connection, disconnect
from passlib.context import CryptContext
from planner.main import main
from planner.models.board import Board
from planner.models.studio import Studio
from planner.models.task import Task
from planner.models.user import User
from planner.utils.jwt import CustomAuthJWT


@pytest.fixture
def setup_teardown():
    if connection is not None:
        disconnect()
    connect("mongoenginetest", mongo_client_class=mongomock.MongoClient)
    yield
    disconnect()


pytest.mark.db = pytest.mark.usefixtures("setup_teardown")


@pytest.fixture
def anon_client():
    return TestClient(main(), base_url="http://testserver/api/v0")


@pytest.fixture
def free_client(user):
    access = CustomAuthJWT().create_access_token(subject=user["email"])
    return TestClient(main(), base_url="http://testserver/api/v0", headers={"Authorization": f"Bearer {access}"})


@pytest.fixture
def member_client(member_user):
    access = CustomAuthJWT().create_access_token(subject=member_user["email"])
    return TestClient(main(), base_url="http://testserver/api/v0", headers={"Authorization": f"Bearer {access}"})


@pytest.fixture
def manager_client(manager_user):
    access = CustomAuthJWT().create_access_token(subject=manager_user["email"])
    return TestClient(main(), base_url="http://testserver/api/v0", headers={"Authorization": f"Bearer {access}"})


@pytest.fixture
def owner_client(owner_user):
    access = CustomAuthJWT().create_access_token(subject=owner_user["email"])
    return TestClient(main(), base_url="http://testserver/api/v0", headers={"Authorization": f"Bearer {access}"})


@pytest.fixture
def user():
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = context.hash("password")

    user = User(
        email="user@email.com",
        username="username",
        password=password_hash,
    ).save()
    return user


@pytest.fixture
def owner_user():
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = context.hash("password")

    user = User(
        email="owner@email.com",
        username="username",
        password=password_hash,
    ).save()
    return user


@pytest.fixture
def manager_user(studio):
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = context.hash("password")

    user = User(
        email="manager@email.com",
        username="username",
        password=password_hash,
    ).save()
    studio.managers.append(user)
    studio.save()
    return user


@pytest.fixture
def member_user(studio):
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = context.hash("password")

    user = User(
        email="member@email.com",
        username="username",
        password=password_hash,
    ).save()
    studio.members.append(user)
    studio.save()
    return user


@pytest.fixture
def studio(owner_user):
    return Studio(name="StudioOne", owner=owner_user).save()


@pytest.fixture
def board(user):
    return Board(name="BoardOne", owner=user).save()


# Change to studio_board_owner & updated tests
@pytest.fixture
def studio_board(owner_user, studio):
    return Board(name="Studio Board", owner=owner_user, studio=studio).save()


@pytest.fixture
def task(user, board):
    return Task(owner=user, board=board, title="Task", description="task").save()


@pytest.fixture
def studio_task(user, studio_board, studio):
    return Task(owner=user, board=studio_board, title="Task", description="task", studio=studio).save()
