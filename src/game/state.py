class GameState:
    FAILURE = -1
    WAITING  = 0
    SUCCESS = 1

    VALID_STATE = {
        "NORMAL": WAITING,
        "FAILURE": FAILURE,
        "SUCCESS": SUCCESS,
        -1: FAILURE,
        0:  WAITING,
        1:  SUCCESS
    }

    @classmethod
    def isValid(cls, _mod):
        return _mod in cls.VALID_STATE

    @classmethod
    def get(cls, _mod):
        return cls.VALID_STATE.get(_mod)
