class BaseLine():
    x: list
    y: list
    clr: str
    style: str
    width: int

    def __init__(self, x: list, y: list,
                 clr: str=None, style=None, width=None):
        self.x = x
        self.y = y
        self.clr=clr
        self.style=style
        self.width=width

    def coords(self):
        c=()
        for i in range(len(x)):
            c.append(x[i], y[i])

    def __str__(self):
        string = 'x:' + str(self.x) \
            + ' y:' + str(self.y) \
            + ' clr:' + str(self.clr) \
            + ' width:' + str(self.width) \
            + ' style:' + str(self.style)

        return string


class Line(BaseLine):
    """
    Storage class for canvas line attributes
    """
    id_: str

    def __init__(self, id_: str, x: list, y: list,
                 clr: str=None, style=None, width=None):
        super().__init__(x=x, y=y, clr=clr, style=style, width=width)
        self.id_ = id_
        self.x = x
        self.y = y
        self.clr=clr
        self.style=style
        self.width=width

    def __str__(self):
        string = 'id_:' + str(self.id_) \
            + ' x:' + str(self.x) \
            + ' y:' + str(self.y) \
            + ' clr:' + str(self.clr) \
            + ' width:' + str(self.width) \
            + ' style:' + str(self.style)
        return string

class Graph():
    id_: list

    def __init__(self, x: list, y: list,
                 clr=None, style=None, width:list=None):
        self.x = x
        self.y = y
        self.clr=clr
        self.style=style
        self.width=width

    def get_x_axis(self):
        return BaseLine(x=[self.x[0], self.x[1]],
                        y=[self.y[1], self.y[1]],
                        clr=self.clr,
                        style=self.style,
                        width=self.width)

    def get_y_axis(self):
        return BaseLine(x=[self.x[0], self.x[0]],
                        y=[self.y[0], self.y[1]],
                        clr=self.clr,
                        style=self.style,
                        width=self.width)
        

    def get_xy_axis(self):
        return (self.x[0], self.y[0], self.x[0], self.y[1],
                self.x[0], self.y[1], self.x[1], self.y[1])

    def get_origin(self):
        return (self.x[0], self.y[1])

    def __str__(self):
        string = 'coords:[' + str(self.x[0]) +', '\
            + str(self.y[0]) + ']-[' \
            + str(self.x[0])  +', '\
            + str(self.y[1]) + ']-[' \
            + str(self.x[0])  +', '\
            + str(self.y[1]) + ']-[' \
            + str(self.x[1])  +', '\
            + str(self.y[1]) + ']' \
            + ' clr:' + str(self.clr) \
            + ' width:' + str(self.width) \
            + ' style:' + str(self.style)

        return string

class Triangle():
    id_: list

    def __init__(self, x: list, y: list,
                 clr=None, style=None, width:list=None):
        self.x = x
        self.y = y
        self.clr=clr
        self.style=style
        self.width=width

    def get_coords(self, type_='acute'):
        if not(type_ == 'acute') and \
           not(type_ == 'right') and \
           not(type_ == 'obtuse'):
            raise ValueError('type_ should be "acute", "right" or "obtuse" '\
                             '(obtuse is currently unsupported)')

        
        if self.y[0] < self.y[1]:
            upside_down = False
        else:
            upside_down = True

        if self.x[0] < self.x[1]:
            inverted = True
        else:
            inverted = False

        if upside_down:
            a_y = max(self.y)
            b_y = min(self.y)
            c_y = min(self.y)
        else:
            a_y = min(self.y)
            b_y = max(self.y)
            c_y = max(self.y)

        if inverted:
            a_x = min(self.x)
            b_x = max(self.x)
            if type_ == "right":
                c_x = max(self.x)-abs(max(self.x)-min(self.x))
            else:
                c_x = min(self.x)-abs(max(self.x)-min(self.x))
        else:
            a_x = max(self.x)
            b_x = min(self.x)
            if type_ == "right":
                c_x = min(self.x)+abs(max(self.x)-min(self.x))
            else:
                c_x = max(self.x)+abs(max(self.x)-min(self.x))

        return (a_x, a_y, b_x, b_y, c_x, c_y, a_x, a_y)


class Square():
    id_: list

    def __init__(self, x: list, y: list,
                 clr=None, style=None, width:list=None):
        self.x = x
        self.y = y
        self.clr=clr
        self.style=style
        self.width=width

class Curve():
    id_: list

    def __init__(self, x: list, y: list,
                 clr=None, style=None, width:list=None):
        self.x = x
        self.y = y
        self.clr=clr
        self.style=style
        self.width=width

    def get_coords(self):
        print(self.x, self.y)
        print(min(self.x), min(self.y), min(self.x), max(self.y),
               max(self.x)+abs(max(self.x)-min(self.x)), max(self.y))
        return(min(self.x), min(self.y), min(self.x), max(self.y),
               max(self.x)+abs(max(self.x)-min(self.x)), max(self.y))
    
class Arrow():
    id_: list

    def __init__(self, x: list, y: list,
                 clr=None, style=None, width:list=None):
        self.x = x
        self.y = y
        self.clr=clr
        self.style=style
        self.width=width


class Text(Line):

    def __init__(self, id_: str, x: list, y: list,
                 clr: str=None, style=None, width=None, text=None, font=None):
        super().__init__(id_, x, y,
                         clr, style,
                         width)
        self.text=text
        self.font=font



