import os, tty, termios, sys

class Color:
    colors = {
        "black": '\033[30m',
        "red": '\033[31m',
        "green": '\033[32m',
        "yellow": '\033[33m',
        "blue": '\033[34m',
        "magenta": '\033[35m',
        "cyan": '\033[36m',
        "white": '\033[37m',
        "reset": '\033[39m',

        "bg_black": '\033[40m',
        "bg_red": '\033[41m',
        "bg_green": '\033[42m',
        "bg_yellow": '\033[43m',
        "bg_blue": '\033[44m',
        "bg_magenta": '\033[45m',
        "bg_cyan": '\033[46m',
        "bg_white": '\033[47m',
        "bg_reset": '\033[49m'
    }

class Decor:
    styles = {
        "bold": ('\033[1m', '\033[22m'),
        "dim": ('\033[2m', '\033[22m'),
        "italic": ('\033[3m', '\033[23m'),
        "underline": ('\033[4m', '\033[24m'),
        "blink": ('\033[5m', '\033[25m'),
        "reset_all": ('\033[0m',)
    }

class Gui:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Gui, cls).__new__(cls)
            cls._is_win = os.name == 'nt'
            ## default user selections
            cls.color_settings = {
                "_fc": Color.colors["white"],
                "_bc": Color.colors["bg_black"],
                "_ec": Color.colors["red"],
                "_cc": Color.colors["green"],
                "_ac": Color.colors["yellow"]
            }
        return cls._instance
    
    @property
    def clear(self):
        os.system("cls") if self._is_win else os.system("clear")

    def ls(self, menu: list[dict[str, str]]):
        for item in menu:
            print(f"{item["key"]}. {item["name"]}")


    def styled(self, text, style):
        if style in Decor.styles:
            start, end = Decor.styles[style]
            return f"{start}{text}{end}"
        return text
    
    def colored(self, text, color):
        if color in self.color_settings:
            return f"{self.color_settings[color]}{text}{Color.colors["reset"]}"

    @property
    def lis(self):
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        return ch
    
    def reparam(self, userconfig):
        self.color_settings = {
            key: Color.colors[value]
            for key, value in userconfig["colors"].items()
        }
        
    def print_table(self, data: list[tuple[str, bool]], headers: tuple[str, str]):
        data = [(username, "admin" if admin else "non-admin") for username, admin in data]
        column_widths = [max(len(str(item[i])) for item in data + [headers]) for i in range(len(headers))]
        row_format = "  ".join([f"{{:<{width}}}" for width in column_widths])
        print(row_format.format(*headers))
        print("  ".join(["-" * width for width in column_widths]))
        for row in data:
            print(row_format.format(*row))