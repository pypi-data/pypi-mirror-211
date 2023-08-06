from fastapi_utils.enums import StrEnum


class GroupName(StrEnum):
    GROUND = "GROUND"
    EXPLORER = "EXPLORER"
    INNOVATOR = "INNOVATOR"
    ADMIN = "ADMIN"

    def __str__(self):
        return str(self.value)


class RoleName(StrEnum):
    SUPERUSER = "SUPERUSER"
    ORG_ADMIN = "ORG_ADMIN"

    def __str__(self):
        return str(self.value)
