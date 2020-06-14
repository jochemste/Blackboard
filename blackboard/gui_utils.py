import tkinter as tk

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
