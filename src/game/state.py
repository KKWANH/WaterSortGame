from enum import Enum

class GameState(Enum):
    FAILURE = -1
    WAITING = 0
    SUCCESS = 1