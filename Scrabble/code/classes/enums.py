from enum import Enum

class State(Enum):
    NOT_INITIALIZED = 1
    INITIAL = 2
    IN_PROGRESS = 3
    ABANDONED = 4
    FINISHED = 5
    WAITING_REMOTE_MOVE = 6
    LOCAL_MOVE = 7

class Move(Enum):
    CONSTRUCTION = 1
    CHANGE = 2
    GIVE_UP = 3