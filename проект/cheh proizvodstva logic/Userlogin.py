import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


# КЛАСС ВХОДА
class Login:

    def __init__(self):
        self.loginw = Tk()
        self.loginw.title("Вход")
        width = 500
        height = 600
        screen_width = self.loginw.winfo_screenwidth()
        screen_height = self.loginw.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.loginw.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.loginw.resizable(0, 0)
        self.loginw.protocol('WM_DELETE_WINDOW', self.__login_del__)
        self.loginw.config(bg="#4267b2")
        self.logintable()
        self.username = StringVar(value="Имя пользователя")
        self.password = StringVar(value="Пароль")
        self.obj()

    def __login_del__(self):
        if messagebox.askyesno("Выход", "Покинуть инвентаризацию?") == True:
            self.loginw.destroy()
            exit(0)  # ПРИНУДИТЕЛЬНОЕ ЗАВЕРШЕНИЕ СИСТЕМЫ

    # ТАБЛИЦА ВХОДА
    def logintable(self):
        self.base = sqlite3.connect("login.db")
        self.cur = self.base.cursor()
        self.cur.execute("CREATE TABLE if not exists users ( username varchar (20),password	 varchar (20) NOT NULL,account_type varchar ( 10 ) NOT NULL,PRIMARY KEY(username));")

    # ФУНКЦИЯ ВИДЖЕТОВ
    def obj(self):
        self.loginframe = LabelFrame(self.loginw, bg="#4267b2", height=400, width=300)
        self.loginw.bind('<Return>', self.checkuser)
        self.loginframe.place(x=103, y=95)
        self.toplabel = Label(self.loginframe, fg="white", bg="#4267b2", anchor="center", text="Вход", font="Roboto 40 bold")
        self.toplabel.place(x=75, y=25)
        self.us = ttk.Entry(self.loginframe, width=20, textvariable=self.username, font="Roboto 14 ")
        self.us.place(x=35, y=145, height=40)
        self.pa = ttk.Entry(self.loginframe, width=20, textvariable=self.password, font="Roboto 14 ")
        self.pa.place(x=35, y=185, height=40)
        self.us.bind('<Button-1>', self.onclick)
        self.pa.bind('<Button-1>', self.onclick1)
        self.signin = Button(self.loginframe, width=20, text="Войти", bg="lightblue2", fg="dimgray", command=self.checkuser, font="Roboto 14")
        self.signin.place(x=35, y=290)
        # self.register = Button(self.loginframe, width=20, text="Регистрация", bg="lightblue2", fg="dimgray", command=self.reguser, font="Roboto")
        # self.register.place(x=35, y=320)

    # ПРОВЕРКА ПОЛЬЗОВАТЕЛЯ В БАЗЕ ДАННЫХ
    def checkuser(self, event=0):
        s = self.username.get()
        s1 = self.password.get()
        s = s.upper()
        s1 = s1.upper()
        self.cur.execute("select * from users where username=? and password=? ", (s, s1))
        l = self.cur.fetchall()
        if (len(l) > 0):
            self.success()
        else:
            self.fail()

    # УСПЕШНЫЙ ВХОД
    def success(self):
        # messagebox.showinfo("Успешно", "Вход выполнен успешно")
        self.loginw.quit()

    # НЕУДАЧНЫЙ ВХОД
    def fail(self):
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    # РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ && ВХОД -> РЕГИСТРАЦИЯ
    def reguser(self):
        self.toplabel.config(text="Регистрация")
        self.toplabel.place(x=40, y=25)
        self.username.set("Выберите имя пользователя")
        self.password.set("Создайте пароль")
        self.signin.config(text="ОК", command=self.insert)
        # ДОБАВИТЬ
        self.register = Button(self.loginframe, width=20, text="Назад", bg="lightblue2", fg="dimgray", command=self.revert, font="Roboto 14")
        self.register.place(x=35, y=320)
        # self.register.config(text="Назад", command=self.revert)
        self.signin.config()
        self.signin.place(x=35, y=260)
        self.pa.config(show='')
        self.loginw.focus()
        self.loginw.bind('<Return>', self.insert)
        self.loginw.title('Регистрация')

    # ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ В БАЗУ ДАННЫХ
    def insert(self, event=0):
        s = self.username.get()
        s1 = self.password.get()
        s = s.upper()
        s1 = s1.upper()
        self.cur.execute("select username from users where username = ?", (s,))
        l = self.cur.fetchall()
        if (len(l) > 0):
            messagebox.showerror("Ошибка", "Имя пользователя уже существует")
            self.username.set('Выберите имя пользователя')
            self.loginw.focus()
            return
        if (len(s) == 0 or len(s1) == 0 or len(s) > 20 or len(s1) > 20 or s1 == "СОЗДАЙТЕ ПАРОЛЬ" or s == 'ВЫБЕРИТЕ ИМЯ ПОЛЬЗОВАТЕЛЯ'):
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")
            self.username.set('Выберите имя пользователя')
            self.password.set('Создайте пароль')
            self.pa.config(show='')
            self.loginw.focus()
            return
        else:
            self.cur.execute("insert into users values(?,?,?)", (s, s1, 'USER'))
            messagebox.showinfo("Успешно", "Пользователь зарегистрирован")
            self.base.commit()
            self.revert()
            # ДОБАВИТЬ
            self.loginw.state('withdraw')
            self.tree.delete(*self.tree.get_children())
            self.getusers()

    # РЕГИСТРАЦИЯ -> ВХОД
    def revert(self):
        self.toplabel.config(text="Вход")
        self.toplabel.place(x=75, y=25)
        self.signin.config(text="Войти", command=self.checkuser)
        self.register.config(text="Регистрация", command=self.reguser)
        self.username.set('Имя пользователя')
        self.password.set('Пароль')
        self.pa.config(show='')
        self.signin.config(state=NORMAL)
        self.loginw.focus()
        self.loginw.bind('<Return>', self.checkuser)
        # ДОБАВИТЬ
        self.signin.place(x=35, y=290)
        self.loginw.title('Вход')
        self.loginw.state('withdraw')

    # СОБЫТИЯ ПРИ КЛИКЕ
    def onclick(self, event):
        if (self.username.get() == "Имя пользователя" or self.username.get() == "Выберите имя пользователя"):
            self.us.delete(0, "end")

    def onclick1(self, event):
        if (self.password.get() == "Пароль" or self.password.get() == "Создайте пароль"):
            self.pa.delete(0, "end")
            self.pa.config(show="*")