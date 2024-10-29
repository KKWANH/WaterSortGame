class Colors:
    PURPLE       = '\033[95m'
    BLUE         = '\033[94m'
    CYAN         = '\033[96m'
    GREEN        = '\033[92m'
    YELLOW       = '\033[93m'
    RED          = '\033[91m'
    RESET        = '\033[0m'
    BOLD         = '\033[1m'
    UNDERLINE    = '\033[4m'

    VALID_COLORS = {
        PURPLE, BLUE, CYAN, GREEN, YELLOW, RED, RESET, BOLD, UNDERLINE
    }

    @classmethod
    def isValid(self, _color):
        return _color in self.VALID_COLORS