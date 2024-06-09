PINK = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END_FORMATTING = "\033[0m"

BASE = "    |--- "


def print_pink_message(text, *args, **kwargs):
    print(f"{PINK}{BASE}{text}{END_FORMATTING}", *args, **kwargs)


def print_blue_message(text, *args, **kwargs):
    print(f"{BLUE}{BASE}{text}{END_FORMATTING}", *args, **kwargs)


def print_cyan_message(text, *args, **kwargs):
    print(f"{CYAN}{BASE}{text}{END_FORMATTING}", *args, **kwargs)


def print_green_message(text, *args, **kwargs):
    print(f"{GREEN}{BASE}{text}{END_FORMATTING}", *args, **kwargs)


def print_yellow_message(text, *args, **kwargs):
    print(f"{YELLOW}{BASE}{text}{END_FORMATTING}", *args, **kwargs)


def print_red_message(text, *args, **kwargs):
    print(f"{RED}{BASE}{text}{END_FORMATTING}", *args, **kwargs)


def format_bold(text):
    return f"{BOLD}{text}{END_FORMATTING}"


def format_underline(text):
    return f"{UNDERLINE}{text}{END_FORMATTING}"
