from image_prc import image_prc
from gui_utils import create_tooltip
from tk_shapes import Line, Text, Graph

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image

class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_frames()
        self.bind('<Key-Escape>', self.exit_window)
        self.title('Blackboard')
        self.geometry('800x800')

    def show_frame(self, name):
        self.frames[name].tkraise()

    def __init_frames(self):
        container = ttk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1) # make the cell in grid cover the entire window
        container.grid_columnconfigure(0, weight=1) # make the cell in grid cover the entire window
        self.frames = {}

        #page = DrawPage(container, self)
        #self.frames[0] = page
        #page.addtag_all("all")
        #page.pack(fill=tk.BOTH, expand=True)

        for F in (DrawPage, AdvSelPage):
            frame = F(container, self)
            self.frames[F] = frame
            #frame.grid(row=0, column=0, sticky='nsew')
            frame.pack(fill=tk.BOTH, expand=True)

        self.show_frame(DrawPage)

    def exit_window(self, event):
        if event.keysym == 'Escape':
            self.destroy()
    
class DrawPage(tk.Frame):
    """
    A page, dedicated to drawing on a DrawCanvas
    """
    x: int
    y: int
    drawcanvas: tk.Canvas
    line_colour: str
    frameBut: tk.Frame

    def __init__(self, parent, controller):
        super().__init__(parent, bg='grey')
        self.x = None
        self.y = None
        self.config(cursor='pencil')

        self.frameBut = tk.LabelFrame(self, text='Options', bg='grey')
        self.frameBut.config(cursor='hand1')
        self.frameBut.pack(side='left', fill='both')
        self.clrLabFrame = tk.LabelFrame(self.frameBut, text='Colours', bg='grey')
        self.clrLabFrame.pack(side='top', fill='both', padx=5)
        self.sizeLabFrame = tk.LabelFrame(self.frameBut, text='Size', bg='grey')
        self.sizeLabFrame.pack(side='top', fill='both', padx=5)
        self.styleLabFrame = tk.LabelFrame(self.frameBut, text='Style', bg='grey')
        self.styleLabFrame.pack(side='top', fill='both', padx=5)
        self.menuLabFrame = tk.LabelFrame(self.frameBut, text='Menu', bg='grey')
        self.menuLabFrame.pack(side='top', fill='both', padx=5)
        
        self.bind_all('<Control-Key-s>', lambda e: self.save_figure())

        self.__init_buttons(controller)
        self.__init_drawcanvas()
        
        
    def __init_drawcanvas(self):
        self.dc = DrawCanvas(self)
        self.dc.pack(expand=True)
        self.bind('<Configure>', self.dc.on_resize)
        self.bind_all('<Button-4>', lambda e : self.__change_size(incr=1))
        self.bind_all('<Button-5>', lambda e : self.__change_size(decr=1))

    def __init_style_buttons(self, controller):
        self.style_buttons = []
        frameCol1 = tk.Frame(self.styleLabFrame, bg='grey')
        frameCol2 = tk.Frame(self.styleLabFrame, bg='grey')
        frameCol1.grid(column=0, row=1, pady=10)
        frameCol2.grid(column=1, row=1, pady=10)

        buttonPen = tk.Button(frameCol1, text=(u'\u2015'),
                              command=lambda : self.dc.set_draw_style('pen'),
                                    bg='grey')
        buttonPen.pack(side='top', fill='both', padx=5)
        create_tooltip(buttonPen, "Set style to pencil")

        buttonDash = tk.Button(frameCol2, text=(u'\u002D\u002D\u002D'),
                               command=lambda : self.dc.set_draw_style('dash'),
                                    bg='grey')
        buttonDash.pack(side='top', fill='both', padx=5)
        create_tooltip(buttonDash, "Set style to dashes")

        buttonDot = tk.Button(frameCol1, text=(u'\u002E\u002E\u002E'),
                              command=lambda : self.dc.set_draw_style('dot'),
                                    bg='grey')
        buttonDot.pack(side='top', fill='both', padx=5)
        create_tooltip(buttonDot, "Set style to dots")

        buttonText = tk.Button(frameCol2, text='A', font=('Courier', 12, 'bold'),
                               command=lambda : self.dc.set_draw_style('text'),
                                    bg='grey')
        buttonText.pack(side='top', fill='both', padx=5)
        create_tooltip(buttonText, "Set style to text typing")

        buttonGraph = tk.Button(frameCol1, text=(u'\u301C'),
                              command=lambda : self.dc.set_draw_style('graph'),
                                    bg='grey')
        buttonGraph.pack(side='top', fill='both', padx=5)
        create_tooltip(buttonGraph, "Set style to graph plotting")

        buttonSquare = tk.Button(frameCol2, text=(u'\u25A1'),
                                 command=lambda : self.dc.set_draw_style('rect'),
                                    bg='grey')
        buttonSquare.pack(side='top', fill='both', padx=5)
        create_tooltip(buttonSquare, "Set style to rectangular drawing")

    def __init_clr_buttons(self, controller):
        self.clr_buttons = []
        frameCol1 = tk.Frame(self.clrLabFrame, bg='grey')
        frameCol2 = tk.Frame(self.clrLabFrame, bg='grey')
        frameCol1.grid(column=0, row=1, pady=10)
        frameCol2.grid(column=1, row=1, pady=10)
        
        buttonColourLightgrey = tk.Button(frameCol1, text='lg',
                                    command=lambda : self.change_clr(buttonColourLightgrey,
                                                                     clr='lightgrey'),
                                    bg='lightgrey')
        buttonColourLightgrey.pack(side='top', fill='both')
        buttonColourLightgrey['state'] = tk.DISABLED
        self.clr_buttons.append(buttonColourLightgrey)
        create_tooltip(buttonColourLightgrey, "Set colour to light grey")
        
        
        buttonColourRed = tk.Button(frameCol2, text='r',
                                    command=lambda : self.change_clr(buttonColourRed,
                                                                     clr='red'),
                                    bg='red')
        buttonColourRed.pack(side='top', fill='both')
        self.clr_buttons.append(buttonColourRed)
        create_tooltip(buttonColourRed, "Set colour to red")

        buttonColourGreen = tk.Button(frameCol1, text='g',
                                    command=lambda : self.change_clr(buttonColourGreen,
                                                                     clr='green'),
                                    bg='green')
        buttonColourGreen.pack(side='top', fill='both')
        self.clr_buttons.append(buttonColourGreen)
        create_tooltip(buttonColourGreen, "Set colour to green")

        buttonColourBlue = tk.Button(frameCol2, text='b',
                                    command=lambda : self.change_clr(buttonColourBlue,
                                                                     clr='blue'),
                                    bg='blue')
        buttonColourBlue.pack(side='top', fill='both')
        self.clr_buttons.append(buttonColourBlue)
        create_tooltip(buttonColourBlue, "Set colour to blue")

        buttonColourYellow = tk.Button(frameCol1, text='y',
                                    command=lambda : self.change_clr(buttonColourYellow,
                                                                     clr='yellow'),
                                    bg='yellow')
        buttonColourYellow.pack(side='top', fill='both')
        self.clr_buttons.append(buttonColourYellow)
        create_tooltip(buttonColourYellow, "Set colour to yellow")

        buttonColourPurple = tk.Button(frameCol2, text='p',
                                    command=lambda : self.change_clr(buttonColourPurple,
                                                                     clr='purple'),
                                    bg='purple')
        buttonColourPurple.pack(side='top', fill='both')
        self.clr_buttons.append(buttonColourPurple)
        create_tooltip(buttonColourPurple, "Set colour to purple")

        buttonErase = tk.Button(self.clrLabFrame, text='Eraser',
                                command=lambda : self.change_clr(buttonErase,
                                                                     clr=None),
                                bg=None)
        buttonErase.grid(column=0, row=3, padx=10, columnspan=2, sticky='n')
        self.clr_buttons.append(buttonErase)
        create_tooltip(buttonErase, "Use the eraser")

        buttonSelClr = tk.Button(self.clrLabFrame, text='Select\ncolour',
                                command=lambda : {self.select_clr()},
                                bg='white')
        buttonSelClr.grid(column=0, row=2, padx=10, columnspan=2, sticky='n')
        self.clr_buttons.append(buttonSelClr)
        create_tooltip(buttonSelClr, "Select a custom colour")
        
        self.__init_clr_label(clr='lightgrey')

    def __init_size_buttons(self, controller):
        buttonPlus = tk.Button(self.sizeLabFrame, text='+',
                                command=lambda : self.__change_size(incr=1),
                                bg='grey')
        buttonPlus.pack(side='top', fill='both', padx=10)
        create_tooltip(buttonPlus, "Increase pen size")

        buttonMin = tk.Button(self.sizeLabFrame, text='-',
                                command=lambda : self.__change_size(decr=1),
                                bg='grey')
        buttonMin.pack(side='top', fill='both', padx=10)
        create_tooltip(buttonMin, "Decrease pen size")

        buttonReset = tk.Button(self.sizeLabFrame, text='reset',
                                command=lambda : self.__change_size(size=2),
                                bg='grey')
        buttonReset.pack(side='top', fill='both', padx=10)
        create_tooltip(buttonReset, "Reset pen size")
        
        self.__init_size_label(size=2)
        
    def __init_menu_buttons(self, controller):
        buttonUndo = tk.Button(self.menuLabFrame, text='Undo',
                               command=lambda : {self.dc.undo_line()},
                               bg='grey')
        buttonUndo.pack(side='top', fill='both', padx=10)
        create_tooltip(buttonUndo, "Undo last move")
        
        buttonSave = tk.Button(self.menuLabFrame, text='Save',
                               command=lambda : {self.save_figure()},
                               bg='grey')
        buttonSave.pack(side='top', fill='both', padx=10)
        create_tooltip(buttonSave, "Save drawing")

        buttonClear = tk.Button(self.menuLabFrame, text='Clear',
                               command=lambda : {self.dc.clear()},
                               bg='grey')
        buttonClear.pack(side='top', fill='both', padx=10)
        create_tooltip(buttonClear, "Clear the screen")

        buttonExit = tk.Button(self.menuLabFrame, text='Exit',
                                 command=lambda : controller.destroy(), bg='grey')
        buttonExit.pack(side='top', fill='both', padx=10)
        create_tooltip(buttonExit, "Exit the program")

        
    def __init_buttons(self, controller):
        self.__init_clr_buttons(controller)
        self.__init_size_buttons(controller)
        self.__init_style_buttons(controller)
        self.__init_menu_buttons(controller)

    def __init_size_label(self, size):
        self.size_label = tk.Label(self.sizeLabFrame, text=str(size)+'px',
                                   bg='grey')
        self.size_label.pack(side='top', fill='both', padx=10)
        create_tooltip(self.size_label, "Current size")

    def __init_clr_label(self, clr):
        self.clr_label = tk.Label(self.clrLabFrame, bg=str(clr))
        self.clr_label.grid(column=0, row=0, padx=10, columnspan=2)
        self.clr_label.config(width=4)
        create_tooltip(self.clr_label, "Current colour")

    def __change_size(self, size=None, incr=None, decr=None):
        self.dc.set_line_width(size=size, incr=incr, decr=decr)
        self.size_label.destroy()
        self.size_label = tk.Label(self.sizeLabFrame, text=str(self.dc.line_width)+'px',
                                   bg='grey')
        self.size_label.pack(side='bottom', fill='both', padx=10)
        create_tooltip(self.size_label, "Current size")
        
    def change_clr(self, button, clr):
        self.dc.set_colour(colour=clr)
        self.clr_label.destroy()
        self.clr_label = tk.Label(self.clrLabFrame, bg=self.dc.line_colour)
        self.clr_label.grid(column=0, row=0, padx=10, columnspan=2)
        self.clr_label.config(width=4)
        create_tooltip(self.clr_label, "Current colour")
        for but in self.clr_buttons:
            but['state'] = tk.NORMAL
        button['state'] = tk.DISABLED
        
    def select_clr(self):
        clr = askcolor(color=self.dc.line_colour)[1]
        if not(clr == None):
            self.dc.set_colour(colour=clr)
        self.clr_label.destroy()
        self.clr_label = tk.Label(self.clrLabFrame, bg=self.dc.line_colour)
        self.clr_label.grid(column=0, row=0, padx=10, columnspan=2)
        self.clr_label.config(width=4)
        
    def save_figure(self):
        temp_file='temp.eps'
        self.dc.postscript(file=temp_file)
        img = Image.open(temp_file)
        name = tk.filedialog.asksaveasfilename(title='Select file',
                                            filetypes=(('png files', '*.png'),
                                                       ('pdf files', '*.pdf'),
                                                       ('all files', '*')))

        if len(name) > 0:
            img.save(name)
            image_prc.change_clr(img_name=name, rgb=[255, 255, 255],
                                 new_rgb=[0, 0, 0], alpha=255)
            #image_prc.invert_clrs(img_name=name, excl_rgb=[255, 255, 255])
        os.remove(temp_file)
        
                               
    def update_drawcanvas(self):
        newcanvas = self.dc
        self.dc.destroy()
        self.dc = newcanvas

    
class AdvSelPage(ttk.Frame):
    """
    Advanced selection page to insert graph templates and such
    """

    def __init__(self, parent, controller):
        super().__init__(parent)

class DrawCanvas(tk.Canvas):
    """
    A custom Canvas to draw on
    """
    x: int
    y: int
    drawcanvas: tk.Canvas
    line_colour: str
    prev_line_colour: str
    line_width: int
    height: int
    width: int
    lines_list: list
    cleared_lines: list
    draw_style: str

    def __init__(self, parent):
        super().__init__(parent, bg='black', highlightthickness=0)
        self.x = None
        self.y = None
        self.line_colour = 'lightgrey'
        self.line_width = 2
        self.lines_list = []
        self.cleared_lines = []
        self.draw_style = 'pen'
        self.last_coord = dict(x= None, y= None)
        self.graph_coords = dict(x= None, y= None)

        self.bind('<Shift-Button-1>', self.draw_straight_line)
        self.bind('<B1-Motion>', self.draw)
        self.bind('<Button-1>', self.draw)
        self.bind('<ButtonRelease-1>', self.mouse_released)
        self.bind('<Button-2>', self.draw_text)
        self.bind('<B3-Motion>', lambda e : {self.draw_line(event=e, clr=None)})
        self.bind('<Button-3>', lambda e : {self.draw_line(event=e, clr=None)})
        self.bind('<ButtonRelease-3>', lambda : {self.set_colour(self.line_colour)})
        self.bind('<ButtonRelease-3>', self.mouse_released)
        self.bind_all('<Control-slash>', self.undo_line_callback)
        self.bind_all('<Control-Key-z>', self.undo_line_callback)
        self.bind('<Key>', self.add_letter)
        self.update()
        self.height =  self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.focus_set()
        self.addtag_all('all')

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
                                                             fill=self.line_colour,
                                                             font=("tahoma", "12", "normal"),
                                                             text=""),
                                        x=[self.x],
                                        y=[self.y],
                                        clr=self.line_colour,
                                        style='text',
                                        width=self.line_width,
                                        text="",
                                        font=("tahoma", "12", "normal")))
        
    def draw_graph(self, event):
        self.lines_list.append([])

        x1 = self.graph_coords['x']
        y1 = self.graph_coords['y']
        x2, y2 = event.x, event.y

        graph = Graph(x=[x1,x2],y=[y1,y2], clr=self.line_colour,
                      width=self.line_width, style='graph')

        graph.id_ = self.create_line(graph.get_xy_axis(),
                               fill=self.line_colour,
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
            clr = self.line_colour

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
                                                             fill=self.line_colour,
                                                             font=("tahoma", "12", "normal"),
                                                             text="Click the bubbles that are multiples of two."),x=[self.x], y=[self.y], clr=self.line_colour, style='text', width=self.line_width,
                                        text="Click the bubbles that are multiples of two.", font=("tahoma", "12", "normal")))
        
    def draw_line(self, event, clr='', style=None):
        l_width = self.line_width
        if clr == '':
           clr = self.line_colour
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
        
    def draw_line_coords(self, x1, y1, x2, y2, clr='', width=None, style=None):
        if width ==  None:
            l_width = self.line_width
        else:
            l_width = width
        if style == None:
            l_style=self.draw_style
        else:
            l_style = style

        if clr == '':
           clr = self.line_colour
        self.lines_list.append([])

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
                                      splinesteps=36,
                                      dash=dash),
                 x=[x1, x2], y=[y1, y2], clr=clr, width=l_width,
                 style=l_style)
        self.lines_list[-1].append(l)

        self.last_coord['x'] = x2
        self.last_coord['y'] = y2

    def draw_straight_line(self, event, clr=''):
        l_width = self.line_width
        if clr == '':
           clr = self.line_colour
        if clr == None:
            l_width = self.line_width*20

        self.lines_list.append([])

        
        x1, y1 = self.last_coord['x'], self.last_coord['y']
        x2, y2 = event.x-2, event.y-2

        self.x, self.y = event.x, event.y

        if self.draw_style == 'dash':
            dash = (int(10*(l_width/2)), int(10*(l_width/2)))
        elif self.draw_style == 'dot':
            dash=(1, int(10*(l_width/2)))
        else:
            dash=()


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
           clr = self.line_colour
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
           clr = self.line_colour
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
        self.prev_line_colour = self.line_colour
        self.line_colour = colour

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
        temp_clr = self.line_colour
        self.line_colour = self.prev_line_colour
        self.prev_line_colour = temp_clr
        
    def mouse_released(self, event):
        self.last_coord['x'] = self.x
        self.last_coord['y'] = self.y
        self.x = None
        self.y = None

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


    
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
