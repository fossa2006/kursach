import sqlite3
import random
import matplotlib.colors as mcolors
import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox, simpledialog
from Addtional_features import mycombobox, myentry
import matplotlib
import pandas as pd
from tkcalendar import DateEntry

matplotlib.use('TkAgg')  # Устанавливаем бэкенд TkAgg для интеграции с Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# МЕНЮ АДМИНИСТРАТОРА
class Admin:

    def __init__(self, mainw):
        self.mainw = mainw
        self.cur.execute("ALTER TABLE sales ADD COLUMN username VARCHAR(20)")  # Добавляем поле username в таблицу sales
        self.base.commit()

    def export_to_excel(self):
        """
        Экспорт данных из таблицы products в Excel.
        """
        try:
            # Получаем данные из таблицы products
            self.cur.execute("SELECT * FROM products")
            products = self.cur.fetchall()

            # Если данных нет, выводим сообщение
            if not products:
                messagebox.showinfo("Информация", "Нет данных для экспорта")
                return

            # Создаем DataFrame из данных
            columns = ["Product ID", "Product Name", "Description", "Category", "Price", "Stocks"]
            df = pd.DataFrame(products, columns=columns)

            # Сохраняем DataFrame в Excel
            file_path = "products_export.xlsx"
            df.to_excel(file_path, index=False)

            messagebox.showinfo("Успешно", f"Данные успешно экспортированы в файл: {file_path}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте данных: {e}")
    # ДОБАВЛЕНИЕ ОСНОВНОГО МЕНЮ АДМИНИСТРАТОРА В ОКНО, ВСЕ ФРЕЙМЫ И КНОПКИ С ИЗОБРАЖЕНИЯМИ
    def admin_mainmenu(self, a, b):
        self.mainframe = LabelFrame(self.mainw, width=1200, height=145, bg="#f7f7f7")
        self.mainframe.place(x=100, y=100)
        mi = PhotoImage(file="images/accounts.png")
        mi = mi.subsample(a, b)
        self.accounts = Button(self.mainframe, text="Профили", font="roboto 11 bold", bd=5, image=mi, compound=TOP,
                               command=self.buildusertable)
        self.accounts.image = mi
        self.accounts.place(x=655, y=27)
        mi = PhotoImage(file="images/Door_Out-512.png")
        mi = mi.subsample(a, b)
        self.logout = Button(self.mainframe, text="Выйти", bd=5, font="roboto 11 bold", image=mi, compound=TOP)
        self.logout.image = mi
        self.logout.place(x=1050, y=27)
        mi = PhotoImage(file="images/change1.png")
        mi = mi.subsample(a, b)
        self.changeuser = Button(self.mainframe, text="Сменить пользователя", bd=5, font="roboto 11 bold", image=mi,
                                 compound=TOP)
        self.changeuser.image = mi
        self.changeuser.place(x=855, y=27)
        mi = PhotoImage(file="images/items.png")
        mi = mi.subsample(a, b)
        self.items = Button(self.mainframe, text="добавить", bd=5, image=mi, font="roboto 11 bold", compound=TOP,
                            command=self.additems)
        self.items.image = mi
        self.items.place(x=47, y=27)
        mi = PhotoImage(file="images/inventory.png")
        mi = mi.subsample(a, b)
        self.stocks = Button(self.mainframe, text="Инвентаризация", bd=5, image=mi, font="roboto 11 bold", compound=TOP,
                             command=self.buildprodtable)
        self.stocks.image = mi
        self.stocks.place(x=255, y=27)
        mi = PhotoImage(file="images/sales.png")
        mi = mi.subsample(a, b)
        self.sales = Button(self.mainframe, text="Траты", bd=5, font="roboto 11 bold", image=mi, compound=TOP,
                            command=self.buildsalestable)
        self.sales.image = mi
        self.sales.place(x=450, y=27)

        # Добавляем кнопку для отображения круговой диаграммы
        mi = PhotoImage(file="images/pie_chart.png")  # Изображение для кнопки (если есть)
        mi = mi.subsample(a, b)
        self.pie_chart_button = Button(self.mainframe, text="Диаграмма", bd=5, font="roboto 11 bold", image=mi,
                                       compound=TOP, command=self.show_pie_chart)
        self.pie_chart_button.image = mi
        self.pie_chart_button.place(x=1050, y=27)

        self.formframe = Frame(self.mainw, width=500, height=550, bg="#FFFFFF")
        self.formframe.place(x=100, y=315)
        self.formframeinfo = self.formframe.place_info()
        self.tableframe1 = LabelFrame(self.mainw, width=350, height=700)
        self.tableframe1.place(x=1200, y=315, anchor=NE)
        self.tableframe1info = self.tableframe1.place_info()
        self.tableframe = LabelFrame(self.mainw, width=350, height=700)
        self.tableframe.place(x=1300, y=315, anchor=NE)
        self.tableframeinfo = self.tableframe.place_info()
        self.itemframe = Frame(self.mainw, bg="#FFFFFF", width=600, height=300)
        self.itemframe.place(x=420, y=280, anchor=NW)
        self.itemframeinfo = self.itemframe.place_info()
        self.formframe1 = Frame(self.mainw, width=500, height=445, bg="#FFFFFF")
        self.formframe1.place(x=100, y=275)
        self.formframe1info = self.formframe1.place_info()
        self.searchframe = Frame(self.mainw, width=720, height=70, bg="#FFFFFF")
        self.searchframe.place(x=575, y=260)
        self.searchframeinfo = self.searchframe.place_info()
        self.searchbut = Button(self.searchframe, text="Поиск", font="roboto 14", bg="#FFFFFF", bd=5,
                                command=self.searchprod)
        self.searchbut.place(x=0, y=20, height=40)
        self.searchvar = StringVar()
        self.searchentry = myentry(self.searchframe, textvariable=self.searchvar, font="roboto 14", width=25,
                                   bg="#FFFFFF")
        self.searchentry.place(x=210, y=20, height=40)
        self.cur.execute("select product_desc from products")
        li = self.cur.fetchall()
        a = []
        for i in range(0, len(li)):
            a.append(li[i][0])
        self.searchentry.set_completion_list(a)
        self.resetbut = Button(self.searchframe, text="Сбросить", font="roboto 14", bd=5, width=8, bg="#FFFFFF",
                               command=self.resetprodtabel)
        self.resetbut.place(x=510, y=18, height=40)
        self.cond = 0
        self.buildprodtable()

    # ОСНОВНОЕ МЕНЮ АДМИНИСТРАТОРА ЗАКАНЧИВАЕТСЯ

    # СОЗДАНИЕ ТАБЛИЦЫ материалов В ИНВЕНТАРИЗАЦИИ
    def buildprodtable(self):
        self.searchframe.place_forget()
        self.tableframe.place(self.tableframeinfo)
        self.formframe.place(self.formframeinfo)
        self.tableframe1.place_forget()
        self.formframe1.place_forget()
        self.itemframe.place_forget()
        if (self.cond == 1):
            self.tree.delete(*self.tree.get_children())
            self.tree.grid_remove()
            self.tree.destroy()
        scrollbarx = Scrollbar(self.tableframe, orient=HORIZONTAL)
        scrollbary = Scrollbar(self.tableframe, orient=VERTICAL)
        self.tree = ttk.Treeview(self.tableframe, columns=("Product ID", "Product Name", "Description", "Category",
                                                           'Price', 'Stocks'), selectmode="browse", height=18,
                                 yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=100)
        self.tree.column('#2', stretch=NO, minwidth=0, width=100)
        self.tree.column('#3', stretch=NO, minwidth=0, width=150)
        self.tree.column('#4', stretch=NO, minwidth=0, width=150)
        self.tree.column('#5', stretch=NO, minwidth=0, width=100)
        self.tree.column('#6', stretch=NO, minwidth=0, width=100)
        self.tree.heading('Product ID', text="id продукта", anchor=W)
        self.tree.heading('Product Name', text="Имя продукта", anchor=W)
        self.tree.heading('Description', text="Описание", anchor=W)
        self.tree.heading('Category', text="Категории", anchor=W)
        self.tree.heading('Price', text="Цена", anchor=W)
        self.tree.heading('Stocks', text="Остаток", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        self.getproducts()
        self.tree.bind("<<TreeviewSelect>>", self.clickprodtable)
        self.formframe.focus_set()
        self.itemeditv = StringVar()
        self.itemeditdescv = StringVar()
        self.itemeditcatv = StringVar()
        self.itemeditpricev = StringVar()
        self.itemeditstockv = StringVar()
        self.addstock = StringVar()
        va = 5
        l1 = ['Имя продукта', 'Описание', 'Категория', 'Цена', 'Остаток', 'Добавить']
        for i in range(0, 6):
            Label(self.formframe, text=l1[i], font="roboto 14 bold", bg="#FFFFFF").place(x=0, y=va)
            va += 60
        Entry(self.formframe, textvariable=self.itemeditv, font="roboto 14", bg="#FFFFFF", width=20).place(x=142, y=0,
                                                                                                           height=40)
        Entry(self.formframe, textvariable=self.itemeditdescv, font="roboto 14", bg="#FFFFFF", width=20).place(x=142,
                                                                                                               y=60,
                                                                                                               height=40)
        x = myentry(self.formframe, textvariable=self.itemeditcatv, font="roboto 14", bg="#FFFFFF", width=20)
        x.place(x=142, y=120, height=40)
        self.cur.execute("select product_cat from products")
        li = self.cur.fetchall()
        a = []
        self.desc_name = []
        for i in range(0, len(li)):
            if (a.count(li[i][0]) == 0):
                a.append(li[i][0])
        x.set_completion_list(a)
        Entry(self.formframe, textvariable=self.itemeditpricev, font="roboto 14", bg="#FFFFFF", width=20).place(x=142,
                                                                                                                y=180,
                                                                                                                height=40)
        Entry(self.formframe, textvariable=self.itemeditstockv, font="roboto 14", bg="#FFFFFF", width=20).place(x=142,
                                                                                                                y=240,
                                                                                                                height=40)
        Entry(self.formframe, textvariable=self.addstock, font="roboto 14", bg="#FFFFFF", width=20).place(x=142, y=300,
                                                                                                          height=40)
        Button(self.formframe, text="Обновить", font="robot 11 bold", bg="#FFFFFF", bd=5, width=10, height=2,
               command=self.changeprodtable).place(x=105, y=361)
        Button(self.formframe, text="Удалить", font="robot 11 bold", bg="#FFFFFF", bd=5, width=10, height=2,
               command=self.delproduct).place(x=305, y=361)
        self.cond = 1
        self.mainsearch(1)

    # Функция для отображения круговой диаграммы
    def show_pie_chart(self):
        try:
            # Получаем данные из таблицы products
            self.cur.execute("SELECT product_name, stocks FROM products")
            products = self.cur.fetchall()

            # Если данных нет, выводим сообщение
            if not products:
                messagebox.showinfo("Информация", "Нет данных для отображения диаграммы")
                return

            # Подготовка данных для диаграммы
            labels = [product[0] for product in products]
            sizes = [product[1] for product in products]

            # Вычисляем общую сумму stocks
            total_stocks = sum(sizes)

            # Вычисляем остаток вычитания из 100000
            remaining_stocks = 100000 - total_stocks

            # Добавляем остаток в данные для диаграммы
            if remaining_stocks > 0:
                labels.append("Остаток")
                sizes.append(remaining_stocks)

            # Создаем фигуру и оси для диаграммы
            fig, ax = plt.subplots(figsize=(5, 6))
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=self.get_colors(sizes))
            ax.set_title("Распределение материалов по количеству")

            # Создаем новое окно для диаграммы
            self.chart_window = Toplevel(self.mainw)
            self.chart_window.title("Круговая диаграмма")
            self.chart_window.geometry("600x800")

            # Интегрируем график в новое окно
            self.canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

            # Добавляем метку для отображения остатка
            self.remaining_label = Label(self.chart_window, text=f"Остаток: {remaining_stocks}", font=("Arial", 12),
                                         fg="black")
            self.remaining_label.pack(side=tkinter.BOTTOM, pady=5)

            # Добавляем кнопку "Обновить диаграмму"
            update_button = Button(self.chart_window, text="Обновить диаграмму", command=self.update_pie_chart)
            update_button.pack(side=tkinter.BOTTOM, pady=5)

            # Добавляем кнопку "Назад"
            back_button = Button(self.chart_window, text="Назад", command=self.close_chart_window)
            back_button.pack(side=tkinter.BOTTOM, pady=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании диаграммы: {e}")

    def update_pie_chart(self):
        try:
            # Получаем обновленные данные из таблицы products
            self.cur.execute("SELECT product_name, stocks FROM products")
            products = self.cur.fetchall()

            # Если данных нет, выводим сообщение
            if not products:
                messagebox.showinfo("Информация", "Нет данных для отображения диаграммы")
                return

            # Подготовка данных для диаграммы
            labels = [product[0] for product in products]
            sizes = [product[1] for product in products]

            # Вычисляем общую сумму stocks
            total_stocks = sum(sizes)

            # Вычисляем остаток вычитания из 100000
            remaining_stocks = 100000 - total_stocks

            # Добавляем остаток в данные для диаграммы
            if remaining_stocks > 0:
                labels.append("Остаток")
                sizes.append(remaining_stocks)

            # Очищаем текущую диаграмму
            self.canvas.get_tk_widget().destroy()

            # Создаем новую фигуру и оси для диаграммы
            fig, ax = plt.subplots(figsize=(5, 6))
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=self.get_colors(sizes))
            ax.set_title("Распределение материалов по количеству")

            # Интегрируем новую диаграмму в окно
            self.canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

            # Обновляем метку с остатком
            self.remaining_label.config(text=f"Остаток: {remaining_stocks}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обновлении диаграммы: {e}")

    def get_colors(self, sizes):
        # Возвращает список случайных цветов для секторов диаграммы
        colors = []
        for size in sizes:
            if size == sizes[-1]:  # Если это остаток, то цвет grey
                colors.append("grey")
            else:
                # Генерируем случайный цвет для каждого товара
                random_color = random.choice(list(mcolors.CSS4_COLORS.values()))
                colors.append(random_color)
        return colors

    def close_chart_window(self):
        # Закрываем окно с диаграммой
        self.chart_window.destroy()

    # ОСНОВНОЕ МЕНЮ АДМИНИСТРАТОРА ЗАКАНЧИВАЕТСЯ

    # СОЗДАНИЕ ТАБЛИЦЫ ТОВАРОВ В ИНВЕНТАРИЗАЦИИ
    def buildprodtable(self):
        self.searchframe.place_forget()
        self.tableframe.place(self.tableframeinfo)
        self.formframe.place(self.formframeinfo)
        self.tableframe1.place_forget()
        self.formframe1.place_forget()
        self.itemframe.place_forget()
        if (self.cond == 1):
            self.tree.delete(*self.tree.get_children())
            self.tree.grid_remove()
            self.tree.destroy()
        scrollbarx = Scrollbar(self.tableframe, orient=HORIZONTAL)
        scrollbary = Scrollbar(self.tableframe, orient=VERTICAL)
        self.tree = ttk.Treeview(self.tableframe, columns=("Product ID", "Product Name", "Description", "Category",
                                                           'Price', 'Stocks'), selectmode="browse", height=18,
                                 yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=100)
        self.tree.column('#2', stretch=NO, minwidth=0, width=100)
        self.tree.column('#3', stretch=NO, minwidth=0, width=150)
        self.tree.column('#4', stretch=NO, minwidth=0, width=150)
        self.tree.column('#5', stretch=NO, minwidth=0, width=100)
        self.tree.column('#6', stretch=NO, minwidth=0, width=100)
        self.tree.heading('Product ID', text="id продукта", anchor=W)
        self.tree.heading('Product Name', text="Имя продукта", anchor=W)
        self.tree.heading('Description', text="Описание", anchor=W)
        self.tree.heading('Category', text="Категории", anchor=W)
        self.tree.heading('Price', text="Цена", anchor=W)
        self.tree.heading('Stocks', text="Остаток", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        self.getproducts()
        self.tree.bind("<<TreeviewSelect>>", self.clickprodtable)
        self.formframe.focus_set()
        self.itemeditv = StringVar()
        self.itemeditdescv = StringVar()
        self.itemeditcatv = StringVar()
        self.itemeditpricev = StringVar()
        self.itemeditstockv = StringVar()
        self.addstock = StringVar()
        va = 5
        l1 = ['Имя продукта', 'Описание', 'Категория', 'Цена', 'Остаток', 'Добавить']
        for i in range(0, 6):
            Label(self.formframe, text=l1[i], font="roboto 14 bold", bg="#FFFFFF").place(x=0, y=va)
            va += 60
        Entry(self.formframe, textvariable=self.itemeditv, font="roboto 14", bg="#FFFFFF", width=20).place(x=142, y=0,
                                                                                                           height=40)
        Entry(self.formframe, textvariable=self.itemeditdescv, font="roboto 14", bg="#FFFFFF", width=20).place(x=142,
                                                                                                               y=60,
                                                                                                               height=40)
        x = myentry(self.formframe, textvariable=self.itemeditcatv, font="roboto 14", bg="#FFFFFF", width=20)
        x.place(x=142, y=120, height=40)
        self.cur.execute("select product_cat from products")
        li = self.cur.fetchall()
        a = []
        self.desc_name = []
        for i in range(0, len(li)):
            if (a.count(li[i][0]) == 0):
                a.append(li[i][0])
        x.set_completion_list(a)
        Entry(self.formframe, textvariable=self.itemeditpricev, font="roboto 14", bg="#FFFFFF", width=20).place(x=142,
                                                                                                                y=180,
                                                                                                                height=40)
        Entry(self.formframe, textvariable=self.itemeditstockv, font="roboto 14", bg="#FFFFFF", width=20).place(x=142,
                                                                                                                y=240,
                                                                                                                height=40)
        Entry(self.formframe, textvariable=self.addstock, font="roboto 14", bg="#FFFFFF", width=20).place(x=142, y=300,
                                                                                                          height=40)
        Button(self.formframe, text="Обновить", font="robot 11 bold", bg="#FFFFFF", bd=5, width=10, height=2,
               command=self.changeprodtable).place(x=105, y=361)
        Button(self.formframe, text="Удалить", font="robot 11 bold", bg="#FFFFFF", bd=5, width=10, height=2,
               command=self.delproduct).place(x=305, y=361)
        self.cond = 1
        self.mainsearch(1)

    # ПОИСКОВЫЙ ФРЕЙМ ДЛЯ ТАБЛИЦ ПОЛЬЗОВАТЕЛЕЙ И ТОВАРОВ
    def mainsearch(self, f):
        self.searchvar.set('')
        if (f == 1):
            self.searchframe.config(width=720)
            self.searchframe.place(x=575, y=245)
            self.searchbut.config(text="Поиск", command=self.searchprod)
            self.searchbut.place(x=0, y=23, height=37)
            self.searchentry.config(textvariable=self.searchvar, width=20)
            self.searchentry.place(x=210, y=25, height=35)
            self.cur.execute("select product_desc from products")
            li = self.cur.fetchall()
            a = []
            for i in range(0, len(li)):
                a.append(li[i][0])
            self.searchentry.set_completion_list(a)
            self.resetbut.config(command=self.resetprodtabel)
            self.resetbut.place(x=460, y=22, height=37)
        elif (f == 0):
            self.searchframe.place(x=661, y=245)
            self.searchframe.config(width=520)
            self.searchbut.config(command=self.searchuser)
            self.searchbut.config(text="Поиск по Имени")
            self.searchbut.place(x=0, y=23)
            self.searchentry.config(width=18, textvariable=self.searchvar)
            self.searchentry.place(x=195, y=25, height=35)
            self.resetbut.config(command=self.resetusertable)
            self.resetbut.place(x=415, y=23)
            self.cur.execute("select username from users")
            li = self.cur.fetchall()
            a = []
            for i in range(0, len(li)):
                a.append(li[i][0])
            self.searchentry.set_completion_list(a)
        else:
            self.searchframe.place(x=138, y=245)
            self.searchframe.config(width=520)
            self.searchbut.config(command=self.searchinvoice)
            self.searchbut.config(text="Поиск")  # Переименование кнопки
            self.searchbut.place(x=100, y=23)
            self.searchentry.config(width=18, textvariable=self.searchvar)
            self.searchentry.place(x=195, y=25, height=35)
            self.resetbut.config(command=self.buildsalestable)
            self.resetbut.place(x=415, y=23)
            self.cur.execute("select invoice from sales")
            li = self.cur.fetchall()
            a = []
            for i in range(0, len(li)):
                if (a.count(str(li[i][0])) == 0):
                    a.append(str(li[i][0]))
            self.searchentry.set_completion_list(a)

    # ИЗВЛЕЧЕНИЕ ТОВАРОВ ИЗ ТАБЛИЦЫ ТОВАРОВ
    def getproducts(self, x=0):
        ans = ''
        self.cur.execute("select * from products")
        productlist = self.cur.fetchall()
        for i in productlist:
            self.tree.insert('', 'end', values=(i))
            if (str(x) == i[0]):
                a = self.tree.get_children()
                ans = a[len(a) - 1]

        return ans

    # МОДИФИКАЦИЯ ЗАПИСИ В ТАБЛИЦЕ ТОВАРОВ
    def changeprodtable(self):
        # Проверяем текущую сумму остатков
        self.cur.execute("SELECT SUM(stocks) FROM products")
        total_stocks = self.cur.fetchone()[0]
        if total_stocks is None:
            total_stocks = 0

        # Проверяем, не превысит ли сумма 100 000 после обновления товара
        new_stock = int(self.itemeditstockv.get())
        add_stock = self.addstock.get()
        if add_stock == '':
            add_stock = 0
        new_stock += int(add_stock)

        if total_stocks + new_stock > 100000:
            messagebox.showerror("Ошибка", "Склад переполнен! Сумма остатков не может превышать 100 000.")
            return

        # Остальной код для обновления товара
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        self.itemeditv.set((self.itemeditv.get()).upper())
        self.itemeditcatv.set((self.itemeditcatv.get()).upper())
        self.itemeditdescv.set((self.itemeditdescv.get()).upper())
        if (len(li) == 6):
            if self.itemeditv.get() == '' or self.itemeditdescv.get() == '':
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
                return
            elif self.itemeditcatv.get() == '' or self.itemeditstockv.get() == '' or self.itemeditpricev.get() == '':
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
                return
            else:
                l = [self.itemeditpricev.get(), self.itemeditstockv.get()]
                for i in range(0, len(l)):
                    if (not l[i].isdigit()):
                        messagebox.showerror("Ошибка", "Неверные данные")
                        return
                    elif (int(l[i]) < 0):
                        messagebox.showerror("Ошибка", "Неверные данные")
                        return
            if (self.addstock.get() == ''):
                self.addstock.set('0')

            self.cur.execute(
                "update products set product_name=?,product_desc=?,product_cat=?,product_price = ?,stocks = ? where product_id = ?;",
                (
                    self.itemeditv.get(), self.itemeditdescv.get(), self.itemeditcatv.get(),
                    int(self.itemeditpricev.get()),
                    (int(self.itemeditstockv.get()) + int(self.addstock.get())), li[0]))
            self.base.commit()
            self.addstock.set('')
            self.tree.delete(*self.tree.get_children())
            cur = self.getproducts(li[0])
            self.tree.selection_set(cur)

    def delproduct(self):
        cur = self.tree.focus()
        cur = self.tree.item(cur)
        li = cur['values']
        if messagebox.askyesno('Внимание!', 'Вы хотите удалить материал из инвентаризации?') == True and len(li) == 6:
            self.cur.execute("delete from products where product_id = ?;", (li[0],))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getproducts()
            self.itemeditv.set('')
            self.itemeditdescv.set('')
            self.itemeditcatv.set('')
            self.itemeditstockv.set('')
            self.itemeditpricev.set('')

    def searchprod(self):
        # Создаем новое окно для поиска
        self.search_window = Toplevel(self.mainw)
        self.search_window.title("Результаты поиска")
        self.search_window.geometry("800x600")

        # Переменные для хранения значений полей ввода
        self.search_product_id = StringVar()
        self.search_description = StringVar()

        # Создаем поля ввода для параметров поиска
        Label(self.search_window, text="ID продукта:").grid(row=0, column=0, padx=10, pady=5)
        Entry(self.search_window, textvariable=self.search_product_id).grid(row=0, column=1, padx=10, pady=5)

        Label(self.search_window, text="Описание:").grid(row=1, column=0, padx=10, pady=5)
        Entry(self.search_window, textvariable=self.search_description).grid(row=1, column=1, padx=10, pady=5)

        # Кнопка для выполнения поиска
        Button(self.search_window, text="Поиск", command=self.perform_search).grid(row=2, column=0, columnspan=2, pady=10)

        # Создаем таблицу для отображения результатов
        self.result_tree = ttk.Treeview(self.search_window, columns=("Product ID", "Product Name", "Description", "Category", 'Price', 'Stocks'),
                                        selectmode="browse", height=18)
        self.result_tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.result_tree.column('#1', stretch=NO, minwidth=0, width=100)
        self.result_tree.column('#2', stretch=NO, minwidth=0, width=150)
        self.result_tree.column('#3', stretch=NO, minwidth=0, width=150)
        self.result_tree.column('#4', stretch=NO, minwidth=0, width=100)
        self.result_tree.column('#5', stretch=NO, minwidth=0, width=100)
        self.result_tree.heading('Product ID', text="id продукта", anchor=W)
        self.result_tree.heading('Product Name', text="Имя продукта", anchor=W)
        self.result_tree.heading('Description', text="Описание", anchor=W)
        self.result_tree.heading('Category', text="Категория", anchor=W)
        self.result_tree.heading('Price', text="Цена", anchor=W)
        self.result_tree.heading('Stocks', text="Остаток", anchor=W)
        self.result_tree.grid(row=3, column=0, columnspan=2, sticky="nsew")

        # Добавляем скроллбары
        scrollbary = Scrollbar(self.search_window, orient=VERTICAL, command=self.result_tree.yview)
        scrollbary.grid(row=3, column=2, sticky="ns")
        self.result_tree.configure(yscrollcommand=scrollbary.set)

    def perform_search(self):
        # Получаем значения из полей ввода
        product_id = self.search_product_id.get()
        description = self.search_description.get()

        # Формируем SQL-запрос с учетом введенных параметров
        query = """
            SELECT product_id, product_name, product_desc, product_cat, product_price, stocks
            FROM products
            WHERE 1=1
        """
        params = []

        if product_id:
            query += " AND product_id = ?"
            params.append(product_id)
        if description:
            query += " AND product_desc LIKE ?"
            params.append('%' + description + '%')

        # Выполняем запрос
        self.cur.execute(query, tuple(params))
        productlist = self.cur.fetchall()

        # Очищаем текущую таблицу результатов
        self.result_tree.delete(*self.result_tree.get_children())

        # Заполняем таблицу результатами поиска
        for product in productlist:
            self.result_tree.insert('', 'end', values=(product))
    def resetprodtabel(self):
        self.searchvar.set('')
        self.tree.delete(*self.tree.get_children())
        self.getproducts()

    # СОБЫТИЕ ПРИ КЛИКЕ НА ТАБЛИЦУ ТОВАРОВ
    def clickprodtable(self, event):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if (len(li) == 6):
            self.itemeditv.set((li[1]))
            self.itemeditdescv.set((li[2]))
            self.itemeditcatv.set((li[3]))
            self.itemeditpricev.set(str(li[4]))
            self.itemeditstockv.set(str(li[5]))
            self.addstock.set('')

    # ФУНКЦИЯ ДЛЯ КНОПКИ ТОВАРОВ
    def additems(self):
        self.formframe1.place_forget()
        self.searchframe.place_forget()
        self.tableframe.place_forget()
        self.tableframe1.place_forget()
        self.formframe.place_forget()
        self.itemframe.place(self.itemframeinfo)
        self.newitem = StringVar()
        self.newitemdesc = StringVar()
        self.newitemcode = StringVar()
        self.newitemcat = StringVar()
        self.newitemprice = StringVar()
        self.newitemstock = StringVar()
        l = ['id продукта', "Имя продукта", "Описание", "Категория", "Цена", "Остаток"]
        for i in range(0, len(l)):
            Label(self.itemframe, text=l[i], font="Roboto 14 bold", bg="#ffffff").grid(row=i, column=0, pady=15,
                                                                                       sticky="w")
        Entry(self.itemframe, width=40, textvariable=self.newitemcode, font="roboto 11", bg="#ffffff").grid(row=0,
                                                                                                            column=1,
                                                                                                            pady=15,
                                                                                                            padx=10,
                                                                                                            ipady=3)
        Entry(self.itemframe, width=40, textvariable=self.newitem, font="roboto 11", bg="#ffffff").grid(row=1, column=1,
                                                                                                        pady=15,
                                                                                                        padx=10,
                                                                                                        ipady=3)
        Entry(self.itemframe, width=40, textvariable=self.newitemdesc, font="roboto 11", bg="#ffffff").grid(row=2,
                                                                                                            column=1,
                                                                                                            pady=15,
                                                                                                            padx=8,
                                                                                                            ipady=3)
        cat = myentry(self.itemframe, width=40, textvariable=self.newitemcat, font="roboto 11", bg="#ffffff")
        cat.grid(row=3, column=1, pady=15, padx=10, ipady=3)
        Entry(self.itemframe, width=40, textvariable=self.newitemprice, font="roboto 11", bg="#ffffff").grid(row=4,
                                                                                                             column=1,
                                                                                                             pady=15,
                                                                                                             padx=10,
                                                                                                             ipady=3)
        Entry(self.itemframe, width=40, textvariable=self.newitemstock, font="roboto 11", bg="#ffffff").grid(row=5,
                                                                                                             column=1,
                                                                                                             pady=15,
                                                                                                             padx=10,
                                                                                                             ipady=3)
        self.cur.execute("select product_cat,product_name,product_desc from products")
        li = self.cur.fetchall()
        a = []
        self.desc_name = []
        for i in range(0, len(li)):
            if (a.count(li[i][0]) == 0):
                a.append(li[i][0])
            self.desc_name.append(li[i][2])
        cat.set_completion_list(a)
        Button(self.itemframe, text="Добавить материал", height=3, bd=6, command=self.insertitem, bg="#FFFFFF").grid(row=6,
                                                                                                                  column=1,
                                                                                                                  pady=10,
                                                                                                                  padx=12,
                                                                                                                  sticky="w",
                                                                                                                  ipadx=10)
        Button(self.itemframe, text="Назад", height=3, width=8, bd=6, command=self.buildprodtable, bg="#FFFFFF").grid(
            row=6, column=1, padx=16, pady=10, sticky="e", ipadx=10)

    # ВЫПОЛНЯЕТ ПРОВЕРКУ И ДОБАВЛЯЕТ ТОВАРЫ
    def insertitem(self):
        # Проверяем текущую сумму остатков
        self.cur.execute("SELECT SUM(stocks) FROM products")
        total_stocks = self.cur.fetchone()[0]
        if total_stocks is None:
            total_stocks = 0

        # Проверяем, не превысит ли сумма 100 000 после добавления нового товара
        new_stock = int(self.newitemstock.get())
        if total_stocks + new_stock > 100000:
            messagebox.showerror("Ошибка", "Склад переполнен! Сумма остатков не может превышать 100 000.")
            return

        # Остальной код для добавления товара
        self.newitem.set((self.newitem.get()).upper())
        self.newitemdesc.set((self.newitem.get()).upper())
        self.newitemcat.set((self.newitem.get()).upper())
        if self.newitemcode.get() == '' or self.newitem.get() == '' or self.newitemdesc.get() == '':
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return
        elif self.newitemcat.get() == '' or self.newitemprice.get() == '' or self.newitemstock.get() == '':
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return
        else:
            l = [self.newitemcode.get(), self.newitemprice.get(), self.newitemstock.get()]
            for i in range(0, len(l)):
                if (not l[i].isdigit()):
                    if (i == 0):
                        messagebox.showerror("Ошибка", "Product ID должен быть числом")
                    else:
                        messagebox.showerror("Ошибка", "Неверные данные")
                    return
                elif (int(l[i]) < 0):
                    messagebox.showerror("Ошибка", "Неверные данные")
                    return
        self.cur.execute('select * from products where product_id = ?', (int(self.newitemcode.get()),))
        l = self.cur.fetchall()
        if (len(l) > 0):
            messagebox.showerror("Ошибка", "Product ID должен быть уникальным")
            return
        if (self.desc_name.count(self.newitemdesc.get()) != 0):
            messagebox.showerror('Ошибка', 'Материал с таким описанием уже существует!')
            return
        x = int(self.newitemcode.get())
        y = int(self.newitemprice.get())
        z = int(self.newitemstock.get())
        self.cur.execute("insert into products values(?,?,?,?,?,?)", (x, self.newitem.get(), self.newitemdesc.get(),
                                                                      self.newitemcat.get(), y, z))
        self.newitem.set('')
        self.newitemstock.set('')
        self.newitemprice.set('')
        self.newitemdesc.set('')
        self.newitemcode.set('')
        self.newitemcat.set('')
        messagebox.showinfo('Успешно', 'Материал успешно добавлен')
        self.base.commit()

    # СОЗДАНИЕ ТАБЛИЦЫ ПОЛЬЗОВАТЕЛЕЙ
    def buildusertable(self):
        self.searchframe.place_forget()
        self.formframe.place_forget()
        self.tableframe.place_forget()
        self.itemframe.place_forget()
        self.formframe1.place(self.formframe1info)
        self.tableframe1.place(self.tableframe1info)
        self.tree.delete(*self.tree.get_children())
        self.tree.grid_remove()
        self.tree.destroy()
        scrollbarx = Scrollbar(self.tableframe1, orient=HORIZONTAL)
        scrollbary = Scrollbar(self.tableframe1, orient=VERTICAL)
        self.tree = ttk.Treeview(self.tableframe1, columns=("Username", "Password", "Account Type"),
                                 selectmode="browse", height=17, yscrollcommand=scrollbary.set,
                                 xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=170)
        self.tree.column('#2', stretch=NO, minwidth=0, width=170)
        self.tree.column('#3', stretch=NO, minwidth=0, width=170)
        self.tree.heading('Username', text="Имя пользователя", anchor=W)
        self.tree.heading('Password', text="Пароль", anchor=W)
        self.tree.heading('Account Type', text="Тип доступа", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        self.getusers()
        self.tree.bind("<<TreeviewSelect>>", self.clickusertable)
        self.formframe1.focus_set()
        self.usernamedit = StringVar()
        self.passwordedit = StringVar()
        self.accedit = StringVar()
        va = 110
        l1 = ['Имя польз.', 'Пароль', 'Доступ']
        for i in range(0, 3):
            Label(self.formframe1, text=l1[i], font="roboto 14 bold", bg="#FFFFFF").place(x=0, y=va)
            va += 70
        Entry(self.formframe1, textvariable=self.usernamedit, font="roboto 14", bg="#FFFFFF", width=25,
              state='readonly').place(x=162, y=105, height=40)
        Entry(self.formframe1, textvariable=self.passwordedit, font="roboto 14", bg="#FFFFFF", width=25).place(x=162,
                                                                                                               y=175,
                                                                                                               height=40)
        profiles = mycombobox(self.formframe1, font="robot 14", width=23, textvariable=self.accedit)
        profiles.place(x=162, y=245, height=40)
        profiles.set_completion_list(['ADMIN', 'USER'])
        Button(self.formframe1, text="Регистрация", font="robot 12 bold", bg="#FFFFFF", bd=5, width=12, height=2,
               command=self.adduser).place(x=0, y=10)
        Button(self.formframe1, text="Обновить", font="robot 12 bold", bg="#FFFFFF", bd=5, width=10, height=2,
               command=self.changeusertable).place(x=145, y=381)
        Button(self.formframe1, text="Удалить", font="robot 12 bold", bg="#FFFFFF", bd=5, width=10, height=2,
               command=self.deluser).place(x=345, y=381)

        self.mainsearch(0)

    # ИЗВЛЕЧЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ИЗ ТАБЛИЦЫ ПОЛЬЗОВАТЕЛЕЙ
    def getusers(self, x=0):
        ans = ''
        self.cur.execute("select * from users")
        userslist = self.cur.fetchall()
        for i in userslist:
            self.tree.insert('', 'end', values=(i))
            if (str(x) == i[0]):
                a = self.tree.get_children()
                ans = a[len(a) - 1]

        return ans

    def changeusertable(self):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        self.usernamedit.set((self.usernamedit.get()).upper())
        self.passwordedit.set((self.passwordedit.get()).upper())
        self.accedit.set((self.accedit.get()).upper())
        if (len(li) == 3):
            if self.usernamedit.get() == '' or self.accedit.get() == '':
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
                return
            if (self.accedit.get() != 'ADMIN' and self.accedit.get() != 'USER'):
                messagebox.showerror("Ошибка", "Неизвестный тип аккаунта!")
                return
            self.cur.execute(
                "update users set password = ?,account_type = ? where username = ?;", (
                    self.passwordedit.get(), self.accedit.get(), self.usernamedit.get()))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            cur = self.getusers(li[0])
            self.tree.selection_set(cur)

    def deluser(self):
        cur = self.tree.focus()
        cur = self.tree.item(cur)
        li = cur['values']
        fa = 0
        if (self.username.get() == li[0]):
            if (messagebox.askyesno("Внимание!", "Удалить текущего пользователя?") == True):
                fa = 1
            else:
                return
        if messagebox.askyesno('Внимание!', 'Вы хотите удалить этот профиль?') == True and len(li) == 3:
            self.cur.execute("delete from users where username = ?;", (li[0],))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getusers()
            self.usernamedit.set('')
            self.passwordedit.set('')
            self.accedit.set('')
        if (fa == 1):
            self.change_user()

    def adduser(self):
        self.reguser()
        self.loginw.state('normal')  # ОКНО ВХОДА ОТКРЫВАЕТСЯ

    def searchuser(self):
        if (self.searchvar.get() == ''):
            return
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("select * from users")
        li = self.cur.fetchall()
        for i in li:
            if (i[0] == self.searchvar.get()):
                self.tree.insert('', 'end', values=(i))

    def resetusertable(self):
        self.searchvar.set('')
        self.tree.delete(*self.tree.get_children())
        self.getusers()

    def clickusertable(self, event):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if (len(li) == 3):
            self.usernamedit.set((li[0]))
            self.passwordedit.set((li[1]))
            self.accedit.set((li[2]))

    def buildsalestable(self):
        self.searchframe.place_forget()
        self.formframe.place_forget()
        self.tableframe.place_forget()
        self.itemframe.place_forget()
        self.formframe1.place_forget()
        self.tableframe1.place(x=1280, y=315, anchor=NE)
        self.tree.delete(*self.tree.get_children())
        self.tree.grid_remove()
        self.tree.destroy()
        scrollbarx = Scrollbar(self.tableframe1, orient=HORIZONTAL)
        scrollbary = Scrollbar(self.tableframe1, orient=VERTICAL)
        self.tree = ttk.Treeview(self.tableframe1, columns=("Invoice No.", "Product ID", "Description",
                                                            'Quantity', 'Total Price', 'Date', 'Time'),
                                 selectmode="browse", height=16,
                                 yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=140)
        self.tree.column('#2', stretch=NO, minwidth=0, width=150)
        self.tree.column('#3', stretch=NO, minwidth=0, width=170)
        self.tree.column('#4', stretch=NO, minwidth=0, width=130)
        self.tree.column('#5', stretch=NO, minwidth=0, width=130)
        self.tree.column('#6', stretch=NO, minwidth=0, width=130)
        self.tree.heading('Invoice No.', text="Счёт-фактура", anchor=W)
        self.tree.heading('Product ID', text="id продукта", anchor=W)
        self.tree.heading('Description', text="Описание", anchor=W)
        self.tree.heading('Quantity', text="Кол-во", anchor=W)
        self.tree.heading('Total Price', text="Общ цена", anchor=W)
        self.tree.heading('Date', text="Дата", anchor=W)
        self.tree.heading('Time', text="Время", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)

        # Инициализация метки для отображения общей суммы
        self.total_sales_label = Label(self.tableframe1, text="Общая сумма: 0", font="roboto 14 bold", bg="#FFFFFF")
        self.total_sales_label.place(x=0, y=400)

        # Загрузка данных и обновление общей суммы
        self.getsales()
        self.mainsearch(2)

    def getsales(self):
        self.cur.execute("SELECT * FROM sales")
        saleslist = self.cur.fetchall()
        for i in range(0, len(saleslist)):
            saleslist[i] = list(saleslist[i])
            # Получаем описание и цену продукта
            self.cur.execute("SELECT product_desc, product_price FROM products WHERE product_id=?",
                             (int(saleslist[i][2]),))
            l = self.cur.fetchall()
            if l:  # Проверяем, есть ли результаты запроса
                product_desc = l[0][0]
                product_price = l[0][1]
            else:  # Если продукт не найден, используем значения по умолчанию
                product_desc = "Unknown"
                product_price = 0

            s = (str(saleslist[i][4])).split('-')
            saleslist[i][4] = s[2] + " - " + s[1] + " - " + s[0]

            # Формируем строку для таблицы
            saleslist[i] = [
                saleslist[i][1],  # Invoice No.
                saleslist[i][2],  # Product ID
                product_desc,  # Description
                saleslist[i][3],  # Quantity
                product_price * (int(saleslist[i][3])),  # Total Price
                saleslist[i][4],  # Date
                saleslist[i][5],  # Time
            ]

            saleslist[i] = tuple(saleslist[i])

        for i in saleslist:
            self.tree.insert('', 'end', values=(i))

        # Обновляем общую сумму после добавления данных
        self.update_total_sales()

    def update_total_sales(self):
        # Считаем общую сумму всех "Общ цена"
        total_sales = 0
        for item in self.tree.get_children():
            try:
                # Индекс 5 - это "Общ цена"
                total_sales += float(self.tree.item(item, 'values')[5])
            except ValueError:
                # Если не удалось преобразовать в float, пропускаем это значение
                continue

        # Обновляем текст метки с общей суммой
        self.total_sales_label.config(text=f"Общая сумма: {total_sales}")

    def searchinvoice(self):
        # Открываем новое окно для поиска
        self.search_window = Toplevel(self.mainw)
        self.search_window.title("Поиск по параметрам")
        self.search_window.geometry("400x300")

        # Переменные для хранения значений полей ввода
        self.search_invoice = StringVar()
        self.search_product_id = StringVar()
        self.search_description = StringVar()  # Переменная для описания

        # Создаем поля ввода для параметров поиска
        Label(self.search_window, text="Номер счета:").grid(row=0, column=0, padx=10, pady=5)
        Entry(self.search_window, textvariable=self.search_invoice).grid(row=0, column=1, padx=10, pady=5)

        Label(self.search_window, text="ID продукта:").grid(row=1, column=0, padx=10, pady=5)
        Entry(self.search_window, textvariable=self.search_product_id).grid(row=1, column=1, padx=10, pady=5)

        Label(self.search_window, text="Описание:").grid(row=2, column=0, padx=10, pady=5)  # Поле для описания
        search_entry = myentry(self.search_window, textvariable=self.search_description, font="roboto 12", width=20)
        search_entry.grid(row=2, column=1, padx=10, pady=5)

        # Получаем список описаний из таблицы products
        self.cur.execute("SELECT DISTINCT product_desc FROM products")
        descriptions = [desc[0] for desc in self.cur.fetchall()]

        # Устанавливаем список автозаполнения для поля описания
        search_entry.set_completion_list(descriptions)

        # Кнопка для выполнения поиска
        Button(self.search_window, text="Поиск", command=self.perform_search).grid(row=3, column=0, columnspan=2,
                                                                                   pady=10)

    def perform_search(self):
        # Получаем значения из полей ввода
        invoice = self.search_invoice.get()
        product_id = self.search_product_id.get()
        description = self.search_description.get()

        # Формируем SQL-запрос с учетом введенных параметров
        query = """
            SELECT s.invoice, s.product_id, p.product_desc, s.quantity, p.product_price * s.quantity AS total_price, s.date, s.time
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            WHERE 1=1
        """
        params = []

        if invoice:
            query += " AND s.invoice = ?"
            params.append(invoice)
        if product_id:
            query += " AND s.product_id = ?"
            params.append(product_id)
        if description:
            query += " AND p.product_desc LIKE ?"
            params.append('%' + description + '%')

        # Выполняем запрос
        self.cur.execute(query, tuple(params))
        saleslist = self.cur.fetchall()

        # Очищаем текущую таблицу
        self.tree.delete(*self.tree.get_children())

        # Заполняем таблицу результатами поиска
        for i in range(0, len(saleslist)):
            saleslist[i] = list(saleslist[i])
            s = (str(saleslist[i][5])).split('-')  # Дата
            saleslist[i][5] = s[2] + " - " + s[1] + " - " + s[0]
            saleslist[i] = tuple(saleslist[i])

            self.tree.insert('', 'end', values=(saleslist[i]))

        # Закрываем окно поиска
        self.search_window.destroy()

    def search_by_description(self):
        if self.searchvar.get() == '':
            return
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT * FROM sales WHERE product_desc LIKE ?", ('%' + self.searchvar.get() + '%',))
        saleslist = self.cur.fetchall()
        for i in range(0, len(saleslist)):
            saleslist[i] = list(saleslist[i])
            self.cur.execute("SELECT product_desc, product_price FROM products WHERE product_id=?",
                             (int(saleslist[i][2]),))
            product_info = self.cur.fetchall()
            s = (str(saleslist[i][4])).split('-')
            saleslist[i][4] = s[2] + " - " + s[1] + " - " + s[0]
            if len(saleslist[i]) > 7:  # Проверяем, что столбец username существует
                username = saleslist[i][7]  # Получаем имя пользователя
            else:
                username = "Unknown"  # Если username отсутствует, используем значение по умолчанию
            if product_info:
                saleslist[i] = [username, saleslist[i][1], saleslist[i][2], product_info[0][0], saleslist[i][3],
                                product_info[0][1] * (int(saleslist[i][3])),
                                saleslist[i][4], saleslist[i][5]]
                saleslist[i] = tuple(saleslist[i])
            else:
                # Если product_info пусто, пропускаем эту запись
                continue
        for j in saleslist:
            if self.searchvar.get().lower() in j[3].lower():  # Проверяем совпадение по описанию
                self.tree.insert('', 'end', values=(j))
