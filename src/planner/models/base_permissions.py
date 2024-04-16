from enum import Enum, auto


class PermissionTypes(Enum):
    OWNER = auto()
    MANAGER = auto()
    MEMBER = auto()
    NONE = auto()


class BasePermissions:
    def __init__(self, user):
        self.user = user

    def check(self, obj):
        if hasattr(obj, "studio"):
            if obj.owner == self.user:
                return PermissionTypes.OWNER
            if obj.studio:
                if obj.studio.owner == self.user:
                    return PermissionTypes.OWNER
                elif self.user in obj.studio.managers:
                    return PermissionTypes.MANAGER
                elif self.user in obj.studio.members:
                    return PermissionTypes.MEMBER
        else:
            if obj.owner == self.user:
                return PermissionTypes.OWNER
            elif self.user in obj.managers:
                return PermissionTypes.MANAGER
            elif self.user in obj.members:
                return PermissionTypes.MEMBER
        return PermissionTypes.NONE
