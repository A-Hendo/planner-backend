from datetime import datetime
from enum import Enum
from typing import Annotated, Any, List, Optional, Union

from bson import ObjectId
from pydantic import (
    AfterValidator,
    BaseModel,
    EmailStr,
    PlainSerializer,
    WithJsonSchema,
)

from config import Config
from planner.models.task import Importance, State, Type


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]


class UserBody(BaseModel):
    email: EmailStr


class StudioBody(BaseModel):
    id: str


class CreateBoard(BaseModel):
    name: str
    studio_id: str | None = None


class UserSettings(BaseModel):
    pass


class UserModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    _id: PyObjectId
    email: EmailStr
    username: str
    type: Enum
    settings: Optional[UserSettings]
    created: datetime
    updated: datetime
    renewal_date: datetime | None


class MemberManagerModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    _id: PyObjectId
    email: EmailStr
    username: str


class StudioSettings(BaseModel):
    pass


class StudioModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    _id: PyObjectId
    name: str
    settings: Optional[StudioSettings]
    created: datetime
    updated: datetime
    owner: UserModel
    active: bool


class BoardSettings(BaseModel):
    pass


class BoardModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    _id: PyObjectId
    name: str
    owner: UserModel
    studio: Optional[StudioModel]
    settings: Optional[BoardSettings]
    created: datetime
    updated: datetime
    active: bool


class CommentModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    _id: PyObjectId
    owner: UserModel
    body: str
    updated: datetime
    created: datetime
    replies: Optional[List["CommentModel"]] = []


class TaskModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    _id: PyObjectId
    title: str
    type: Type
    description: str
    studio: StudioModel
    tags: List[str]
    creation_date: datetime
    updated_date: datetime
    owner: UserModel
    assigned: List[UserModel] | None
    board: BoardModel
    dependents: List[UserModel] | None
    estimation: str | None
    comments: List[CommentModel] | None
    importance: Importance
    time_spent: int | None
    state: State | None = None


class PostTask(BaseModel):
    title: str
    type: Type | None = None
    description: str | None = None
    tags: List[str] | None = None
    assigned: List[UserModel] | None = None
    dependents: List[UserModel] | None = None
    estimation: str | None = None
    importance: Importance | None = None
    time_spent: int | None = None
    state: State | None = None


class PutTask(BaseModel):
    title: str
    type: Type
    description: str
    tags: List[str] = []
    assigned: List[EmailStr] = []
    dependents: List[EmailStr] = []
    estimation: str
    importance: Importance
    time_spent: int
    state: State


class CommentIn(BaseModel):
    text: str


class Token(BaseModel):
    access: str
    refresh: str


class Credentials(BaseModel):
    email: EmailStr
    password: str


class AccessToken(BaseModel):
    access: str


class UserRole(BaseModel):
    username: str
    role: int


class JWTConfig(BaseModel):
    authjwt_secret_key: str = Config.SECRECT_KEY
