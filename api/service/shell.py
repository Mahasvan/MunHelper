pink = "\033[95m"
blue = "\033[94m"
cyan = "\033[96m"
green = "\033[92m"
yellow = "\033[93m"
red = "\033[91m"
bold = "\033[1m"
underline = "\033[4m"
end_formatting = "\033[0m"


def print_pink_message(text):
    print(f"{pink}        |--- {text}{end_formatting}")


def print_blue_message(text):
    print(f"{blue}        |--- {text}{end_formatting}")


def print_cyan_message(text):
    print(f"{cyan}        |--- {text}{end_formatting}")


def print_green_message(text):
    print(f"{green}        |--- {text}{end_formatting}")


def print_yellow_message(text):
    print(f"{yellow}        |--- {text}{end_formatting}")


def print_red_message(text):
    print(f"{red}        |--- {text}{end_formatting}")


def format_bold(text):
    return bold + text + end_formatting


def format_underline(text):
    return underline + text + end_formatting
