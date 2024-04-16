from datetime import datetime
from enum import IntEnum, auto

from email_validator import validate_email
from mongoengine import (
    DateTimeField,
    Document,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EnumField,
    StringField,
)
from passlib.context import CryptContext

from planner.models.base_permissions import BasePermissions


class AccountType(IntEnum):
    FREE = auto()
    PRO = auto()
    STUDIO = auto()
    STUDIO_MEMBER = auto()


class Settings(EmbeddedDocument):
    """Settings model for users"""


class User(Document, BasePermissions):
    """User model for mongodb"""

    email = EmailField(required=True, unique=True)
    username = StringField(required=True)
    password = StringField(required=True)
    type = EnumField(AccountType, default=AccountType.FREE)
    settings = EmbeddedDocumentField(Settings)
    created = DateTimeField(default=datetime.now())
    updated = DateTimeField(default=datetime.now())
    renewal_date = DateTimeField(default=None)

    def create(user):
        validated_email = validate_email(user.email, check_deliverability=False)
        email = validated_email.normalized

        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password_hash = context.hash(user.password)

        user = User(email=email, username=user.username, password=password_hash).save()
        print(user.to_json())

    def permissions(self):
        return BasePermissions(self)
