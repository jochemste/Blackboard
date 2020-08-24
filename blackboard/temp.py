import tkinter as tk
from tkinter import ttk

class Entry_w_Placeholder(tk.Entry):
    """
    Tkinter Entry based widget with a placeholder

    A widget to allow placeholders, based on the tkinter Entry widget.
    Allows a custom text to be displayed in the Entry, that disappears
    when the widget is in focus/clicked on.

    Attributes
    ----------
    None

    Methods
    -------
    __init__(self, master)
        Constructor
    insert_placeholder(self, text)
        Inserts place holder into the Entry
    """
        
    def __init__(self, master):
        """
        Constructor
        
        Sets the master of the Entry widget
        
        Parameters
        ----------
        master
            The root/master of the widget
        """
        super().__init__(master)

    def insert_placeholder(self, text):
        """
        Inserts place holder into the Entry
        
        Inserts text into the Entry that disappears once clicked on and appears again 
        once out of focus.
        
        Parameters
        ----------
        text: str
            The text to use as placeholder
        """
        self.insert(0, text)
        self.bind('<FocusIn>',
                  lambda args: self.delete(0, 'end'))
        self.bind('<FocusOut>',
                  lambda args: self.insert(0, text))

