import sys
import sqlite3
from PyQt5 import uic
# Ипортирую все виджеты для работы qt дизайнера
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTextBrowser


class Window2(QMainWindow):
    def __init__(self):
        # вызываю родительский инит что бы окно работало
        super().__init__()

        # задаю название для окна
        self.setWindowTitle("Новая заметка")
        # подключаю мой файл сделаный в pqt
        uic.loadUi('ui_file.ui', self)
        # кнопки, окна и тд я задал в ui файле
        # что сократило обем программы

        # после нажатия кнопки вызываю функцию run
        self.but.clicked.connect(self.run)
        # подключаю масив на архитиктуре sql
        self.con = sqlite3.connect("Server.db")
        # задаю курсор в масива
        self.cur = self.con.cursor()

    def run(self):
        # получаю все введенные пользователем данные
        self.messag = self.massage.text()
        self.dat = self.date.text()
        self.hou = self.hour.text()
        self.minut = self.minute.text()

        # так как окно с текстом принимает только строки
        # обеденяю все получанные данные, что бы задать их в командную строку
        self.Nice = [self.messag + ' ' + self.dat + ' ' + self.hou + ' ' + self.minut]
        # задаю распакованный список в командную строку
        self.NewInTheTable.setText(*self.Nice)

        # запокововаю все данные в список, что бы отправить их на сервер
        self.a = [self.messag, self.dat, self.hou, self.minut]
        # открываю таблицу с сервера
        f = open("timing.txt", 'a')
        # записыаю данные на сервер
        f.write(str(self.a) + '\n')
        # сохроняю результат и закрываю
        f.close()

        # далее код для работы с sql таблицами
        # он закоментирован что бы не конфликтовать

        # con = sqlite3.connect("Server.db")
        # con = sqlite3.connect("Help.db")
        # cur = con.cursor()
        # query = "INSERT INTO Problem (id) VALUES ({})".format('2')
        # cur.execute(query)
        # self.NewInTheTable.setText(self.messag, self.dat, self.hou, self.minut)


class Window3(QMainWindow):
    def __init__(self):
        # вызываю родительский инит что бы окно работало
        super().__init__()

        # задаю название для окна
        self.setWindowTitle("Список заметок")

        # подключаю мой файл сделаный в pqt
        uic.loadUi('Window3.ui', self)
        # кнопки, окна и тд я задал в ui файле
        # что сократило обем программы

        # завожу счетчик нажатий на кнопку
        self.push = 0
        # вызываю функцию run после нажатия кнопки
        self.pushButton.clicked.connect(self.run)

    def run(self):
        # открываю архив с данными
        f = open("timing.txt", mode="rb")

        # считываю масив информации
        lines = f.readlines()
        # преобразововаю информацию из изночального вида в список
        a = [i[:len(i) - 2] for i in lines]
        a = [str(i) for i in a]
        a = [i[2:len(i) - 1] for i in a]
        a = [i[1:len(i) - 1] for i in a]
        # удаляю лишнии знаки
        # получившиеся при сохранении
        self.a = [i.split(', ') for i in a]
        # закрываю архив
        f.close()

        # создаю промежуточный списоки
        # список t идет для формирования списка datatime
        t = []
        # в datatime записываю все время
        datatime = []
        # бегу по списку а
        for i in self.a:
            # удаляю первый символ i
            i = i[1:]
            # перевожу дату в викторианкий формат
            year = i[0].split('.')
            # меняю расположение дат
            year = '-'.join([year[2], year[1], year[0]])
            # преобразововаю время в привычную нам форму записи
            i = [(f'{i[1]}:{i[2]}')]
            # собираю вместе дату и время
            t.append([year] + i)
        # бугу по списку t
        for j in t:
            # делаю промежуточный список k
            k = []
            # бегу по дате и времени
            for i in j:
                # убираю лишнии знаки
                i = i.split("'")
                # если перед минутой минутой нету 0 то добавляю его
                if len(i[-2]) == 1:
                    i[-2] = '0' + i[-2]
                # соеденяю получившийся результат
                i = ''.join(i)
                # собираю новый список аналогичный t
                k.append(i)
            # соеденяю получившиюсю информацию
            k = [k[0] + ' ' + k[1]]
            # формирую список со всем временем
            datatime.append(k)
        # делаю список time
        # что бы потом записать сообщение
        # что бы вывести на экран
        time = []
        for i in datatime:
            time.append(i[0])
        # вывожу время на экран с каф равным числу нажатий на кнопку
        self.textBrowser.setText(f'{time[self.push]}')

        # считываю новое нажатие
        self.push += 1
        # меняю содержимое кнопки
        self.pushButton.setText(f'Следующяя заметка. Всего заметок {len(datatime)}')


class Window(QMainWindow):
    def __init__(self):
        # вызываю родительский инит что бы окно работало
        super().__init__()

        # задаю название для окна
        self.title = "First Window"

        # делаю новую кнопку
        self.pushButton = QPushButton("Сделать новую заметку", self)
        # задаю размеры кнопки
        self.pushButton.resize(150, 50)
        # задаю положение кнопки
        self.pushButton.move(275, 200)
        self.pushButton.setToolTip("<h3>Start the Session</h3>")

        # делаю новую кнопку
        self.pushButton2 = QPushButton("Открвыть список заметок", self)
        # задаю размеры кнопки
        self.pushButton2.resize(150, 50)
        # задаю положение кнопки
        self.pushButton2.move(275, 400)
        self.pushButton2.setToolTip("<h3>Start the Session</h3>")

        # после нажатия на кнопку вызываеться функция окно3
        self.pushButton2.clicked.connect(self.window3)

        # после нажатия на кнопку вызываеться функция окно2
        self.pushButton.clicked.connect(self.window2)

        # вызываю функцию в которой
        # расписаны дальнейшии действия
        self.main_window()

        # задаю новые переменный принадлежащии классу окон
        self.Window2 = Window2()
        self.Window3 = Window3()

    def main_window(self):
        # задаю новое окно с пояснением
        self.label = QLabel(" ", self)
        # двигаю поеснение
        self.label.move(285, 175)
        # задаю новоы title
        self.setWindowTitle(self.title)
        # задаю размеры
        self.setGeometry(100, 100, 680, 500)
        # открываю окно
        self.show()

    def window2(self):
        # вызываю новое окно
        # он закроеться после нажатия на крестик
        self.Window2.show()

    def window3(self):
        # вызываю новое окно
        # он закроеться после нажатия на крестик
        self.Window3.show()


if __name__ == "__main__":
    # вызываю главное окно
    # после его закрытия закроються все окна
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())