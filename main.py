from tkinter import *
import random
from tkinter.messagebox import showinfo, showerror
import time
import re


class Mybutton(Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(Mybutton, self).__init__(
            master, width=3, font="Dimkin 15 bold", *args, **kwargs
        )
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False
        self.count_flag = 0
        self.time_start = 0
        self.is_flag = False


class Saper:
    window = Tk()
    window.title("Saper")
    ROW = 5
    COLUMMS = 5
    MINES = 5
    IS_GAMEROVER = False

    def __init__(self):
        self.buttons = []
        for i in range(self.ROW + 2):
            temp = []
            for j in range(self.COLUMMS + 2):
                btn = Mybutton(self.window, x=i, y=j)
                btn.config(text="b", command=lambda button=btn: self.click(button))
                btn.bind("<Button - 3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(self):
        count = 1
        self.flag_position = []
        self.count_flag = self.MINES
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Start", command=self.reload)
        settings_menu.add_command(label="Settings", command=self.create_setting_win)
        settings_menu.add_command(label="Statistics", command=self.create_stat_win)
        settings_menu.add_command(label="Exit", command=self.window.destroy)
        menubar.add_cascade(label="Menu", menu=settings_menu)

    def create_stat_win():
        pass

    def create_setting_win(self):
        pass

    def reload(self):
        pass

    def right_click(self):
        pass

    def click(self, clicked_button: Mybutton):
        pass

    def start(self):
        self.create_widgets()
        self.window.mainloop()


game = Saper()
game.start()
