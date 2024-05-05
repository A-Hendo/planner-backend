from datetime import datetime
from enum import Enum, EnumType
from typing import Annotated, Any, List, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from config import Config
from planner.models.task import Importance, State, Type


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


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

    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    email: EmailStr
    username: str
    type: Enum
    settings: Optional[UserSettings]
    created: datetime
    updated: datetime
    renewal_date: datetime | None
    password_expired: bool


class MemberManagerModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    email: EmailStr
    username: str


class StudioSettings(BaseModel):
    pass


class StudioModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    name: str
    settings: Optional[StudioSettings]
    created: datetime
    updated: datetime
    owner: UserModel
    active: bool

class PutStudio(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    settings: Optional[StudioSettings]
    active: bool

class PostStudio(BaseModel):
    name: str


class BoardSettings(BaseModel):
    pass


class BoardModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    name: str
    owner: UserModel
    studio: Optional[StudioModel]
    settings: Optional[BoardSettings]
    created: datetime
    updated: datetime
    active: bool


class PutBoardModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    settings: Optional[BoardSettings]
    active: bool


class CommentModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    owner: UserModel
    body: str
    updated: datetime
    created: datetime
    replies: Optional[List["CommentModel"]] = []

class AllTasks(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    sid: int
    title: str
    type: Type
    state: State | None = None


class TaskModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    sid: int
    title: str
    type: Type
    description: str
    studio: StudioModel | None
    tags: List[str]
    creation_date: datetime
    updated_date: datetime
    owner: UserModel
    assigned: List[UserModel] | None
    board: BoardModel
    dependents: List[UserModel] | None
    estimation: dict = {}
    comments: List[CommentModel] | None
    importance: Importance
    time_spent: dict = {}
    state: State | None = None


class PostTask(BaseModel):
    title: str
    type: Type = Type.TASK
    description: str | None = None
    tags: List[str] = []
    assigned: List[UserModel] = []
    dependents: List[UserModel] = []
    estimation: dict = {}
    importance: Importance = Importance.MEDIUM
    time_spent: dict = {}
    state: State = State.TODO


class PutTask(BaseModel):
    title: Optional[str] = None
    type: Optional[Type] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    assigned: Optional[List[EmailStr]] = None
    dependents: Optional[List[EmailStr]] = None
    estimation: Optional[dict] = {}
    importance: Optional[Importance] = None
    time_spent: Optional[dict] = None
    state: Optional[State] = None


class PatchTask(BaseModel):
    title: str
    type: Type
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


class JWTConfig(BaseModel):
    authjwt_secret_key: str = Config.SECRECT_KEY
