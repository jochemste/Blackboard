from gui_utils import create_tooltip, Entry_w_Placeholder
from drawcanvas import DrawCanvas
from file_handler import File_handler
import math

import os
import tkinter as tk
from tkinter import ttk
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
        self.__init_menu()
        self.bind('<Key-Escape>', self.exit_window)
        self.bind('<Control-Key-d>', self.exit_window)
        self.title('Blackboard')
        #self.geometry('1000x1000')
        self.protocol("WM_DELETE_WINDOW", self.exit_window)


    def __init_menu(self):
        """
        """
        menuBar = tk.Menu(self, bg='grey')

        menuFile = tk.Menu(menuBar, tearoff=0)
        menuFile.add_command(label='Save <C-s>',
                             command=self.frames[DrawPage].save_figure)
        menuFile.add_command(label='Exit <Esc>',
                             command=self.exit_window)
        menuBar.add_cascade(label='File', menu=menuFile)
        
        menuEdit = tk.Menu(menuBar, tearoff=0)
        menuEdit.add_command(label='Undo <C-/><C-z>',
                             command=self.frames[DrawPage].dc.undo_line)
        menuEdit.add_command(label='Clear',
                             command=self.frames[DrawPage].dc.clear)
        menuBar.add_cascade(label='Edit', menu=menuEdit)

        menuPages = tk.Menu(menuBar, tearoff=0)
        menuPages.add_command(label='Home',
                              command=lambda:self.show_frame(DrawPage))
        menuPages.add_command(label='Advanced options',
                              command=lambda:self.show_frame(AdvSelPage))
        menuBar.add_cascade(label='Pages', menu=menuPages)

        menuStyle = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Styles', menu=menuStyle)

        self.config(menu=menuBar)
        

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
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(DrawPage)

    def call_function(self, member, function, p1, p2, p3=None, p4=None):
        """
        Allows members to call functions from other members
        """
        function(self.frames[member], p1, p2, p3, p4)

    def exit_window(self, event=None):
        """
        Event handler to exit the window. 
        Destroys the window when the Escape key is used.
        
        Parameters
        ----------
        event:
            The event to handle
        """
        self.frames[DrawPage].log_setting('settings.txt')
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
        frameCol3 = tk.Frame(self.styleLabFrame, bg='grey')
        frameCol1.grid(column=0, row=1, pady=10)
        frameCol2.grid(column=1, row=1, pady=10)
        frameCol3.grid(column=0, row=2, columnspan=2, pady=10)

        self.style_options = {u'\u2015': 'pen',
                              u'\u002D\u002D\u002D': 'dash',
                              u'\u002E\u002E\u002E': 'dot',
                              'A': 'text',
                              u'\u25B2': 'triangle',
                              u'\u25E3': 'triangleR',
                              u'\u221F': 'graph',
                              u'\u25A1': 'square',
                              u'\u2B05': 'arrow'}

        styleslist = []
        for style in self.style_options.items():
            styleslist.append(style[0])
        
        self.styleComboBox = ttk.Combobox(frameCol3,
                                          values=styleslist,
                                          width=10,
                                          state='readonly')
        self.styleComboBox.pack(side='top', fill='both', padx=5)
        self.styleComboBox.set(styleslist[0])
        self.styleComboBox.bind('<<ComboboxSelected>>', lambda e:\
                           self.change_style(self.style_options[self.styleComboBox.get()]))
        #                   self.dc.set_draw_style(self.style_options[self.styleComboBox.get()]))

        buttonPen = tk.Button(frameCol1, text=(u'\u2015'),
                              command=lambda : (self.change_style('pen'),
                                                #self.dc.set_draw_style('pen'),
                                                self.styleComboBox.set(u'\u2015')),
                                    bg='grey')
        buttonPen.pack(side='top', fill='both', padx=5)
        self.style_buttons.append(buttonPen)
        create_tooltip(buttonPen, "Set style to pencil")

        buttonDash = tk.Button(frameCol2, text=(u'\u002D\u002D\u002D'),
                               command=lambda : (self.change_style('dash'),
                                                #self.dc.set_draw_style('dash'),
                                                 self.styleComboBox.set(u'\u002D\u002D\u002D')),
                                    bg='grey')
        buttonDash.pack(side='top', fill='both', padx=5)
        self.style_buttons.append(buttonDash)
        create_tooltip(buttonDash, "Set style to dashes")

        buttonDot = tk.Button(frameCol1, text=(u'\u002E\u002E\u002E'),
                              command=lambda : (self.change_style('dot'),
                                                #self.dc.set_draw_style('dot'),
                                                self.styleComboBox.set(u'\u002E\u002E\u002E')),
                                    bg='grey')
        buttonDot.pack(side='top', fill='both', padx=5)
        self.style_buttons.append(buttonDot)
        create_tooltip(buttonDot, "Set style to dots")

        buttonText = tk.Button(frameCol2, text='A', font=('Courier', 12, 'bold'),
                               command=lambda : (self.change_style('text'),
                                                #self.dc.set_draw_style('text'),
                                                 self.styleComboBox.set('A')),
                                    bg='grey')
        buttonText.pack(side='top', fill='both', padx=5)
        self.style_buttons.append(buttonText)
        create_tooltip(buttonText, "Set style to text typing")

        buttonTriangle = tk.Button(frameCol1, text=(u'\u25B2'),
                              command=lambda : (self.change_style('triangle'),
                                                #self.dc.set_draw_style('triangle'),
                                                 self.styleComboBox.set(u'\u25B2')),
                                    bg='grey')
        buttonTriangle.pack(side='top', fill='both', padx=5)
        self.style_buttons.append(buttonTriangle)
        create_tooltip(buttonTriangle, "Set style to acute triangles")

        buttonTriangleR = tk.Button(frameCol2, text=(u'\u25E3'),
                              command=lambda : (self.change_style('triangleR'),
                                                #self.dc.set_draw_style('triangleR'),
                                                 self.styleComboBox.set(u'\u25E3')),
                                    bg='grey')
        buttonTriangleR.pack(side='top', fill='both', padx=5)
        self.style_buttons.append(buttonTriangleR)
        create_tooltip(buttonTriangleR, "Set style to right triangles")

        buttonGraph = tk.Button(frameCol1, text=(u'\u221F'),
                              command=lambda : (self.change_style('graph'),
                                                #self.dc.set_draw_style('graph'),
                                                 self.styleComboBox.set(u'\u221F')),
                                    bg='grey')
        buttonGraph.pack(side='top', fill='both', padx=5)
        self.style_buttons.append(buttonGraph)
        create_tooltip(buttonGraph, "Set style to graph plotting")

        buttonSquare = tk.Button(frameCol2, text=(u'\u25A1'),
                                 command=lambda : (self.change_style('square'),
                                                #self.dc.set_draw_style('square'),
                                                 self.styleComboBox.set(u'\u25A1')),
                                    bg='grey')
        buttonSquare.pack(side='top', fill='both', padx=5)
        self.style_buttons.append(buttonSquare)
        create_tooltip(buttonSquare, "Set style to rectangular drawing")

        buttonArrow = tk.Button(frameCol2, text=(u'\u2B05'),
                                 command=lambda : (self.change_style('arrow'),
                                                   #self.dc.set_draw_style('arrow'),
                                                   self.styleComboBox.set(u'\u2B05')),
                                    bg='grey')
        buttonArrow.pack(side='top', fill='both', padx=5)
        self.style_buttons.append(buttonArrow)
        create_tooltip(buttonArrow, "Set style to arrow drawing")

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
                
        #buttonUndo = tk.Button(self.menuLabFrame, text='Undo',
        #                       command=lambda : {self.dc.undo_line()},
        #                       bg='grey')
        #buttonUndo.pack(side='top', fill='both', padx=10)
        #create_tooltip(buttonUndo, "Undo last move")
        
        #buttonSave = tk.Button(self.menuLabFrame, text='Save',
        #                       command=lambda : {self.save_figure()},
        #                       bg='grey')
        #buttonSave.pack(side='top', fill='both', padx=10)
        #create_tooltip(buttonSave, "Save drawing")

        #buttonClear = tk.Button(self.menuLabFrame, text='Clear',
        #                       command=lambda : {self.dc.clear()},
        #                       bg='grey')
        #buttonClear.pack(side='top', fill='both', padx=10)
        #create_tooltip(buttonClear, "Clear the screen")

        #buttonAdvs = tk.Button(self.menuLabFrame, text='Advanced',
        #                         command=lambda : controller.show_frame(AdvSelPage), bg='grey')
        #buttonAdvs.pack(side='top', fill='both', padx=10)
        #create_tooltip(buttonAdvs, "Advanced settings")

        #buttonExit = tk.Button(self.menuLabFrame, text='Exit',
        #                         command=lambda : controller.exit_window(), bg='grey')
        #buttonExit.pack(side='top', fill='both', padx=10)
        #create_tooltip(buttonExit, "Exit the program")

        
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

    def change_style(self, style):
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
        self.dc.set_draw_style(style)
        for button in self.style_buttons:
            button['state'] = tk.NORMAL

        for s in self.style_options.items():
            if s[1] == style:
                buttonLabel = s[0]

        for button in self.style_buttons:
            if button['text'] == buttonLabel:
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
        
    def save_figure(self, invert_clrs=False):
        """
        Saves the figure currently visible on the DrawCanvas

        Saves the drawings as a postscript and pops up a filedialog, after which it converts 
        the file into the user defined file and removes the postscript file.

        Parameters
        ----------
        None
        """
        self.dc.save()


    def toggle_shape_correction(self, set_=None):
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
        if not(set_ == None):
            self.dc.correct = set_
            self.shape_correction.set(set_)
        elif self.shape_correction.get() == 1:
            self.dc.correct = True
        else:
            self.dc.correct = False

    def toggle_scaling(self, set_=None):
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
        if not(set_ == None):
            self.dc.scale_widg = bool(set_)
            self.scale_drawing.set(set_)
        elif self.scale_drawing.get() == 1:
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
        f_handler = File_handler(logfile)
        f_handler.clear_file()

        data = 'line_colour:'+str(self.dc.line_clr)
        data += '\n'
        data += 'draw_style:'+str(self.dc.draw_style)
        data += '\n'
        data += 'line_width:'+str(self.dc.line_width)
        data += '\n'
        data += 'scaling:'+str(int(self.dc.scale_widg))
        data += '\n'
        data += 'shape_correction:'+str(int(self.dc.correct))
        data += '\n'
        data += 'margin_line:'+str(self.dc.margin_line)
        data += '\n'
        data += 'margin_circle:'+str(self.dc.margin_circle)
        data += '\n'

        f_handler.write_data(data)

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
        f_handler = File_handler(logfile)

        data = f_handler.read_data()

        for line in data:
            if 'line_colour' in line:
                clr = line.split(':')[1]
                clr = clr.split('\n')[0]
                for button in self.clr_buttons:
                    if clr.startswith(button['text']):
                        self.change_clr(button, clr)
                        break
            elif 'draw_style' in line:
                style = line.split(':')[1]
                style = style.split('\n')[0]
                self.change_style(style)
                for s in self.style_options.items():
                    if style == s[1]:
                        self.styleComboBox.set(s[0])
                        break
            elif 'line_width' in line:
                width = line.split(':')[1]
                width = int(width.split('\n')[0])
                self.__change_size(size=width)
            elif 'scaling' in line:
                scale = line.split(':')[1]
                scale = int(scale.split('\n')[0])
                self.toggle_scaling(set_=scale)
            elif 'shape_correction' in line:
                corr = line.split(':')[1]
                corr = int(corr.split('\n')[0])
                self.toggle_shape_correction(set_=corr)
            elif 'margin_line' in line:
                pass
            elif 'margin_circle' in line:
                pass

    def callback_draw_graph(self, x, y, clr='', width=None):
        """
        """
        if not(type(x) == list) or len(x) <= 1:
            raise ValueError('x should contain at least two sets of coordinates')
        if not(type(y) == list) or len(y) <= 1:
            raise ValueError('y should contain at least two sets of coordinates')
        self.dc.draw_graph_coords(x=x, y=y, clr=clr, width=width)

    def callback_draw_sine(self, x, y, periods=1, freq=1):
        """
        """
        x_step = 2*math.pi*freq/(max(x)-min(x))
        y_amp = max(y)-min(y)

        sine = []

        for i in range(0, (max(x)-min(x))*periods):
            sine.append(min(x)+i)
            sine.append(max(y)-y_amp*math.sin(i*x_step))

        self.dc.draw_line_coords(coords=sine)#, style='dash')
        self.dc.draw_graph_coords(x=x, y=y, clr='#BBBBBB')

    def callback_draw_cosine(self, x, y, periods=1, freq=1):
        """
        """
        x_step = 2*math.pi*freq/(max(x)-min(x))
        y_amp = max(y)-min(y)

        cosine = []

        for i in range(0, (max(x)-min(x))*periods):
            cosine.append(min(x)+i)
            cosine.append(max(y)-y_amp*math.cos(i*x_step))

        self.dc.draw_line_coords(coords=cosine)#, style='dot')
        self.dc.draw_graph_coords(x=x, y=y, clr='#BBBBBB')

    
class AdvSelPage(ttk.Frame):
    """
    Advanced selection page to insert graph templates and such
    """

    def __init__(self, parent, controller):
        """
        Class constructor
        """
        super().__init__(parent)
        self.__init_frames()
        self.__init_buttons(controller=controller)
        self.__init_graph_widgets(controller=controller)

    def __init_frames(self):
        """
        Initialises the frames
        """
        self.config(cursor='hand1')
        
        self.menuFrameLab = tk.LabelFrame(self, text='Menu', bg='grey')
        #self.menuFrameLab.config(cursor='hand1')
        self.menuFrameLab.pack(side='left', fill='both')

        self.shapeFrameLab = tk.LabelFrame(self, text='Shapes', bg='grey')
        self.shapeFrameLab.pack(side='left', fill='both')

        self.graphFrameLab = tk.LabelFrame(self, text='Graph', bg='grey')
        self.graphFrameLab.pack(side='left', fill='both')

    def __init_buttons(self, controller):
        """
        Initialises the buttons
        """
        pass

    def __init_graph_widgets(self, controller):
        """
        Initialises the graph related widgets
        
        Parameters
        ----------
        controller:
            The controlling widget
        """
        fLeft = tk.Frame(self.graphFrameLab, bg='grey')
        fLeft.pack(side='left')
        fRight = tk.Frame(self.graphFrameLab, bg='grey')
        fRight.pack(side='left')
        xlabel = tk.Label(fLeft, text='x:', bg='grey')
        xlabel.pack(side='top', padx=10)

        xentry = Entry_w_Placeholder(fRight, placeholder='100, 300')
        xentry.pack(side='top', padx=10)

        ylabel = tk.Label(fLeft, text='y:', bg='grey')
        ylabel.pack(side='top', padx=10)

        yentry = Entry_w_Placeholder(fRight, placeholder='100, 200')
        yentry.pack(side='top', padx=10)

        periodScale = tk.Scale(fLeft,
                               command=lambda e:(),
                               bg='grey', troughcolor='grey',
                               orient=tk.HORIZONTAL,
                               label='Periods',
                               from_=10,
                               to=1)
        periodScale.pack(side='top', fill='both', padx=5)
        periodScale.set(1)
        create_tooltip(periodScale, "Set number of periods")

        freqLabel = tk.Label(fLeft, text='Frequency:', bg='grey')
        freqLabel.pack(side='top', fill='both', padx=5)
        freqEntry = Entry_w_Placeholder(fRight, placeholder='1')
        freqEntry.pack(side='top', fill='both', padx=5)
        create_tooltip(freqEntry, "Set frequency in Hz")

        sinFunc = lambda:(controller.call_function(member=DrawPage,
                                                   function=DrawPage.callback_draw_sine,
                                                   p1=self.convert_t_list(xentry.get().split(','), int),
                                                   p2=self.convert_t_list(yentry.get().split(','), int),
                                                   p3=periodScale.get(),
                                                   p4=float(freqEntry.get())))

        buttonSine = tk.Button(self.graphFrameLab, text='Sine wave',
                               command= sinFunc,
                               bg='grey')
        buttonSine.pack(side='top', fill='both', padx=10)
        create_tooltip(buttonSine, 'Creates a sine wave')

        cosFunc = lambda:(controller.call_function(member=DrawPage,
                                                   function=DrawPage.callback_draw_cosine,
                                                   p1=self.convert_t_list(xentry.get().split(','), int),
                                                   p2=self.convert_t_list(yentry.get().split(','), int),
                                                   p3=periodScale.get(),
                                                   p4=float(freqEntry.get())))
        
        buttonCos = tk.Button(self.graphFrameLab, text='Cosine wave',
                               command= cosFunc,
                               bg='grey')
        buttonCos.pack(side='top', fill='both', padx=10)
        create_tooltip(buttonCos, 'Creates a cosine wave')

    def convert_t_list(self, old, type_):
        """
        Converts a item(s) to a list of specified type

        Parameters
        ----------
        old:
            The old item(s) to convert to a list
        type_:
            The type to convert to

        Returns
        -------
        new:
            The list of items converted to a specified type
        
        """
        new = []
        for item in old:
            new.append(type_(item))

        if len(new) == 1:
            new = new[0]
        return new

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
