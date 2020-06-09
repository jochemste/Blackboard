from image_prc import image_prc

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
        self.bind_all('<Key>', self.exit_window)
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
        #print(event)
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
        self.frameBut = tk.Frame(self)
        self.frameBut.config(cursor='hand1')
        self.frameBut.pack(side='left')
        self.__init_buttons(controller)
        self.__init_drawcanvas()
        
        
    def __init_drawcanvas(self):
        self.dc = DrawCanvas(self)
        self.dc.pack(expand=True)
        self.bind('<Configure>', self.dc.on_resize)

    def __init_buttons(self, controller):
        buttonExit = tk.Button(self.frameBut, text='Exit',
                                 command=lambda : controller.destroy(), bg='grey')
        buttonExit.pack(side='top', fill='both')
        
        buttonColourRed = tk.Button(self.frameBut, text='Red',
                                    command=lambda : {self.dc.set_colour('red')},
                                    bg='red')
        buttonColourRed.pack(side='top', fill='both')

        buttonColourLightgrey = tk.Button(self.frameBut, text='Lightgrey',
                                    command=lambda : self.dc.set_colour('lightgrey'),
                                    bg='lightgrey')
        buttonColourLightgrey.pack(side='top', fill='both')

        #buttonColourWhite = tk.Button(self.frameBut, text='White',
        #                            command=lambda : self.dc.set_colour('white'),
        #                            bg='white')
        #buttonColourWhite.pack(side='top', fill='both')

        buttonColourGreen = tk.Button(self.frameBut, text='Green',
                                    command=lambda : self.dc.set_colour('green'),
                                    bg='green')
        buttonColourGreen.pack(side='top', fill='both')

        buttonColourBlue = tk.Button(self.frameBut, text='Blue',
                                    command=lambda : self.dc.set_colour('blue'),
                                    bg='blue')
        buttonColourBlue.pack(side='top', fill='both')

        buttonErase = tk.Button(self.frameBut, text='Eraser',
                                command=lambda : {self.dc.set_colour(None)},
                                bg='grey')
        buttonErase.pack(side='top', fill='both')

        buttonSelClr = tk.Button(self.frameBut, text='Select colour',
                                command=lambda : {self.select_clr()},
                                bg='grey')
        buttonSelClr.pack(side='top', fill='both')

        buttonClear = tk.Button(self.frameBut, text='Clear',
                               command=lambda : {self.dc.clear()},
                               bg='grey')
        buttonClear.pack(side='top', fill='both')

        buttonClear = tk.Button(self.frameBut, text='Undo',
                               command=lambda : {self.dc.undo_line()},
                               bg='grey')
        buttonClear.pack(side='top', fill='both')

        buttonSave = tk.Button(self.frameBut, text='Save',
                               command=lambda : {self.save_figure()},
                               bg='grey')
        buttonSave.pack(side='top', fill='both')
        

    def select_clr(self):
        clr = askcolor(color=self.dc.line_colour)[1]
        print('selected colour:', clr)
        if not(clr == None):
            self.dc.set_colour(colour=clr)
        
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
        self.draw_style = 'free'

        self.bind('<B1-Motion>', self.draw)
        self.bind('<Button-1>', self.draw)
        #self.bind('<B1-Motion>', self.draw_line)
        #self.bind('<Button-1>', self.draw_line)
        self.bind('<ButtonRelease-1>', self.mouse_released)
        self.bind('<Button-2>', self.draw_text)
        self.bind('<B3-Motion>', lambda e : {self.draw_line(event=e, clr=None)})
        self.bind('<Button-3>', lambda e : {self.draw_line(event=e, clr=None)})
        self.bind('<ButtonRelease-3>', lambda : {self.set_colour(self.line_colour)})
        self.bind('<ButtonRelease-3>', self.mouse_released)
        self.bind_all('<Control-slash>', self.undo_line_callback)
        self.bind_all('<Control-Key>', self.undo_line_callback)
        self.update()
        self.height =  self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.addtag_all('all')

    def draw(self, event):
        if self.draw_style == 'free':
            self.draw_line(event)
        elif self.draw_style == 'text':
            self.draw_text(event)
        
    def draw_text(self, event):
        print('d.t.:', event)
        
    def draw_line(self, event, clr=''):
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
                                      splinesteps=36),
                 x=[x1, x2], y=[y1, y2], clr=clr, width=l_width,
                 style=self.draw_style)
        self.lines_list[-1].append(l)
        
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

        l = Line(id_=self.create_line(x1,y1,
                                  x2, y2,
                                  fill=clr,
                                  smooth=True,
                                  width=l_width,
                                  capstyle=tk.ROUND,
                                  splinesteps=36),
                 x=[x1, x2], y=[y1, y2], clr=clr, width=l_width,
                 style=l_style)
        self.lines_list[-1].append(l)
    
    def undo_line(self):
        if len(self.lines_list) >= 1:
            for line in self.lines_list[-1]:
                self.delete(line.id_)
        
            del self.lines_list[-1]
        else:
            for line in self.cleared_lines:
                self.draw_line_coords(x1=line.x[0], y1=line.y[0],
                                      x2=line.x[1], y2=line.y[1],
                                      clr=line.clr, width=line.width,
                                      style=line.style)
                #self.draw_line_coords(x1=line[0], y1=line[1],
                #                      x2=line[2], y2=line[3])
        
    def undo_line_callback(self, event):
        #print(event)
        if (event.char == event.keysym or len(event.char)==1) and ('slash' in event.keysym or 'z' in event.keysym):
            self.undo_line()
        else:
            print('u.l.c:', event)
            self.undo_line()

    def key_e_callback(self, event):
        """
        Key event handler
        """
        print('k.e.h.:', event)
        if (event.char == event.keysym or len(event.char)==1):
            if ('slash' in event.keysym or 'z' in event.keysym):
                self.undo_line()

    def set_draw_style(self, style: str):
        self.draw_style = style
                
    def set_colour(self, colour):
        self.prev_line_colour = self.line_colour
        self.line_colour = colour

    def reset_colour(self):
        temp_clr = self.line_colour
        self.line_colour = self.prev_line_colour
        self.prev_line_colour = temp_clr
        
    def mouse_released(self, event):
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
        
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
