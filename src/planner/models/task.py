from datetime import datetime
from enum import Enum, auto

from mongoengine import (
    DateTimeField,
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    EnumField,
    IntField,
    ListField,
    ReferenceField,
    SequenceField,
    StringField,
)
from mongoengine.queryset import CASCADE, Q, queryset_manager

from planner.models.board import Board
from planner.models.comment import Comment
from planner.models.studio import Studio
from planner.models.user import User


class Type(Enum):
    TASK = auto()
    BUG = auto()


class Importance(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class State(Enum):
    TODO = auto()
    IN_PROGRESS = auto()
    VERIFICATION = auto()
    DONE = auto()


class ActivityLog(EmbeddedDocument):
    user = ReferenceField(User, required=True)
    amount = IntField(required=True)  # ? minutes?


class Task(Document):
    """Task Model"""

    sid = SequenceField()
    title = StringField(required=True)
    group = StringField()  # For splitting tasks, eg for backend, frontend, etc
    type = EnumField(Type, default=Type.TASK)
    description = StringField()
    studio = ReferenceField(Studio, reverse_delete_rule=CASCADE, default=None)
    tags = ListField(StringField())
    creation_date = DateTimeField(default=datetime.now())
    updated_date = DateTimeField(default=datetime.now())
    owner = ReferenceField(User, required=True)
    assigned = ListField(ReferenceField(User), default=[])
    board = ReferenceField(Board, reverse_delete_rule=CASCADE, required=True)
    dependents = ListField(ReferenceField(User), default=[])
    estimation = DictField(default={})
    comments = EmbeddedDocumentListField(Comment, default=None)
    importance = EnumField(Importance, default=Importance.MEDIUM)
    activity_log = EmbeddedDocumentListField(ActivityLog)
    time_spent = DictField(default={})
    state = EnumField(State, default=State.TODO)

    @queryset_manager
    def objects(doc_cls, queryset, user=None, *args, **kwargs):
        if not user:
            return queryset.filter(*args, **kwargs)

        studios = Studio.objects(user=user)
        boards = Board.objects(user=user)
        user = User.objects(email=user).first()

        return queryset.filter(Q(owner=user) | Q(studio__in=studios) | Q(board__in=boards), *args, **kwargs)

    def save(self, *args, **kwargs):
        tasks = Task.objects(board=self.board)
        self.sid = len(tasks) + 1
        return super(Task, self).save(*args, **kwargs)
