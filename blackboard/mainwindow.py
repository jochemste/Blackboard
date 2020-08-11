from image_prc import image_prc
from gui_utils import create_tooltip
from drawcanvas import DrawCanvas

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

        for F in (DrawPage, AdvSelPage):
            frame = F(container, self)
            self.frames[F] = frame
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
    drawcanvas: DrawCanvas
    line_colour: str
    frameBut: tk.Frame

    def __init__(self, parent, controller):
        super().__init__(parent, bg='grey')
        
        self.x = None
        self.y = None

        self.config(cursor='pencil')

        # Initialise the options frame label
        self.frameBut = tk.LabelFrame(self, text='Options', bg='grey')
        self.frameBut.config(cursor='hand1')
        self.frameBut.pack(side='left', fill='both')

        # Initialise the label frames for the separate menus inside the invisible options frame
        self.clrLabFrame = tk.LabelFrame(self.frameBut, text='Colours', bg='grey')
        self.clrLabFrame.pack(side='top', fill='both', padx=5)
        self.sizeLabFrame = tk.LabelFrame(self.frameBut, text='Size', bg='grey')
        self.sizeLabFrame.pack(side='top', fill='both', padx=5)
        self.styleLabFrame = tk.LabelFrame(self.frameBut, text='Style', bg='grey')
        self.styleLabFrame.pack(side='top', fill='both', padx=5)
        self.shapeCorLabFrame = tk.LabelFrame(self.frameBut, text='Shapes', bg='grey')
        self.shapeCorLabFrame.pack(side='top', fill='both', padx=5)
        self.menuLabFrame = tk.LabelFrame(self.frameBut, text='Menu', bg='grey')
        self.menuLabFrame.pack(side='top', fill='both', padx=5)
        
        self.bind_all('<Control-Key-s>', lambda e: self.save_figure())

        self.__init_buttons(controller)
        self.__init_drawcanvas()
        self.__init_shape_widgets(controller)
        
        
    def __init_drawcanvas(self):
        self.dc = DrawCanvas(parent=self, test='true')
        self.dc.pack(expand=True)
        self.bind('<Configure>', self.dc.on_resize)
        self.bind_all('<Button-4>', lambda e : self.__change_size(incr=1))
        self.bind_all('<Button-5>', lambda e : self.__change_size(decr=1))

    def __init_shape_widgets(self, controller):
        self.shape_correction = tk.IntVar()
        corrCheckButton = tk.Checkbutton(self.shapeCorLabFrame, text='Correct',
                                         variable=self.shape_correction,
                                         onvalue=1, offvalue=0,
                                         command=self.toggle_shape_correction,
                                         bg='grey')
        corrCheckButton.pack(side='top', fill='both', padx=5)
        self.shape_correction.set(1)

        corrScale = tk.Scale(self.shapeCorLabFrame,
                             command=self.set_shape_corr_margin,
                             bg='grey', troughcolor='grey',
                             orient=tk.HORIZONTAL,
                             showvalue=0)
        corrScale.pack(side='top', fill='both', padx=5)
        corrScale.set(self.dc.margin)

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
        self.clr_label = tk.Label(self.clrLabFrame, bg=self.dc.line_clr)
        self.clr_label.grid(column=0, row=0, padx=10, columnspan=2)
        self.clr_label.config(width=4)
        create_tooltip(self.clr_label, "Current colour")
        for but in self.clr_buttons:
            but['state'] = tk.NORMAL
        button['state'] = tk.DISABLED
        
    def select_clr(self):
        clr = askcolor(color=self.dc.line_clr)[1]
        if not(clr == None):
            self.dc.set_colour(colour=clr)
        self.clr_label.destroy()
        self.clr_label = tk.Label(self.clrLabFrame, bg=self.dc.line_clr)
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


    def toggle_shape_correction(self):
        if self.shape_correction.get() == 1:
            self.dc.correct = True
        else:
            self.dc.correct = False

    def set_shape_corr_margin(self, arg):
        self.dc.margin = int(arg)
        
                               
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

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
