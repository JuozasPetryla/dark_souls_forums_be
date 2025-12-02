from enum import Enum

class CommentRatingTypes(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"