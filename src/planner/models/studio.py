from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField,
)
from mongoengine.queryset import CASCADE, Q, queryset_manager

from planner.models.user import User


class Settings(EmbeddedDocument):
    """Settings for studio model"""


# ? Owners can invite users to become a member, inviting members costs the owner a studio subscription /
# ? it gives the members a studio_member account type, owners must have a studio account
class Studio(Document):
    """Studio model for grouping users under a company"""

    name = StringField(required=True)
    settings = EmbeddedDocumentField(Settings)
    created = DateTimeField(default=datetime.now())
    updated = DateTimeField(default=datetime.now())
    # ? Deny studio delete when user owner is deleted?
    owner = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    active = BooleanField(default=True)
    managers = ListField(ReferenceField(User))
    members = ListField(ReferenceField(User))

    @queryset_manager
    def objects(doc_cls, queryset, user=None, *args, **kwargs):
        """Queryset_manager to return only active studios to members"""
        if not user:
            return queryset.filter(*args, **kwargs)

        user = User.objects(email=user).first()

        return queryset.filter(Q(active=True) & Q(members=user) | Q(owner=user) | Q(managers=user), *args, **kwargs)
