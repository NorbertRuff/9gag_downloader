"""Theme and color definitions."""


class Theme:
    def __init__(self):
        self.border_width = 1
        self.border_color = Color.MAIN
        self.appearance_mode = "dark"
        self.padding = 10
        self.element_width = 1000
        self.geometry = "1024x768"


class Color:
    MAIN = "#42f5b9"
    WHITE = "#ffffff"
    BLACK = "#000000"
    BLUE = "#42f5b9"
    RED = "#ff0000"
    GREEN = "#42f5b9"
    YELLOW = "#ffff00"
