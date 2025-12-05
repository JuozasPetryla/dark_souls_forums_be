from enum import Enum

class UserRelationTypes(str, Enum):
    FRIEND = "friend"
    BLOCKED = "blocked"