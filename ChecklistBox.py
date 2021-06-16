import tkinter as tk
import tkinter.font as font

class ChecklistBox(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

    def setItems(self, choices, callback):
        for child in self.winfo_children():
            child.destroy()
        
        self.vars = []
        bg = self.cget('background')

        for choice in choices:
            var = tk.StringVar(value=choices[choice]['description'])
            self.vars.append(var)
            cb = tk.Checkbutton(self,
                var=var,
                text=choices[choice]['description'],
                fg='black',
                onvalue=1,
                offvalue=0,
                font=font.Font(family="TkDefaultFont", size=8),
                cursor='hand2',
                anchor='w',
                width=20,
                background=bg,
                relief='flat',
                highlightthickness=0,
                command=callback)
            cb.pack(side='top', fill='x', anchor='w')

    def getItemCheckStates(self):
        values = []
        for var in self.vars:
            value = var.get()
            values.append(value)
        return values

class ScrollableChecklist(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(side='right', fill='y', expand='false')
        self.canvas = tk.Canvas(self,
            highlightthickness=0,
            yscrollcommand=self.vscrollbar.set,
            **kwargs)
        self.canvas.configure(bd=0)
        self.canvas.pack(side='left', fill='both', expand='true')
        self.vscrollbar.config(command=self.canvas.yview)
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.interior = tk.Frame(self.canvas, **kwargs)
        self.interior.configure(height=2400)
        self.canvas.create_window((0, 0), window=self.interior, anchor='nw')
        self.canvas.bind('<Configure>', self.set_scrollregion)

    def set_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def setItems(self, choices, callback):
        for child in self.interior.winfo_children():
            child.destroy()
        
        self.vars = []
        bg = self.cget('background')

        for choice in choices:
            var = tk.StringVar(value=choices[choice]['description'])
            var.set(choices[choice]['hidden'])
            self.vars.append(var)
            cb = tk.Checkbutton(self.interior,
                var=var,
                text=choices[choice]['description'],
                foreground='#000000',
                onvalue=1,
                offvalue=0,
                font=font.Font(family="TkDefaultFont", size=8),
                cursor='hand2',
                anchor='w',
                width=20,
                background=bg,
                relief='flat',
                highlightthickness=0,
                command=callback)
            cb.pack(side='top', fill='x', anchor='w')

    def getItemCheckStates(self):
        values = []
        for var in self.vars:
            value = var.get()
            values.append(value)
        return values