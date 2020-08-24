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
        
    def __init__(self, master, *args, **kwargs):
        """
        Constructor
        
        Sets the master of the Entry widget
        
        Parameters
        ----------
        master
            The root/master of the widget
        """
        super().__init__(master)

        if 'placeholder' in kwargs:
            self.insert_placeholder(kwargs['placeholder'])

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
        focusout = lambda args: self.insert(0, text)
        self.insert(0, text)
        self.bind('<FocusIn>',
                  lambda args: self.delete_if_empty(first=0, last='end',
                                                    text=text))
        self.bind('<FocusOut>', lambda args: self.insert_if_empty(0, text))

    def delete_if_empty(self, first, last, text):
        """
        Deletes the contents of the entry if no edited
        
        Deletes the contents of the entry if the user did not change 
        the placeholder.
        
        Parameters
        ----------
        first:
            The index of the first to delete
        last:
            The index (or string) of the last to delete
        text: str
            The text used as placeholder
        """
        if self.get() == text:
            self.delete(first, last)
        
    def insert_if_empty(self, index, text):
        """
        Inserts the placeholder if the entry is         
        
        Parameters
        ----------
        index:
            The index where the place holder should start
        text: str
            The text used as placeholder
        """
        if not(self.get()):
            self.insert(index, text)
        

class ToolTip(object):

    def __init__(self, widget, waittime=400):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.waittime = waittime

    def schedule(self, text):
        self.unschedule()
        self.id = self.widget.after(self.waittime,
                                    lambda : self.showtip(text=text))

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, text, event=None):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
        #if event == None:
        #    label.pack(ipadx=1)
        #else:
        #    label.place(x=event.x, y=event.y)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.schedule(text)
    def leave(event):
        toolTip.unschedule()
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
