from enum import Enum


class MoveType(Enum):
    NORMAL = 2
    CASTLE = 3
    EN_PASSANT = 4
    PROMOTION = 5
    NONE = -2
