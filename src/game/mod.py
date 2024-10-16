class GameMod:
    NORMAL = 0
    HIDDEN = 1

    VALID_MOD = {
        "NORMAL": NORMAL,
        "HIDDEN": HIDDEN,
        0: NORMAL,
        1: HIDDEN
    }

    @classmethod
    def isValid(cls, _mod):
        return _mod in cls.VALID_MOD

    @classmethod
    def get(cls, _mod):
        return cls.VALID_MOD.get(_mod)