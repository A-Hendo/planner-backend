from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ReferenceField,
    StringField,
)
from mongoengine.queryset import CASCADE, Q, queryset_manager

from planner.models.studio import Studio
from planner.models.user import User


class Settings(EmbeddedDocument):
    """Settings for board model"""


class Board(Document):
    """Board model for grouping tasks under a single board"""

    name = StringField(required=True)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE)
    studio = ReferenceField(Studio, default=None, reverse_delete_rule=CASCADE)
    settings = EmbeddedDocumentField(Settings)
    created = DateTimeField(default=datetime.now())
    updated = DateTimeField(default=datetime.now())
    active = BooleanField(default=True)

    @queryset_manager
    def objects(doc_cls, queryset, user=None, *args, **kwargs):
        """Queryset_manager was more difficult to implement than the class,
        manager would  be a better implementation to as it would be on every
        objects call"""
        if not user:
            return queryset.filter(*args, **kwargs)

        studio = Studio.objects(user=user)
        user = User.objects(email=user).first()

        if studio:
            return queryset.filter(Q(owner=user) | Q(studio__in=studio), *args, **kwargs)
        return queryset.filter(Q(owner=user), *args, **kwargs)
