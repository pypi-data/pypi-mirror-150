BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"

RESET = "\033[0m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"


def from_id(id_: int) -> str:
    return f"\033[38;5;{id_}m"
