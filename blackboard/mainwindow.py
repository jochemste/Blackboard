import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.__init_frames()
        self.bind_all('<Key>', self.exit_window)

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
        

        for F in (DrawPage, AnotherPage):
            frame = F(container, self)
            self.frames[F] = frame
            #frame.grid(row=0, column=0, sticky='nsew')
            frame.pack(fill=tk.BOTH, expand=True)

        self.show_frame(DrawPage)

    def exit_window(self, event):
        print(event)
        if event.keysym == 'Escape':
            self.destroy()
    
class DrawPage(tk.Frame):
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
        #self.drawcanvas = tk.Canvas(self)
        #self.drawcanvas.create_line(5, 5, 10, 10)
        #self.drawcanvas.grid(row=0, column=0, sticky='nsew')
        #self.drawcanvas.addtag_all('all')
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

        buttonColourWhite = tk.Button(self.frameBut, text='White',
                                    command=lambda : self.dc.set_colour('white'),
                                    bg='white')
        buttonColourWhite.pack(side='top', fill='both')

        buttonColourGreen = tk.Button(self.frameBut, text='Green',
                                    command=lambda : self.dc.set_colour('green'),
                                    bg='green')
        buttonColourGreen.pack(side='top', fill='both')

        buttonColourBlue = tk.Button(self.frameBut, text='Blue',
                                    command=lambda : self.dc.set_colour('blue'),
                                    bg='blue')
        buttonColourBlue.pack(side='top', fill='both')

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
        

    def save_figure(self):
        self.dc.postscript(file='temp.eps')
        img = Image.open('temp.eps')
        name = tk.filedialog.asksaveasfilename(title='Select file',
                                            filetypes=(('png files', '*.png'),
                                                       ('pdf files', '*.pdf'),
                                                       ('all files', '*')))
        img.save(name)
        
                               
    def update_drawcanvas(self):
        newcanvas = self.dc
        self.dc.destroy()
        self.dc = newcanvas

    
class AnotherPage(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

class DrawCanvas(tk.Canvas):
    x: int
    y: int
    drawcanvas: tk.Canvas
    line_colour: str
    prev_line_colour: str
    line_width: int
    height: int
    width: int
    line_ids: list

    def __init__(self, parent):
        super().__init__(parent, bg='black', highlightthickness=0)
        self.x = None
        self.y = None
        self.line_colour = 'white'
        self.line_width = 5
        self.line_ids = []

        self.bind('<B1-Motion>', self.draw_line)
        self.bind('<ButtonRelease-1>', self.mouse_released)
        self.bind('<B3-Motion>', lambda e : {self.draw_line(event=e, clr='green')})
        self.bind('<ButtonRelease-3>', lambda : {self.set_colour(self.line_colour)})
        self.bind('<ButtonRelease-3>', self.mouse_released)
        self.bind_all('<Control-slash>', self.undo_line_callback)
        self.bind_all('<Control-Key>', self.undo_line_callback)
        self.update()
        self.height =  self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.addtag_all('all')

    def draw_line(self, event, clr=''):
        print(event)
        if clr == '':
           clr = self.line_colour
        if self.x == None:
            self.x=event.x
            self.line_ids.append([])
        if self.y == None:
            self.y=event.y
        x1, y1 = self.x, self.y
        x2, y2 = event.x, event.y
        self.x, self.y = event.x, event.y
        self.line_ids[-1].append(self.create_line(x1,y1,
                                                  x2, y2,
                                                  fill=clr,
                                                  smooth=True,
                                                  width=self.line_width))
        

    def undo_line(self):
        if len(self.line_ids):
            for id in self.line_ids[-1]:
                self.delete(id)
        
            del self.line_ids[-1]
        
    def undo_line_callback(self, event):
        print(event)
        if (event.char == event.keysym or len(event.char)==1) and ('slash' in event.keysym or 'z' in event.keysym):
            self.undo_line()
        else:
            self.undo_line()

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
        self.scale("all",0,0,wscale,hscale)

    def clear(self):
        self.delete('all')

        
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
