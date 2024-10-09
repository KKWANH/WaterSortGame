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

class PrintTypes:
    SUCCESS     = Colors.GREEN
    FAILURE     = Colors.RED
    INFORMT     = Colors.CYAN
    WARNING     = Colors.YELLOW

    VALID_TYPES = {
        "SUCCESS": SUCCESS,
        "FAILURE": FAILURE,
        "INFORMT": INFORMT,
        "WARNING": WARNING
    }

    @classmethod
    def isValid(self, _type):
        return _type in self.VALID_TYPES
    
    @classmethod
    def get(self, _type):
        return self.VALID_TYPES.get(_type)

def print_header(_header, _color=None, _type=None):
    """
    _header: string
    _color: ANSI color code based on class 'Colors'
    _type: Print type based on class 'PrintTypes'. Available: (SUCCESS, FAILURE, INFORMT, WARNING)
    """
    color = Colors.RESET
    if Colors.isValid(_color):
        color = _color
    elif PrintTypes.isValid(_type):
        color = PrintTypes.get(_type)
    print(f"{color}{Colors.BOLD}[{_header}]{Colors.RESET}")

def print_command(_header, _body, _header_color=None, _header_type=None, _end="\n"):
    print_header(_header, _color=_header_color, _type=_header_type)
    print(f" {_body}", end=_end)

def print_error(_body, _end="\n"):
    print_command("FAILURE", _body, _header_type=PrintTypes.FAILURE, _end=_end)