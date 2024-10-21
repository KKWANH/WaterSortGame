# util.py

from util.colors import Colors

def print_header(_header, _color=None, _disable=False):
    """
    _header: string
    _color: ANSI color code based on class 'Colors'
    _type: Print type based on class 'PrintTypes'. Available: (SUCCESS, FAILURE, INFORMT, WARNING)
    """
    if _disable:
        print(f"          ", end="")
    else:
        print(f"{_color}{Colors.BOLD}[{_header}]{Colors.RESET}", end=" ")

def print_command(_header, _body, _header_color=None, _header_disable=False, _end="\n"):
    if not isinstance(_end, str):
        raise TypeError(f"_end parameter must be a string, got {type(_end)}, {_end} instead")
    print_header(_header, _color=_header_color, _disable=_header_disable)
    print(f" {_body}", end=_end)

def print_error(_body, _end="\n", _header_disable=False):
    print_command("FAILURE", _body, _header_color=Colors.RED, _header_disable=_header_disable, _end=_end)

def print_info(_body, _end="\n", _header_disable=False):
    print_command("INFORMT", _body, _header_color=Colors.CYAN, _header_disable=_header_disable, _end=_end)

def print_debug(_body, _end="\n", _header_disable=False):
    print_command("_DEBUG_", _body, _header_color=Colors.PURPLE, _header_disable=_header_disable, _end=_end)
