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

        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMMS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.config(text=btn.number)
                btn.grid(row=i, column=j, stick="NWES")
                count += 1

    def create_stat_win():
        pass

    def create_setting_win(self):
        def change_lvl(mines, row, col):
            row_entry.delete(0, END)
            row_entry.insert(0, row)
            column_entry.delete(0, END)
            column_entry.insert(0, col)
            mines_entry.delete(0, END)
            mines_entry.insert(0, mines)

        win_settings = Toplevel(self.window)
        win_settings.title("Settings")
        Label(win_settings, text="Count row").grid(row=0, column=0)
        Label(win_settings, text="Count column").grid(row=1, column=0)
        Label(win_settings, text="Count mines").grid(row=2, column=0)

        row_entry = Entry(win_settings)
        row_entry.insert(0, self.ROW)
        row_entry.grid(row=0, columnspan=3, column=1, padx=20, pady=20)
        column_entry = Entry(win_settings)
        column_entry.insert(0, self.COLUMMS)
        column_entry.grid(row=1, columnspan=3, column=1, padx=20, pady=20)
        mines_entry = Entry(win_settings)
        mines_entry.insert(0, self.COLUMMS)
        mines_entry.grid(row=2, columnspan=3, column=1, padx=20, pady=20)

        save_btn = Button(
            win_settings,
            text="Apply",
            command=lambda: self.change_settings(row_entry, column_entry, mines_entry),
        )
        save_btn.grid(row=4, column=1, padx=20, pady=20)

        easy_btn = Button(
            win_settings, text="Easy", command=lambda: change_lvl(5, 6, 6)
        )
        easy_btn.grid(row=3, column=0)

        normal_btn = Button(
            win_settings, text="Normal", command=lambda: change_lvl(10, 10, 10)
        )
        normal_btn.grid(row=3, column=1)

        hard_btn = Button(
            win_settings, text="Hard", command=lambda: change_lvl(35, 10, 25)
        )
        hard_btn.grid(row=3, column=2)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        self.IS_GAMEROVER = False

    def change_settings(self, row: Entry, column: Entry, mines: Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror("Error", "Incorret values")
            return
        self.ROW = int(row.get())
        self.COLUMMS = int(column.get())
        self.MINES = int(mines.get())
        self.reload()

    def right_click(self):
        pass

    def click(self, clicked_button: Mybutton):
        pass

    def start(self):
        self.create_widgets()
        self.window.mainloop()


game = Saper()
game.start()
