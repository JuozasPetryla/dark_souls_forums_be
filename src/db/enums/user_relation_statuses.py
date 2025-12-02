from enum import Enum

class UserRelationStatuses(str, Enum):
    ACCEPTED = "accepted"
    PENDING = "pending"
    DECLINED = "declined"