class Line():
    """
    Storage class for canvas line attributes
    """
    id_: str
    x: list
    y: list
    clr: str
    style: str
    width: int

    def __init__(self, id_: str, x: list, y: list,
                 clr: str=None, style=None, width=None):
        self.id_ = id_
        self.x = x
        self.y = y
        self.clr=clr
        self.style=style
        self.width=width

class Graph():
    pass

class Triangle():
    pass

class Square():
    pass

class Text(Line):

    def __init__(self, id_: str, x: list, y: list,
                 clr: str=None, style=None, width=None, text=None, font=None):
        super().__init__(id_, x, y,
                         clr, style,
                         width)
        self.text=text
        self.font=font
