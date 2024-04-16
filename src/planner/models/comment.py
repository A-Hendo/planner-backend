from datetime import datetime

from mongoengine import (
    DateTimeField,
    EmbeddedDocument,
    ListField,
    ReferenceField,
    StringField,
)

from planner.models.user import User


class Comment(EmbeddedDocument):
    owner = ReferenceField(User, required=True)
    text = StringField(default="", required=True)
    updated = DateTimeField(default=datetime.now())
    created = DateTimeField(default=datetime.now())
    replies = ListField(ReferenceField("self"))
