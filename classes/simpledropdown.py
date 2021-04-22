from tkinter import ttk, Toplevel

class SimpleDropDown:
    def __init__(self, parent, title, text, choices):
        self.top = Toplevel(parent)
        self.top.resizable(False, False)
        self.top.tkraise(parent)
        self.top.title(title if title else '')
        self.selection = None
        ttk.Label(self.top, text=text if text else '').grid(row=0, column=0, padx=5, pady=10)
        self.combobox = ttk.Combobox(self.top, value=choices if choices else [], state='readonly')
        self.combobox.current(0)
        self.combobox.grid(row=1, column=0, padx=5, pady=10)
        self.combobox.bind('<<ComboboxSelected>>', self.comboboxSelect)

    def comboboxSelect(self, event):
        self.selection = self.combobox.get()
        self.top.destroy()