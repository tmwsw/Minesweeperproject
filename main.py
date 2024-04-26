from tkinter import *
import random
from tkinter.messagebox import showinfo, showerror
import time
import re
from PIL import ImageTk, Image

colors = {
    0: "white",  # белый
    1: "#331fcf",  # синий
    2: "#5acf1f",  # зеленый
    3: "#c0cf1f",  # чуть желтый
    4: "#cfa61f",  # чуть оранжевый
    5: "#cf1f91",  # розовый
    6: "#8f1171",  # чуть фиолетовый
    7: "#b01c0e",  # красный
    8: "#aba130",  # черный
}


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


class Minesweepper:
    window = Tk()
    window.title("Сапер")
    ROW = 5
    COLUMMS = 5
    MINES = 5
    IS_GAMEROVER = False
    IS_FIRST_CLICK = True
    bomb_color = ImageTk.PhotoImage(Image.open("image\\bomb-color.png"))
    bomb_defused = ImageTk.PhotoImage(Image.open("image\\bomb-defused.png"))

    def __init__(self):
        self.buttons = []
        for i in range(self.ROW + 2):
            temp = []
            for j in range(self.COLUMMS + 2):
                btn = Mybutton(self.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button - 3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(
        self,
    ):  # Создает элементы интерфейса, такие как кнопки, метки и меню.
        count = 1
        self.flag_position = []
        self.count_flag = self.MINES
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Начать", command=self.reload)
        settings_menu.add_command(label="Настройки", command=self.create_setting_win)
        settings_menu.add_command(label="Статистика", command=self.create_stat_win)
        settings_menu.add_command(label="Выйти из игры", command=self.window.destroy)
        menubar.add_cascade(label="Меню", menu=settings_menu)

        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMMS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick="NWES")
                count += 1
        for i in range(1, self.ROW + 1):
            Grid.rowconfigure(self.window, i, weight=1)
        for i in range(1, self.COLUMMS + 1):
            Grid.rowconfigure(self.window, i, weight=1)

        self.lbl_time = Label(text="Жми")
        self.lbl_time.grid(row=0, column=1, columnspan=(self.COLUMMS // 2))
        self.lbl_mine = Label(text=f"Флажки: {self.count_flag}")
        self.lbl_mine.grid(
            row=0, column=(self.COLUMMS // 2) + 1, columnspan=(self.COLUMMS // 2)
        )

    def create_setting_win(
        self,
    ):  # Создает окно настроек для изменения параметров игры.
        def change_lvl(mines, row, col):
            row_entry.delete(0, END)
            row_entry.insert(0, row)
            column_entry.delete(0, END)
            column_entry.insert(0, col)
            mines_entry.delete(0, END)
            mines_entry.insert(0, mines)

        win_settings = Toplevel(self.window)
        win_settings.title("Настройки")
        Label(win_settings, text="Ряды").grid(row=0, column=0)
        Label(win_settings, text="Столбцы").grid(row=1, column=0)
        Label(win_settings, text="Мины").grid(row=2, column=0)

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
            text="Применить",
            command=lambda: self.change_settings(row_entry, column_entry, mines_entry),
        )
        save_btn.grid(row=4, column=1, padx=20, pady=20)

        easy_btn = Button(
            win_settings, text="Легко", command=lambda: change_lvl(5, 6, 6)
        )
        easy_btn.grid(row=3, column=0)

        normal_btn = Button(
            win_settings, text="Нормально", command=lambda: change_lvl(10, 10, 10)
        )
        normal_btn.grid(row=3, column=1)

        hard_btn = Button(
            win_settings, text="Тяжело", command=lambda: change_lvl(35, 10, 25)
        )
        hard_btn.grid(row=3, column=2)

    def reload(
        self,
    ):  # Сбрасывает игру, уничтожая текущее окно и инициализируя новую игру.
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        self.IS_GAMEROVER = False
        self.IS_FIRST_CLICK = True

    def change_settings(
        self, row: Entry, column: Entry, mines: Entry
    ):  # Изменяет настройки игры на основе ввода пользователя.
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror("Error", "Incorret values")
            return
        self.ROW = int(row.get())
        self.COLUMMS = int(column.get())
        self.MINES = int(mines.get())
        self.reload()

    def create_stat_win(self):  # Создает окно статистики, отображающее статистику игры.
        with open("logs.txt", "r") as logs:
            text = logs.read()
            list_game_time = re.findall(r":(\w+)", text)
            list_game_result = re.findall(r"-(\w+)", text)
        time = 0
        for i in list_game_time:
            time += int(i)
        time_avg = time / len(list_game_time)
        win_avg = list_game_result.count("win") / len(list_game_result)
        showinfo(
            "Статистика",
            f"Сыграно {len(list_game_result)} игр\n"
            f"Твой рейтинг {win_avg * 100}%\n"
            f"Средняя время игры {time_avg:.2f} сек",
        )

    def right_click(
        self, event
    ):  # Обрабатывает события правого клика для установки флагов на клетки.
        cur_btn = event.widget
        if self.IS_GAMEROVER:
            return
        if self.IS_FIRST_CLICK:
            return
        list_mines_pos = sorted(self.index_mines)
        if not cur_btn.is_flag and not cur_btn.is_open:
            if self.count_flag == 0:
                return
            cur_btn["command"] = 0
            cur_btn.is_flag = True
            cur_btn["text"] = "F"
            cur_btn["image"] = self.bomb_defused
            self.count_flag -= 1
            self.flag_position.append(cur_btn.number)
        elif cur_btn.is_flag and not cur_btn.is_open:
            cur_btn.is_flag = False
            cur_btn["text"] = ""
            cur_btn["image"] = ""
            cur_btn["command"] = lambda button=cur_btn: self.click(button)
            self.count_flag += 1
            self.flag_position.remove(cur_btn.number)

        if list_mines_pos == sorted(self.flag_position):
            showinfo("Победа", f"Ты выиграл\n" f"Ты потратил {self.timer:.0f} сек")
            with open("logs.txt", "a") as logs:
                logs.write(f"result-win time:{self.timer:.0f} sec\n")
            self.reload()
        self.lbl_mine.config(text=f"Flags {self.count_flag}")

    def count_mines_buttons(self):  # Подсчитывает количество мин вокруг каждой кнопки.
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMMS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    def click(
        self, clicked_button: Mybutton
    ):  # Обрабатывает события левого клика на кнопках.
        if self.IS_GAMEROVER:
            return
        if self.IS_FIRST_CLICK:
            self.time_start = time.time()
            self.insert_mines(clicked_button.number)
            self.count_mines_buttons()
            self.tick()
            self.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", bg="red", disabledforeground="black")
            clicked_button.is_open = True
            self.IS_GAMEROVER = True
            for i in range(1, self.ROW + 1):
                for j in range(1, self.COLUMMS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        if btn.is_flag:
                            btn["image"] = self.bomb_defused
                            btn["bg"] = "lightgreen"
                        else:
                            btn["image"] = self.bomb_color
            showinfo(
                "Игра окончена",
                f"Ты проиграл \n"
                f"Ты потратил {self.timer:.0f} сек \n"
                f"и нашёл {self.MINES - self.count_flag} мин",
            )
            with open("logs.txt", "a") as logs:
                logs.write(f"result-loss time:{self.timer:.0f} sec\n")
            # self.open_all_buttons()
        else:
            color = colors.get(clicked_button.count_bomb, "black")
            if clicked_button.count_bomb:
                clicked_button.config(
                    text=clicked_button.count_bomb, disabledforeground=color
                )
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        color = colors.get(clicked_button.count_bomb, "black")
        clicked_button.config(foreground="black", relief=SUNKEN)

    def get_mine_places(
        self, exlude_number: int
    ):  # Генерирует случайные позиции для размещения мин.
        indexes = list(range(1, self.COLUMMS * self.ROW + 1))
        indexes.remove(exlude_number)
        random.shuffle(indexes)
        return indexes[: self.MINES]

    def breadth_first_search(
        self, btn: Mybutton
    ):  # Реализует алгоритм обхода в ширину для открытия смежных клеток.
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, "black")
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text="", disabledforeground=color)
            cur_btn.config(state="disabled", relief=SUNKEN)
            cur_btn.is_open = True
            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x + dx][y + dy]
                        if (
                            not next_btn.is_open
                            and not next_btn.is_flag
                            and 1 <= next_btn.x <= self.ROW
                            and 1 <= next_btn.y <= self.COLUMMS
                            and next_btn not in queue
                        ):
                            queue.append(next_btn)

    def insert_mines(self, number: int):  # Вставляет мины в игровое поле.
        self.index_mines = self.get_mine_places(number)
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMMS + 1):
                btn = self.buttons[i][j]
                if btn.number in self.index_mines:
                    btn.is_mine = True

    def open_all_buttons(self):  # Раскрывает все кнопки в конце игры.
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMMS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", bg="red", disabledforeground="black")
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, "black")
                    btn.config(text=btn.count_bomb, foreground="black")

    def print_mines(self):  # Выводит размещение мин для отладки.
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMMS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("b", end="")
                else:
                    print(btn.count_bomb, end="")
            print()

    def tick(self):  # Обновляет таймер игры
        if self.IS_GAMEROVER:
            return
        self.timer = time.time() - self.time_start
        self.lbl_time.config(text=f"Время: {self.timer:.0f}")
        self.lbl_time.after(500, self.tick)

    def start(
        self,
    ):  # Запускает игру, создавая интерфейс и запуская главный цикл Tkinter.
        self.create_widgets()
        self.window.mainloop()


game = Minesweepper()
game.start()
