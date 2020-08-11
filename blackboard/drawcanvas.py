from tk_shapes import Line, Text, Graph
from shape_det import Shape_detector

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image

class DrawCanvas(tk.Canvas):
    """
    A custom tk.Canvas class to allow for drawing

    Allows drawing and is capable of correcting shapes and having different 
    drawing styles and line widths.
    """
    x: int
    y: int
    drawcanvas: tk.Canvas
    line_clr: str
    prev_line_colour: str
    line_width: int
    height: int
    width: int
    lines_list: list
    cleared_lines: list
    draw_style: str
    correct: bool

    def __init__(self, parent, *args, **kwargs):
        if 'bg' in kwargs:
            bg = kwargs['bg']
        else:
            bg = 'black'
        super().__init__(parent, bg=bg, highlightthickness=0)
        self.x = None
        self.y = None
        self.line_clr = 'lightgrey'
        self.line_width = 2
        self.lines_list = []
        self.cleared_lines = []
        self.draw_style = 'pen'
        self.last_coord = dict(x= None, y= None)
        self.graph_coords = dict(x= None, y= None)
        self.correct = True
        self.margin = 30

        self.bind('<Shift-Button-1>', self.draw_straight_line)
        self.bind('<B1-Motion>', self.draw)
        self.bind('<Button-1>', self.draw)
        self.bind('<ButtonRelease-1>', self.mouse_released)
        self.bind('<Button-2>', self.draw_text)
        self.bind('<B3-Motion>', lambda e : {self.draw_line(event=e, clr=None)})
        self.bind('<Button-3>', lambda e : {self.draw_line(event=e, clr=None)})
        self.bind('<ButtonRelease-3>', lambda : {self.set_colour(self.line_clr)})
        self.bind('<ButtonRelease-3>', self.mouse_released)
        self.bind_all('<Control-slash>', self.undo_line_callback)
        self.bind_all('<Control-Key-z>', self.undo_line_callback)
        self.bind('<Key>', self.add_letter)
        self.update()
        self.height =  self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.focus_set()
        self.addtag_all('all')
        self.process_args(*args, **kwargs)

    def process_args(self, *args, **kwargs):
        if 'correct' in kwargs:
            self.correct = kwargs['correct']
        if 'line_width' in kwargs:
            self.line_width = kwargs['line_width']
        if 'line_clr' in kwargs:
            self.line_clr = kwargs['line_clr']
            

    def draw(self, event):
        if self.draw_style == 'text':
            self.set_text_pos(event)
        elif self.draw_style == 'graph':
            if self.graph_coords['x'] == None:
               self.graph_coords = dict(x= event.x,
                                        y= event.y)
            else:
                self.draw_graph(event)
        else:
            self.draw_line(event=event, style=self.draw_style)

    def add_letter(self, event):
        if self.draw_style == 'text':
            if len(self.lines_list):
                if len(self.lines_list[-1]) == 1 and self.lines_list[-1][-1].style == 'text':
                    #add letter
                    text=self.itemcget(self.lines_list[-1][-1].id_, 'text')+event.char
                    self.itemconfigure(self.lines_list[-1][-1].id_, text=text)
                    self.lines_list[-1][-1].text=text
            

    def set_text_pos(self, event):
        if self.x == None:
            self.x=event.x-(self.line_width/2)-2
            self.lines_list.append([])
        if self.y == None:
            self.y=event.y-(self.line_width/2)-2

        self.lines_list[-1].append(Text(id_=self.create_text(event.x, event.y,
                                                             fill=self.line_clr,
                                                             font=("tahoma", "12", "normal"),
                                                             text=""),
                                        x=[self.x],
                                        y=[self.y],
                                        clr=self.line_clr,
                                        style='text',
                                        width=self.line_width,
                                        text="",
                                        font=("tahoma", "12", "normal")))
        
    def draw_graph(self, event):
        self.lines_list.append([])

        x1 = self.graph_coords['x']
        y1 = self.graph_coords['y']
        x2, y2 = event.x, event.y

        graph = Graph(x=[x1,x2],y=[y1,y2], clr=self.line_clr,
                      width=self.line_width, style='graph')

        graph.id_ = self.create_line(graph.get_xy_axis(),
                               fill=self.line_clr,
                               smooth=True,
                               width=self.line_width,
                               capstyle=tk.ROUND,
                               splinesteps=36)

        self.lines_list[-1].append(graph)

        self.draw_text_coords('0', graph.get_origin()[0]-10, graph.get_origin()[1]+10)
        
        self.graph_coords['x']=None
        self.graph_coords['y']=None

    def draw_graph_coords(self, x, y, clr='', width=None):
        self.lines_list.append([])

        l_width=width
        if l_width == None:
            l_width = self.line_width

        graph = Graph(x=x,y=y, clr=clr,
                      width=l_width, style='graph')

        graph.id_ = self.create_line(graph.get_xy_axis(),
                               fill=clr,
                               smooth=True,
                               width=l_width,
                               capstyle=tk.ROUND,
                               splinesteps=36)

        self.lines_list[-1].append(graph)

        

        #self.draw_text_coords('0', graph.get_origin()[0]-10, graph.get_origin()[1]+10)
        
        self.graph_coords['x']=None
        self.graph_coords['y']=None
        

    def draw_text_coords(self, text, x, y, clr='', font=None):
        self.lines_list.append([])

        if font == None:
            font = ("tahoma", "12", "normal")
        if clr == '':
            clr = self.line_clr

        t = Text(id_=self.create_text(x, y,
                                      fill=clr,
                                      font=font,
                                      text=text),
                 x=[x],
                 y=[y],
                 clr=clr,
                 style='text',
                 width=self.line_width,
                 text=text,
                 font=font)

        self.lines_list[-1].append(t)
            
    def draw_text(self, event):
        if self.x == None:
            self.x=event.x-(self.line_width/2)-2
            self.lines_list.append([])
        if self.y == None:
            self.y=event.y-(self.line_width/2)-2

        
        self.lines_list[-1].append(Text(id_=self.create_text(event.x, event.y,
                                                             fill=self.line_clr,
                                                             font=("tahoma", "12", "normal"),
                                                             text="Click the bubbles that are multiples of two."),x=[self.x], y=[self.y], clr=self.line_clr, style='text', width=self.line_width,
                                        text="Click the bubbles that are multiples of two.", font=("tahoma", "12", "normal")))
        
    def draw_line(self, event, clr='', style=None):
        l_width = self.line_width
        if clr == '':
           clr = self.line_clr
        if clr == None:
            l_width = self.line_width*20
        if style == None:
            l_style=self.draw_style
        else:
            l_style = style

        if self.x == None:
            self.x=event.x-(self.line_width/2)-2
            self.lines_list.append([])
        if self.y == None:
            self.y=event.y-(self.line_width/2)-2

        x1, y1 = self.x, self.y
        x2, y2 = event.x-2, event.y-2
        self.x, self.y = event.x, event.y

        if l_style == 'dash':
            dash = (int(10*(l_width/2)), int(10*(l_width/2)))
        elif l_style == 'dot':
            dash=(1, int(10*(l_width/2)))
        else:
            dash=()
        
        l = Line(id_=self.create_line(x1,y1,
                                      x2, y2,
                                      fill=clr,
                                      smooth=True,
                                      width=l_width,
                                      capstyle=tk.ROUND,
                                      splinesteps=36),
                 x=[x1, x2], y=[y1, y2], clr=clr, width=l_width,
                 style=self.draw_style)
        self.lines_list[-1].append(l)

        self.last_coord['x'] = self.x
        self.last_coord['y'] = self.y
        
    def draw_line_coords(self, x1=None, y1=None, x2=None, y2=None,
                         coords=None, clr='', width=None, style=None):
        if width ==  None:
            l_width = self.line_width
        else:
            l_width = width
        if style == None:
            l_style=self.draw_style
        else:
            l_style = style

        if clr == '':
           clr = self.line_clr
        self.lines_list.append([])

        if l_style == 'dash':
            dash = (int(10*(l_width/2)), int(10*(l_width/2)))
        elif l_style == 'dot':
            dash=(1, int(10*(l_width/2)))
        else:
            dash=()

        if not(coords==None):
            l = Line(id_=self.create_line(coords,
                                          fill=clr,
                                          smooth=True,
                                          width=l_width,
                                          capstyle=tk.ROUND,
                                          splinesteps=36,
                                          dash=dash),
                     x=[x1, x2], y=[y1, y2], clr=clr, width=l_width,
                     style=l_style)
        elif not(x1 == None):
            l = Line(id_=self.create_line(x1,y1,
                                          x2, y2,
                                          fill=clr,
                                          smooth=True,
                                          width=l_width,
                                          capstyle=tk.ROUND,
                                          splinesteps=36,
                                          dash=dash),
                     x=[x1, x2], y=[y1, y2], clr=clr, width=l_width,
                     style=l_style)

        self.lines_list[-1].append(l)

        if not(x2 == None or y2 == None):
            self.last_coord['x'] = x2
            self.last_coord['y'] = y2

    def draw_straight_line(self, event, clr=''):
        l_width = self.line_width
        if clr == '':
           clr = self.line_clr
        if clr == None:
            l_width = self.line_width*20

        self.lines_list.append([])

        
        x1, y1 = self.last_coord['x'], self.last_coord['y']
        x2, y2 = event.x-2, event.y-2

        self.x, self.y = event.x, event.y

        if self.draw_style == 'dash':
            dash = (int(10*(l_width/2)), int(10*(l_width/2)))
        elif self.draw_style == 'dot':
            dash = (1, int(10*(l_width/2)))
        else:
            dash = ()

        l = Line(id_=self.create_line((x1,y1,
                                       x2, y2),
                                      fill=clr,
                                      smooth=False,
                                      width=l_width,
                                      capstyle=tk.ROUND,
                                      splinesteps=36,
                                      dash=dash),
                 x=[x1, x2], y=[y1, y2], clr=clr, width=l_width,
                 style=self.draw_style)
            
        self.lines_list[-1].append(l)

        self.last_coord['x'] = self.x
        self.last_coord['y'] = self.y
        

    def draw_dash(self, event, clr=''):
        l_width = self.line_width
        if clr == '':
           clr = self.line_clr
        if clr == None:
            l_width = self.line_width*20

        if self.x == None:
            self.x=event.x-(self.line_width/2)-2
            self.lines_list.append([])
        if self.y == None:
            self.y=event.y-(self.line_width/2)-2

        x1, y1 = self.x, self.y
        x2, y2 = event.x-2, event.y-2
        self.x, self.y = event.x, event.y
        
        l = Line(id_=self.create_line(x1,y1,
                                      x2, y2,
                                      fill=clr,
                                      smooth=True,
                                      width=l_width,
                                      capstyle=tk.ROUND,
                                      splinesteps=36,
                                      dash=(10, int(10*(l_width/2)))),
                 x=[x1, x2], y=[y1, y2], clr=clr, width=l_width,
                 style=self.draw_style)
        self.lines_list[-1].append(l)

        self.last_coord['x'] = self.x
        self.last_coord['y'] = self.y

    def draw_dot(self, event, clr=''):
        l_width = self.line_width
        if clr == '':
           clr = self.line_clr
        if clr == None:
            l_width = self.line_width*20

        if self.x == None:
            self.x=event.x-(self.line_width/2)-2
            self.lines_list.append([])
        if self.y == None:
            self.y=event.y-(self.line_width/2)-2

        x1, y1 = self.x, self.y
        x2, y2 = event.x-2, event.y-2
        self.x, self.y = event.x, event.y
        
        l = Line(id_=self.create_line(x1,y1,
                                      x2, y2,
                                      fill=clr,
                                      smooth=True,
                                      width=l_width,
                                      capstyle=tk.ROUND,
                                      splinesteps=36,
                                      dash=(1, 10)),
                 x=[x1, x2], y=[y1, y2], clr=clr, width=l_width,
                 style=self.draw_style)
        self.lines_list[-1].append(l)

        self.last_coord['x'] = self.x
        self.last_coord['y'] = self.y
    
    def undo_line(self):
        if len(self.lines_list) >= 1:
            for line in self.lines_list[-1]:
                self.delete(line.id_)
        
            del self.lines_list[-1]

            self.last_coord['x'] = self.lines_list[-1][-1].x[-1]
            self.last_coord['y'] = self.lines_list[-1][-1].y[-1]
        else:
            self.undo_clear()
        
    def undo_line_callback(self, event):
        if (event.char == event.keysym or len(event.char)==1) and ('slash' in event.keysym or 'z' in event.keysym):
            try:
                self.undo_line()
            except:
                pass

    def set_draw_style(self, style: str):
        self.draw_style = style
                
    def set_colour(self, colour):
        self.prev_line_colour = self.line_clr
        self.line_clr = colour

    def set_line_width(self, size=None, incr=None, decr=None):
        if not(size == None):
            self.line_width = size
        elif not(incr == None):
            self.line_width += incr
        elif not(decr == None):
            self.line_width -= decr
        else:
            raise ValueError('Unknown error occurred')

        if self.line_width > 200: self.line_width = 200
        elif self.line_width < 1: self.line_width = 1

    def reset_colour(self):
        temp_clr = self.line_clr
        self.line_clr = self.prev_line_colour
        self.prev_line_colour = temp_clr
        
    def mouse_released(self, event):
        self.last_coord['x'] = self.x
        self.last_coord['y'] = self.y
        self.x = None
        self.y = None
        if (self.draw_style == 'pen' or self.draw_style == 'dot' or \
           self.draw_style == 'dash') and \
           not(self.lines_list[-1][-1].clr == None):
            if self.correct:
                self.shape_correct()

    def shape_correct(self):
        s=Shape_detector()
        x, y=[], []
        for line in self.lines_list[-1]:
            #if line.style == 'pen' or line.style == 'dot' or line.style == 'dash':
            for x_ in line.x:
                x.append(x_)
            for y_ in line.y:
                y.append(y_)
        shape = s.get_shape(x=x, y=y, margin=self.margin)

        if shape == 'line' or shape == 'circle' or \
           shape == 'triangle' or shape == 'rectangle':
            coords=[]
            #x, y=[], []
            x, y=s.shape['x'], s.shape['y']
            for i in range(len(x)):
                coords.append(x[i])
                coords.append(y[i])

            line=self.lines_list[-1][-1]
            for line in self.lines_list[-1]:
                self.delete(line.id_)
            del self.lines_list[-1]
            self.draw_line_coords(coords=coords,
                                  clr=line.clr,
                                  width=line.width,
                                  style=line.style)
            #for i in range(1, len(x)):
            #    self.draw_line_coords(x1=x[i-1], y1=y[i-1],
            #                          x2=x[i], y2=y[i],
            #                          clr=line.clr,
            #                          width=line.width,
            #                          style=line.style)

    
    def on_resize(self, event):
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width, self.height = event.width, event.height
        
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        #self.scale("all",0,0,wscale,hscale)

    def clear(self):
        self.cleared_lines = []

        for lines in self.lines_list:
            for line in lines:
                self.cleared_lines.append(line)
        self.delete('all')
        self.lines_list=[]

    def undo_clear(self):
        for line in self.cleared_lines:
            if line.style=='pen' or line.style=='dash' or line.style=='dot':
                self.draw_line_coords(x1=line.x[0], y1=line.y[0],
                                      x2=line.x[1], y2=line.y[1],
                                      clr=line.clr, width=line.width,
                                      style=line.style)
            elif line.style=='text':
                self.draw_text_coords(text=line.text, x=line.x, y=line.y,
                                      clr=line.clr, font=line.font)
            elif line.style=='graph':
                self.draw_graph_coords(x=line.x, y=line.y,
                                       clr=line.clr, width=line.width)


    
