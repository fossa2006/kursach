import sqlite3
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from Userlogin import Login
from Admin_menu import Admin
from User_menu import User
import pandas as pd  # Для экспорта данных в Excel

# ОСНОВНОЕ ОКНО
class Main(Login, Admin, User):
    def __init__(self):
        Login.__init__(self)
        self.loginw.mainloop()  # Запускаем окно входа
        self.loginw.state('withdraw')  # Скрываем окно входа

        # Создаем основное окно только после успешного входа
        self.mainw = Toplevel(bg="#FFFFFF")
        width = 1400
        height = 780
        screen_width = self.mainw.winfo_screenwidth()
        screen_height = self.mainw.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.mainw.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.mainw.title("Инвентаризация")
        self.mainw.resizable(0, 0)
        self.mainw.protocol('WM_DELETE_WINDOW', self.__Main_del__)
        self.getdetails()

        # Добавляем кнопки для смены языка
        self.current_language = 'ru'  # Устанавливаем язык по умолчанию
        self.create_language_buttons()

        # Инициализация переменной для общей суммы трат
        self.total_sales_label = None

    def __Main_del__(self):
        if messagebox.askyesno("Выход", "Покинуть Инвентаризацию?") == True:
            self.loginw.quit()
            self.mainw.quit()
            exit(0)
        else:
            pass

    def getdetails(self):
        self.cur.execute("CREATE TABLE if not exists products(product_id varchar (20),product_name varchar (50) NOT NULL,product_desc varchar (50) NOT NULL,product_cat varchar (50),product_price INTEGER NOT NULL,stocks INTEGER NOT NULL,PRIMARY KEY(product_id));")
        self.cur.execute("CREATE TABLE if not exists sales (Trans_id	INTEGER,invoice	INTEGER NOT NULL,Product_id	varchar (20),Quantity INTEGER NOT NULL,Date	varchar (20),Time varchar (20),username VARCHAR(20),PRIMARY KEY(Trans_id));")
        self.cur.execute("select * from products ")
        self.products = self.cur.fetchall()
        capuser = self.username.get()
        capuser = capuser.upper()
        self.cur.execute("select account_type from users where username= ? ", (capuser,))
        l = self.cur.fetchall()
        self.account_type = l[0][0]
        self.buildmain()

    def buildmain(self):
        if self.account_type == 'ADMIN':
            super(Admin).__init__()
            self.admin_mainmenu(8, 8)
        else:
            super(User).__init__()
            self.user_mainmenu(8, 8)
        self.logout.config(command=self.__Main_del__)
        self.changeuser.config(command=self.change_user)
        self.topframe = LabelFrame(self.mainw, width=1400, height=120, bg="#4267b2")
        self.topframe.place(x=0, y=0)
        self.store_name = 'Логиститическая'
        self.storelable = Label(self.topframe, text=self.store_name + " Система цеха", bg="#4267b2", anchor="center")
        self.storelable.config(font="Roboto 30 bold", fg="snow")
        self.storelable.place(x=360, y=30)
        mi = PhotoImage(file="images/myprofile.png")
        mi = mi.subsample(4, 4)
        self.myprofile = ttk.Label(self.topframe, text=(self.username.get()).capitalize(), image=mi, compound=TOP)
        self.myprofile.image = mi
        self.myprofile.place(x=1300, y=15)

        # Добавляем кнопки для смены языка
        self.create_language_buttons()

    def create_language_buttons(self):
        self.ru_button = Button(self.topframe, text="RU", command=lambda: self.change_language('ru'))
        self.ru_button.place(x=1200, y=10)

        self.en_button = Button(self.topframe, text="EN", command=lambda: self.change_language('en'))
        self.en_button.place(x=1250, y=10)

        # Добавляем кнопку "Экспорт в Excel"
        self.export_excel_button = Button(self.topframe, text="Экспорт в Excel", command=self.export_to_excel)
        self.export_excel_button.place(x=1050, y=10)  # Укажите подходящее место для кнопки

    def change_language(self, lang):
        self.current_language = lang
        self.translate_interface()

    def translate_interface(self):
        translations = {
            'ru': {
                'Инвентаризация': 'Инвентаризация',
                'Выйти': 'Выйти',
                'Сменить пользователя': 'Сменить пользователя',
                'Профили': 'Профили',
                'добавить': 'добавить',
                'Инвентаризация': 'Инвентаризация',
                'Траты': 'Траты',
                'Поиск': 'Поиск',
                'Сбросить': 'Сбросить',
                'Обновить': 'Обновить',
                'Удалить': 'Удалить',
                'Добавить товар': 'Добавить товар',
                'Назад': 'Назад',
                'id продукта': 'id продукта',
                'Имя продукта': 'Имя продукта',
                'Описание': 'Описание',
                'Категория': 'Категория',
                'Цена': 'Цена',
                'Остаток': 'Остаток',
                'Добавить': 'Добавить',
                'Кол-во': 'Кол-во',
                'Сумма к оплате': 'Сумма к оплате',
                'Номер счета': 'Номер счета',
                'id оплаты': 'id оплаты',
                'Название продукта': 'Название продукта',
                'Дата': 'Дата',
                'Время': 'Время',
                'Пользователь с таким именем уже существует!': 'Пользователь с таким именем уже существует!',
                'Неизвестный тип аккаунта!': 'Неизвестный тип аккаунта!',
                'Данные пользователя успешно обновлены!': 'Данные пользователя успешно обновлены!',
                'Вы хотите удалить этот профиль?': 'Вы хотите удалить этот профиль?',
                'Вы хотите удалить товар из инвентаризации?': 'Вы хотите удалить товар из инвентаризации?',
                'Пожалуйста, заполните все поля': 'Пожалуйста, заполните все поля',
                'Неверные данные': 'Неверные данные',
                'Товар успешно добавлен': 'Товар успешно добавлен',
                'Транзакция успешно завершена!': 'Транзакция успешно завершена!',
                'Корзина пуста!': 'Корзина пуста!',
                'Вы хотите продолжить?': 'Вы хотите продолжить?',
                'Удалить корзину?': 'Удалить корзину?',
                'Распечатать эту транзакцию?': 'Распечатать эту транзакцию?',
                'Товар с таким описанием уже существует!': 'Товар с таким описанием уже существует!',
                'Product ID должен быть уникальным': 'Product ID должен быть уникальным',
                'Product ID должен быть числом': 'Product ID должен быть числом',
                'Товар с таким количеством недоступен!': 'Товар с таким количеством недоступен!',
                'Товар отсутствует в наличии!': 'Товар отсутствует в наличии!',
                'Неверное количество!': 'Неверное количество!',
                'Не выбрана корзина': 'Не выбрана корзина',
                'Вы хотите сменить пользователя?': 'Вы хотите сменить пользователя?',
                'Выход': 'Выход',
                'Пользователь зарегистрирован': 'Пользователь зарегистрирован',
                'Неверное имя пользователя или пароль': 'Неверное имя пользователя или пароль',
                'Имя пользователя уже существует': 'Имя пользователя уже существует',
                'Выберите имя пользователя': 'Выберите имя пользователя',
                'Создайте пароль': 'Создайте пароль',
                'Назад': 'Назад',
                'ОК': 'ОК',
                'Внимание!': 'Внимание!',
                'Внимание': 'Внимание',
                'Вы хотите удалить текущего пользователя?': 'Вы хотите удалить текущего пользователя?',
                'Удалить текущего пользователя?': 'Удалить текущего пользователя?',
                'Транзакция успешно завершена': 'Транзакция успешно завершена',
                'Диаграмма': 'Диаграмма',  # Добавлено для русского языка
            },
            'en': {
                'Инвентаризация': 'Inventory',
                'Выйти': 'Logout',
                'Сменить пользователя': 'Change User',
                'Профили': 'Profiles',
                'добавить': 'Add',
                'Инвентаризация': 'Inventory',
                'Траты': 'Expenses',
                'Поиск': 'Search',
                'Сбросить': 'Reset',
                'Обновить': 'Update',
                'Удалить': 'Delete',
                'Добавить товар': 'Add Item',
                'Назад': 'Back',
                'id продукта': 'Product ID',
                'Имя продукта': 'Product Name',
                'Описание': 'Description',
                'Категория': 'Category',
                'Цена': 'Price',
                'Остаток': 'Stock',
                'Добавить': 'Add',
                'Кол-во': 'Quantity',
                'Сумма к оплате': 'Total Amount',
                'Номер счета': 'Invoice Number',
                'id оплаты': 'Transaction ID',
                'Название продукта': 'Product Name',
                'Дата': 'Date',
                'Время': 'Time',
                'Пользователь с таким именем уже существует!': 'User with this name already exists!',
                'Неизвестный тип аккаунта!': 'Unknown account type!',
                'Данные пользователя успешно обновлены!': 'User data updated successfully!',
                'Вы хотите удалить этот профиль?': 'Do you want to delete this profile?',
                'Вы хотите удалить товар из инвентаризации?': 'Do you want to delete the item from inventory?',
                'Пожалуйста, заполните все поля': 'Please fill in all fields',
                'Неверные данные': 'Invalid data',
                'Товар успешно добавлен': 'Item added successfully',
                'Транзакция успешно завершена!': 'Transaction completed successfully!',
                'Корзина пуста!': 'Cart is empty!',
                'Вы хотите продолжить?': 'Do you want to continue?',
                'Удалить корзину?': 'Delete cart?',
                'Распечатать эту транзакцию?': 'Print this transaction?',
                'Товар с таким описанием уже существует!': 'Item with this description already exists!',
                'Product ID должен быть уникальным': 'Product ID must be unique',
                'Product ID должен быть числом': 'Product ID must be a number',
                'Товар с таким количеством недоступен!': 'Item with this quantity is not available!',
                'Товар отсутствует в наличии!': 'Item is out of stock!',
                'Неверное количество!': 'Invalid quantity!',
                'Не выбрана корзина': 'No cart selected',
                'Вы хотите сменить пользователя?': 'Do you want to change the user?',
                'Выход': 'Exit',
                'Пользователь зарегистрирован': 'User registered',
                'Неверное имя пользователя или пароль': 'Invalid username or password',
                'Имя пользователя уже существует': 'Username already exists',
                'Выберите имя пользователя': 'Choose a username',
                'Создайте пароль': 'Create a password',
                'Назад': 'Back',
                'ОК': 'OK',
                'Внимание!': 'Attention!',
                'Внимание': 'Attention',
                'Вы хотите удалить текущего пользователя?': 'Do you want to delete the current user?',
                'Удалить текущего пользователя?': 'Delete current user?',
                'Транзакция успешно завершена': 'Transaction completed successfully',
                'Диаграмма': 'Chart',  # Добавлено для английского языка
            }
        }

        # Обновляем текст всех элементов интерфейса
        self.storelable.config(text=translations[self.current_language]['Инвентаризация'])
        self.logout.config(text=translations[self.current_language]['Выйти'])
        self.changeuser.config(text=translations[self.current_language]['Сменить пользователя'])
        self.accounts.config(text=translations[self.current_language]['Профили'])
        self.items.config(text=translations[self.current_language]['добавить'])
        self.stocks.config(text=translations[self.current_language]['Инвентаризация'])
        self.sales.config(text=translations[self.current_language]['Траты'])
        self.searchbut.config(text=translations[self.current_language]['Поиск по Описанию'])
        self.resetbut.config(text=translations[self.current_language]['Сбросить'])
        self.pie_chart_button.config(text=translations[self.current_language]['Диаграмма'])

    def change_user(self):
        if messagebox.askyesno("Внимание!", "Вы хотите сменить пользователя?") == True:
            self.base.commit()
            self.mainw.destroy()
            self.loginw.destroy()
            self.__init__()

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

    def export_to_excel(self):

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


if __name__ == '__main__':
    w = Main()
    w.base.commit()
    w.mainw.mainloop()