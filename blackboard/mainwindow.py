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
        """
        Class constructor
        
        Parameters
        ----------
        *args:
            pass
        **kwargs:
            pass
        """
        super().__init__(*args, **kwargs)
        self.__init_frames()
        self.bind('<Key-Escape>', self.exit_window)
        self.title('Blackboard')
        self.geometry('900x900')

    def show_frame(self, name):
        """
        Shows the frame with the given name.
        
        Parameters
        ----------
        name: str
            The name of the frame
        """
        self.frames[name].tkraise()

    def __init_frames(self):
        """
        Initialises the frames
        """
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
        """
        Event handler to exit the window. 
        Destroys the window when the Escape key is used.
        
        Parameters
        ----------
        event:
            The event to handle
        """
        if event.keysym == 'Escape':
            self.frames["DrawPage"].log_setting('settings.txt')
            self.destroy()
    
class DrawPage(tk.Frame):
    """
    A page/frame, dedicated to drawing on a DrawCanvas and 
    changing the DrawCanvas settings.
    """
    x: int
    y: int
    drawcanvas: DrawCanvas
    line_colour: str
    frameBut: tk.Frame

    def __init__(self, parent, controller):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
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

        
        self.__init_drawcanvas()
        self.__init_buttons(controller)
        self.__init_shape_widgets(controller)
        self.import_setting('settings.txt')
        
        
    def __init_drawcanvas(self):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.dc = DrawCanvas(parent=self, test='true')
        self.dc.pack(expand=True)
        self.bind('<Configure>', self.dc.on_resize)
        #self.bind_all('<Button-4>', lambda e : self.__change_size(incr=1))
        #self.bind_all('<Button-5>', lambda e : self.__change_size(decr=1))
        #self.dc.bind('<Control-Button-4>', lambda e : self.dc.zoom(event=e, direction="+"))
        #self.dc.bind('<Control-Button-5>', lambda e : self.dc.zoom(event=e, direction="-"))

    def __init_shape_widgets(self, controller):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.scale_drawing = tk.IntVar()
        scaleCheckButton = tk.Checkbutton(self.shapeCorLabFrame, text='Scale',
                                         variable=self.scale_drawing,
                                         onvalue=1, offvalue=0,
                                         command=self.toggle_scaling,
                                         bg='grey')
        scaleCheckButton.pack(side='top', fill='both', padx=5)
        if self.dc.scale_widg == False:
            self.scale_drawing.set(0)
        else:
            self.scale_drawing.set(1)
        create_tooltip(scaleCheckButton, "Enable/Disable scaling on window resize")
        
        self.shape_correction = tk.IntVar()
        corrCheckButton = tk.Checkbutton(self.shapeCorLabFrame, text='Correct',
                                         variable=self.shape_correction,
                                         onvalue=1, offvalue=0,
                                         command=self.toggle_shape_correction,
                                         bg='grey')
        corrCheckButton.pack(side='top', fill='both', padx=5)
        create_tooltip(corrCheckButton, "Enable/Disable shape correction")

        if self.dc.correct == True:
            self.shape_correction.set(1)
        else:
            self.shape_correction.set(0)

        corrLnScale = tk.Scale(self.shapeCorLabFrame,
                             command=self.set_shape_corr_margin_ln,
                             bg='grey', troughcolor='grey',
                             orient=tk.HORIZONTAL,
                             showvalue=0,
                             label='Line',
                             from_=1,
                             to=100)
        corrLnScale.pack(side='top', fill='both', padx=5)
        corrLnScale.set(self.dc.margin_line)
        create_tooltip(corrLnScale, "Set line correction sensitivity")

        corrCrclScale = tk.Scale(self.shapeCorLabFrame,
                             command=self.set_shape_corr_margin_crcl,
                             bg='grey', troughcolor='grey',
                             orient=tk.HORIZONTAL,
                             showvalue=0,
                             label='Circle',
                             from_=1,
                             to=100)
        corrCrclScale.pack(side='top', fill='both', padx=5)
        corrCrclScale.set(self.dc.margin_circle)
        create_tooltip(corrCrclScale, "Set circle correction sensitivity")


    def __init_style_buttons(self, controller):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
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
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
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
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.sizeScale = tk.Scale(self.sizeLabFrame,
                             command=self.set_size,
                             bg='grey', troughcolor='grey',
                             orient=tk.VERTICAL,
                             showvalue=0,
                             #label='Size',
                             from_=99,
                             to=1)
        self.sizeScale.pack(side='left', fill='both', padx=5)
        self.sizeScale.set(self.dc.line_width)
        create_tooltip(self.sizeScale, "Set the pen width")
        
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

        #buttonReset = tk.Button(self.sizeLabFrame, text='reset',
        #                        command=lambda : self.__change_size(size=2),
        #                        bg='grey')
        #buttonReset.pack(side='right', fill='both', padx=10)
        #create_tooltip(buttonReset, "Reset pen size")
        
        self.__init_size_label(size=2)
        
    def __init_menu_buttons(self, controller):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
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
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.__init_clr_buttons(controller)
        self.__init_size_buttons(controller)
        self.__init_style_buttons(controller)
        self.__init_menu_buttons(controller)

    def __init_size_label(self, size):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.size_label = tk.Label(self.sizeLabFrame, text=str(size)+'px',
                                   bg='grey')
        self.size_label.pack(side='left', fill='both', padx=10)
        create_tooltip(self.size_label, "Current size")

    def __init_clr_label(self, clr):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.clr_label = tk.Label(self.clrLabFrame, bg=str(clr))
        self.clr_label.grid(column=0, row=0, padx=10, columnspan=2)
        self.clr_label.config(width=4)
        create_tooltip(self.clr_label, "Current colour")

    def __change_size(self, size=None, incr=None, decr=None):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.dc.set_line_width(size=size, incr=incr, decr=decr)
        self.size_label.destroy()
        self.size_label = tk.Label(self.sizeLabFrame, text=str(self.dc.line_width)+'px',
                                   bg='grey')
        self.size_label.pack(side='left', fill='both', padx=10)
        create_tooltip(self.size_label, "Current size")
        self.sizeScale.set(self.dc.line_width)
        
    def change_clr(self, button, clr):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
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
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        clr = askcolor(color=self.dc.line_clr)[1]
        if not(clr == None):
            self.dc.set_colour(colour=clr)
        self.clr_label.destroy()
        self.clr_label = tk.Label(self.clrLabFrame, bg=self.dc.line_clr)
        self.clr_label.grid(column=0, row=0, padx=10, columnspan=2)
        self.clr_label.config(width=4)
        
    def save_figure(self):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
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
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        if self.shape_correction.get() == 1:
            self.dc.correct = True
        else:
            self.dc.correct = False

    def toggle_scaling(self):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        if self.scale_drawing.get() == 1:
            self.dc.scale_widg = True
        else:
            self.dc.scale_widg = False

    def set_shape_corr_margin(self, arg):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.dc.margin = int(arg)

    def set_shape_corr_margin_ln(self, arg):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.dc.margin_line = int(arg)

        
    def set_shape_corr_margin_crcl(self, arg):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.dc.margin_circle = int(arg)
        
    def set_shape_corr_margin_trn(self, arg):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.dc.margin_triangle = int(arg)

    def set_size(self, arg):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        self.__change_size(size=int(arg))
        
    def update_drawcanvas(self):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        newcanvas = self.dc
        self.dc.destroy()
        self.dc = newcanvas

    def log_setting(self, logfile):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        #self.line_colour
        #draw_style
        #margin_circle
        #margin_line
        #scaling
        #shape_correction
        
        pass

    def import_setting(self, logfile):
        """
        Gets the network ip, omitting the part after the last '.'
        
        Parameters
        ----------
        None
        
        Returns
        -------
        network: str
            The network ip
        """
        pass

    
class AdvSelPage(ttk.Frame):
    """
    Advanced selection page to insert graph templates and such
    """

    def __init__(self, parent, controller):
        """
        Class constructor
        """
        super().__init__(parent)

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
