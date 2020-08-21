from tk_shapes import Line, Text, Graph, Triangle, Square
from shape_det import Shape_detector
from image_prc import image_prc

import os
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
    scale_widg: bool

    def __init__(self, parent, *args, **kwargs):
        """
        Initialise the variables, bindings and other important aspects of the canvas
        
        Parameters
        ----------
        Parent:
            The parent widget
        *args:
            Optional and positional arguments
        **kwargs:
            Optional and specified arguments
        """
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
        self.triangle_coords = dict(x= None, y= None)
        self.square_coords = dict(x= None, y= None)
        self.correct = True
        self.scale_widg = False
        self.margin = 30
        self.margin_line = self.margin
        self.margin_circle = self.margin
        self.margin_triangle = self.margin
        self.movement = 20

        self.init_bindings(args=args, kwargs=kwargs)

        self.update()
        self.height =  self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.focus_set()
        self.addtag_all('all')
        self.process_args(*args, **kwargs)

    def process_args(self, *args, **kwargs):
        """
        Processes the optional arguments.
        
        Parameters
        ----------
        *args:
            Optional and positional arguments
        **kwargs:
            Optional and specified arguments
        """
        if 'correct' in kwargs:
            self.correct = kwargs['correct']
        if 'line_width' in kwargs:
            self.line_width = kwargs['line_width']
        if 'line_clr' in kwargs:
            self.line_clr = kwargs['line_clr']

    def init_bindings(self, *args, **kwargs):
        """
        Checks the optional arguments for setting of bindings.

        By default, all bindings are being done.

        Parameters
        ----------
        *args:
            Optional and positional arguments
        **kwargs:
            Optional and specified arguments
        """
        # Bindings of straight line drawing
        if 'bind_straight_ln' in kwargs:
            if kwargs['bind_straight_ln']:
                self.bind('<Shift-Button-1>', self.draw_straight_line)
        else:
            self.bind('<Shift-Button-1>', self.draw_straight_line)

        # Bindings of line drawing
        if 'bind_draw' in kwargs:
            if kwargs['bind_draw']:
                self.bind('<B1-Motion>', self.draw)
                self.bind('<Button-1>', self.draw)
                self.bind('<ButtonRelease-1>', self.mouse_released)
        else:
            self.bind('<B1-Motion>', self.draw)
            self.bind('<Button-1>', self.draw)
            self.bind('<ButtonRelease-1>', self.mouse_released)

        # Bindings of text writing
        if 'bind_text' in kwargs:
            if kwargs['bind_text']:
                self.bind('<Button-2>', self.draw_text)
        else:
            self.bind('<Button-2>', self.draw_text)

        # Bindings of eraser
        if 'bind_eraser' in kwargs:
            if kwargs['bind_eraser']:
                self.bind('<B3-Motion>', lambda e : {self.draw_line(event=e, clr=None)})
                self.bind('<Button-3>', lambda e : {self.draw_line(event=e, clr=None)})
                self.bind('<ButtonRelease-3>', lambda : {self.set_colour(self.line_clr)})
                self.bind('<ButtonRelease-3>', self.mouse_released)
        else:
            self.bind('<B3-Motion>', lambda e : {self.draw_line(event=e, clr=None)})
            self.bind('<Button-3>', lambda e : {self.draw_line(event=e, clr=None)})
            self.bind('<ButtonRelease-3>', lambda : {self.set_colour(self.line_clr)})
            self.bind('<ButtonRelease-3>', self.mouse_released)

        # Bindings of zooming
        if 'bind_zoom' in kwargs:
            if kwargs['bind_zoom']:
                self.bind('<Control-Button-4>', lambda e : self.zoom(event=e, direction="+"))
                self.bind('<Control-Button-5>', lambda e : self.zoom(event=e, direction="-"))
        else:
            self.bind('<Control-Button-4>', lambda e : self.zoom(event=e, direction="+"))
            self.bind('<Control-Button-5>', lambda e : self.zoom(event=e, direction="-"))

        # Bindings of movement
        if 'bind_movement' in kwargs:
            if kwargs['bind_movement']:
                self.bind('<Shift-Button-4>', self.move_right)
                self.bind_all('<Left>', self.move_right)
                self.bind('<Shift-Button-5>', self.move_left)
                self.bind('<Button-4>', self.move_down)
                self.bind('<Button-5>', self.move_up)
                self.bind_all('<Left>', self.move_right)
                self.bind_all('<Right>', self.move_left)
                self.bind_all('<Up>', self.move_down)
                self.bind_all('<Down>', self.move_up)
        else:
            self.bind('<Shift-Button-4>', self.move_right)
            self.bind('<Shift-Button-5>', self.move_left)
            self.bind('<Button-4>', self.move_down)
            self.bind('<Button-5>', self.move_up)
            self.bind_all('<Left>', self.move_right)
            self.bind_all('<Right>', self.move_left)
            self.bind_all('<Up>', self.move_down)
            self.bind_all('<Down>', self.move_up)

        # Bindings for undoing
        if 'bind_undo' in kwargs:
            if kwargs['bind_undo']:
                self.bind_all('<Control-slash>', self.undo_line_callback)
                self.bind_all('<Control-Key-z>', self.undo_line_callback)
        else:
            self.bind_all('<Control-slash>', self.undo_line_callback)
            self.bind_all('<Control-Key-z>', self.undo_line_callback)

    def draw(self, event):
        """
        Processes a drawing event
        
        Parameters
        ----------
        event:
            The event to process.
        """
        if self.draw_style == 'text':
            self.set_text_pos(event)
        elif self.draw_style == 'graph':
            if self.graph_coords['x'] == None:
               self.graph_coords = dict(x=event.x,
                                        y=event.y)
            else:
                self.draw_graph(event)
        elif self.draw_style == 'triangle' or self.draw_style == 'triangleR':
            if self.triangle_coords['x'] == None:
                self.triangle_coords = dict(x=event.x,
                                            y=event.y)
            else:
                self.draw_triangle(event)
        elif self.draw_style == 'square':
            if self.square_coords['x'] == None:
                self.square_coords = dict(x=event.x,
                                          y=event.y)
            else:
                self.draw_square(event)
        else:
            self.draw_line(event=event, style=self.draw_style)

    def add_letter(self, event):
        """
        Adds a letter to a text widget on the canvas.
        
        Parameters
        ----------
        event:
            The event to process and take the charactar/symbol out of.
        """
        if self.draw_style == 'text':
            if len(self.lines_list):
                if len(self.lines_list[-1]) == 1 and self.lines_list[-1][-1].style == 'text':
                    #add letter
                    #print(event)
                    if event.keysym == 'BackSpace':
                        text=self.itemcget(self.lines_list[-1][-1].id_, 'text')[:-1]
                    else:
                        text=self.itemcget(self.lines_list[-1][-1].id_, 'text')+event.char
                    self.itemconfigure(self.lines_list[-1][-1].id_, text=text)
                    self.lines_list[-1][-1].text=text
            

    def set_text_pos(self, event):
        """
        Sets the position of a text widget on the canvas
        
        Parameters
        ----------
        event:
            The event to process and retrieve the positional information out of.
        """
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

    def draw_triangle(self, event):
        """
        Draws a triangle on the canvas

        Parameters
        ----------
        event:
            The event to process for positional data
        """
        self.lines_list.append([])
        
        x1, y1 = self.triangle_coords['x'], self.triangle_coords['y']
        x2, y2 = event.x, event.y

        triangle = Triangle(x=[x1, x2], y=[y1, y2],
                            clr=self.line_clr,
                            width=self.line_width, style=self.draw_style)

        if self.draw_style == 'triangleR':
            tr_style = 'right'
        else:
            tr_style = 'acute'

        triangle.id_ = self.create_line(triangle.get_coords(tr_style),
                                        fill=self.line_clr,
                                        smooth=False,
                                        width=self.line_width,
                                        capstyle=tk.ROUND,
                                        splinesteps=36)

        self.lines_list[-1].append(triangle)

        self.triangle_coords = dict(x=None, y=None)

    def draw_square(self, event):
        """
        """
        pass
        
        
    def draw_graph(self, event):
        """
        Draws a graph on the canvas
        
        Parameters
        ----------
        event:
            The event to process for positional data
        """
        self.lines_list.append([])

        x1 = self.graph_coords['x']
        y1 = self.graph_coords['y']
        x2, y2 = event.x, event.y

        graph = Graph(x=[x1,x2],y=[y1,y2], clr=self.line_clr,
                      width=self.line_width, style='graph')

        graph.id_ = [self.create_line(graph.get_xy_axis(),
                               fill=self.line_clr,
                               smooth=True,
                               width=self.line_width,
                               capstyle=tk.ROUND,
                               splinesteps=36)]

        for line in graph.get_support_lines():
            graph.id_.append(self.create_line(line,
                                              fill=self.line_clr,
                                              smooth=True,
                                              width=self.line_width,
                                              capstyle=tk.ROUND,
                                              splinesteps=36))

        self.lines_list[-1].append(graph)

        self.draw_text_coords('0', graph.get_origin()[0]-10, graph.get_origin()[1]+10)
        
        self.graph_coords['x']=None
        self.graph_coords['y']=None

    def draw_graph_coords(self, x, y, clr='', width=None):
        """
        Draws a graph on the canvas, using coordinates and line information
        
        Parameters
        ----------
        x:
            The x coordinates of the line
        y:
            The y coordinates of the line
        clr:
            The colour of the line
        width:
            The width of the line
        """
        self.lines_list.append([])

        l_width=width
        if l_width == None:
            l_width = self.line_width

        graph = Graph(x=x,y=y, clr=clr,
                      width=l_width, style='graph')

        graph.id_ = [self.create_line(graph.get_xy_axis(),
                               fill=clr,
                               smooth=True,
                               width=l_width,
                               capstyle=tk.ROUND,
                               splinesteps=36)]

        for line in graph.get_support_lines():
            graph.id_.append(self.create_line(line,
                                              fill=self.line_clr,
                                              smooth=True,
                                              width=self.line_width,
                                              capstyle=tk.ROUND,
                                              splinesteps=36))

        self.lines_list[-1].append(graph)

        

        #self.draw_text_coords('0', graph.get_origin()[0]-10, graph.get_origin()[1]+10)
        
        self.graph_coords['x']=None
        self.graph_coords['y']=None
        

    def draw_text_coords(self, text, x, y, clr='', font=None):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        x:
            The x coordinates of the text
        y:
            The y coordinates of the text
        clr:
            The colour of the text
        font:
            The font of the text
        """
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
        """
        Draw text on the canvas
        
        Parameters
        ----------
        The event to be processed for positional data
        """
        if self.x == None:
            self.x=event.x-(self.line_width/2)-2
            self.lines_list.append([])
        if self.y == None:
            self.y=event.y-(self.line_width/2)-2

        
        self.lines_list[-1].append(Text(id_=self.create_text(event.x, event.y,
                                                             fill=self.line_clr,
                                                             font=("tahoma", "12", "normal"),
                                                             text="Click the bubbles that are multiples of two."),
                                        x=[self.x],
                                        y=[self.y],
                                        clr=self.line_clr,
                                        style='text',
                                        width=self.line_width,
                                        text="Click the bubbles that are multiples of two.",
                                        font=("tahoma", "12", "normal")))
        
    def draw_line(self, event, clr='', style=None):
        """
        Draw a line on the canvas with specified colour and style
        
        Parameters
        ----------
        event:
            The event to be processed for positional data
        """
        l_width = self.line_width
        if clr == '':
           clr = self.line_clr
        if clr == None:
            pass
            #l_width = self.line_width*20
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
        """
        Draws lines on the canvas based on the given coordinates
        
        Parameters
        ----------
        x1:
            The start x coordinate

        y1:
            The start y coordinate

        x2:
            The end x coordinate

        y2:
            The end y coordinate

        coords:
            A prepared set of coordinates in the format as needed by the canvas. 
            This also allows a number of lines to be drawn.

        clr:
            The colour of the line(s)

        width:
            The width of the line(s)

        style:
            The style of the line(s)
        """
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
            self.lines_list[-1].append(l)
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

    def draw_shape_coords(self, x, y,
                          clr='', width=None, style=None):
        """
        Draws shapes on the canvas based on the given coordinates
        
        Parameters
        ----------
        x1:
            The start x coordinate

        y1:
            The start y coordinate

        x2:
            The end x coordinate

        y2:
            The end y coordinate

        coords:
            A prepared set of coordinates in the format as needed by the canvas. 
            This also allows a number of lines to be drawn.

        clr:
            The colour of the line(s)

        width:
            The width of the line(s)

        style:
            The style of the line(s)
        """
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

        if l_style == 'triangle':
            shape = Triangle(x=x, y=y, clr=clr,
                             style=l_style, width=l_width)
            shape.id_ = self.create_line(shape.get_coords(),
                                         fill=clr,
                                         smooth=False,
                                         width=l_width,
                                         capstyle=tk.ROUND,
                                         splinesteps=36)
        elif l_style == 'triangleR':
            shape = Triangle(x=x, y=y, clr=clr,
                             style=l_style, width=l_width)
            shape.id_ = self.create_line(shape.get_coords(type_='right'),
                                         fill=clr,
                                         smooth=False,
                                         width=l_width,
                                         capstyle=tk.ROUND,
                                         splinesteps=36)
        elif l_style == 'square':
            pass
        elif l_style == 'arrow':
            pass

        self.lines_list[-1].append(shape)
        
        self.last_coord['x'] = x[-1]
        self.last_coord['y'] = y[-1]

    def draw_straight_line(self, event, clr=''):
        """
        Draws a straight line
        
        Parameters
        ----------
        event:
            The event to be processed for positional data
        
        clr:
            The colour of the line
        """
        l_width = self.line_width
        if clr == '':
           clr = self.line_clr
        if clr == None:
            pass
            #l_width = self.line_width*20

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
        """
        Draw a dashed line
        
        Parameters
        ----------
        event:
            The event to be processed for positional data

        clr:
            The colour of the line
        """
        l_width = self.line_width
        if clr == '':
           clr = self.line_clr
        if clr == None:
            pass
            #l_width = self.line_width*20

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
        """
        Draws a dotted line
        
        Parameters
        ----------
        event:
            The event to be processed for positional data
        
        clr:
            The colour of the line
        """
        l_width = self.line_width
        if clr == '':
           clr = self.line_clr
        if clr == None:
            pass
            #l_width = self.line_width*20

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
        """
        Undoes the last drawn line or redraws all cleared lines
        
        Parameters
        ----------
        None
        """
        if len(self.lines_list) >= 1:
            for line in self.lines_list[-1]:
                if type(line.id_) == list:
                    for id_ in line.id_:
                        print(line.style)
                        self.delete(id_)
                self.delete(line.id_)
        
            del self.lines_list[-1]

            self.last_coord['x'] = self.lines_list[-1][-1].x[-1]
            self.last_coord['y'] = self.lines_list[-1][-1].y[-1]
        else:
            self.undo_clear()
        
    def undo_line_callback(self, event):
        """
        Undoes the last drawn line or redraws all cleared lines. 
        Meant to be used in bindings with keys on the keyboard.
        
        Parameters
        ----------
        event:
            The event to be processed
        
        Returns
        -------
        network: str
            The network ip
        """
        if (event.char == event.keysym or len(event.char)==1) and ('slash' in event.keysym or 'z' in event.keysym):
            try:
                self.undo_line()
            except:
                pass

    def set_draw_style(self, style: str):
        """
        Sets the style for drawing to the specified one
        
        Parameters
        ----------
        style:
            The style to be used
        """
        if style == 'text':
            self.bind('<Key>', self.add_letter)
        elif self.draw_style == 'text':
            self.unbind('<Key>')
        self.draw_style = style
                
    def set_colour(self, colour):
        """
        Sets the colour of the drawings
        
        Parameters
        ----------
        colour:
            The colour to be used for new drawings on the canvas
        """
        self.prev_line_colour = self.line_clr
        self.line_clr = colour

    def set_line_width(self, size=None, incr=None, decr=None):
        """
        Sets the line width or increments/decrements it. Throws a ValueError if 
        all arguments are left empty. The minimum width is 1 and the maximum is 99
        
        Parameters
        ----------
        size:
            The absolute value to be used for the line width
        
        incr:
            The value to increment the current width with.

        decr:
            The value to decrement the current width with.
        """
        if not(size == None):
            self.line_width = size
        elif not(incr == None):
            self.line_width += incr
        elif not(decr == None):
            self.line_width -= decr
        else:
            raise ValueError('None of the arguments have been given a value')

        if self.line_width > 99: self.line_width = 99
        elif self.line_width < 1: self.line_width = 1

    def reset_colour(self):
        """
        Resets the colour for drawings
        
        Parameters
        ----------
        None
        """
        temp_clr = self.line_clr
        self.line_clr = self.prev_line_colour
        self.prev_line_colour = temp_clr
        
    def mouse_released(self, event):
        """
        Handler to activate when the mouse button 1 is released
        
        Parameters
        ----------
        event:
            The event to be handled
        """
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
        """
        Corrects the last drawn shape
        
        Parameters
        ----------
        None
        """
        s=Shape_detector()
        x, y=[], []
        for line in self.lines_list[-1]:
            for x_ in line.x:
                x.append(x_)
            for y_ in line.y:
                y.append(y_)
        shape = s.get_shape(x=x, y=y, margin=self.margin,
                            margin_line=self.margin_line,
                            margin_circle=self.margin_circle,
                            margin_triangle=self.margin_triangle)

        if shape == 'line' or shape == 'circle' or \
           shape == 'triangle' or shape == 'rectangle':
            coords=[]
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
    
    def on_resize(self, event):
        """
        Handler to scale the canvas (and widgets if enabled) when the 
        parent widget is configured.
        
        Parameters
        ----------
        event:
            The event to be processed for configurational data
        """
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width, self.height = event.width, event.height
        
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        if self.scale_widg == True:
            # rescale all the objects tagged with the "all" tag
            self.scale("all",0,0,wscale,hscale)

    def zoom(self, event, direction="+"):
        """
        Allows zooming of the widgets of the canvas. Does not update the 
        last known coordinates yet.
        
        Parameters
        ----------
        event:
            The event to be processed for positional data.

        direction:
            The direction to zoom. 'in' or '+' will result into zooming into the canvas.
            'out' or '-' will result into zooming out of the canvas.
        """
        if direction == "in" or direction == "+":
            self.scale("all", event.x, event.y, 1.1, 1.1)
        elif direction == "out" or direction == "-":
            self.scale("all", event.x, event.y, 0.9, 0.9)

    def move_right(self, event):
        """
        Move all the widgets to the right.
        
        Parameters
        ----------
        event:
            Nothing is done with the event at this stage.
        """
        self.move("all", self.movement, 0)
        self.last_coord['x'] += self.movement

    def move_left(self, event):
        """
        Move all the widgets to the left.
        
        Parameters
        ----------
        event:
            Nothing is done with the event at this stage.
        """
        self.move("all", -self.movement, 0)
        self.last_coord['x'] -= self.movement

    def move_up(self, event):
        """
        Move all the widgets up.
        
        Parameters
        ----------
        event:
            Nothing is done with the event at this stage.
        """
        self.move("all", 0, -self.movement)
        self.last_coord['y'] -= self.movement

    def move_down(self, event):
        """
        Move all the widgets down.
        
        Parameters
        ----------
        event:
            Nothing is done with the event at this stage.
        """
        self.move("all", 0, self.movement)
        self.last_coord['y'] += self.movement

    def clear(self):
        """
        Clears all widgets on the canvas and stores them until the next clear.
        
        Parameters
        ----------
        None
        """
        self.cleared_lines = []

        for lines in self.lines_list:
            for line in lines:
                self.cleared_lines.append(line)
        self.delete('all')
        self.lines_list=[]

    def undo_clear(self):
        """
        Undoes the last clear.
        
        Parameters
        ----------
        None
        """
        for line in self.cleared_lines:
            if line.style=='pen' or line.style=='dash' or line.style=='dot':
                self.draw_line_coords(x1=line.x[0], y1=line.y[0],
                                      x2=line.x[1], y2=line.y[1],
                                      clr=line.clr, width=line.width,
                                      style=line.style)
            elif 'triangle' in line.style or line.style=='square':
                self.draw_shape_coords(x=line.x, y=line.y, clr=line.clr,
                                       width=line.width,
                                       style=line.style)
            elif line.style=='text':
                self.draw_text_coords(text=line.text, x=line.x, y=line.y,
                                      clr=line.clr, font=line.font)
            elif line.style=='graph':
                self.draw_graph_coords(x=line.x, y=line.y,
                                       clr=line.clr, width=line.width)

    def save(self, invert_clrs=False):
        """
        Saves the figure currently visible on the DrawCanvas

        Saves the drawings as a postscript and pops up a filedialog, after which it converts 
        the file into the user defined file and removes the postscript file.

        Parameters
        ----------
        None
        """
        temp_file='temp.eps'
        self.postscript(file=temp_file)
        img = Image.open(temp_file)
        name = tk.filedialog.asksaveasfilename(title='Select file',
                                            filetypes=(('png files', '*.png'),
                                                       ('pdf files', '*.pdf'),
                                                       ('jpg files', '*.jpg'),
                                                       ('all files', '*')))

        # If a name was specified, otherwise remove temp_file and continue
        if len(name) > 0:
            img.save(name)
            image_prc.change_clr(img_name=name, rgb=[255, 255, 255],
                                 new_rgb=[0, 0, 0], alpha=255)
            if invert_clrs:
                image_prc.invert_clrs(img_name=name, excl_rgb=[255, 255, 255])
        os.remove(temp_file)



    
