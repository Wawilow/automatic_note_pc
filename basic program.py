# импортирую библиотеки необходимые для работы программы
import datetime
import time
import sys
import pyglet

# Ипортирую все виджеты для работы qt дизайнера
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTextBrowser


class WindowWhitchMessage(QMainWindow):
    def __init__(self):
        # вызываю родительский инит что бы окно работало
        super().__init__()
        # вызываю под функцию где будет
        # описано продолжение работы программы
        self.initUI()

    def initUI(self):
        # считываю время на компютере
        now = str(datetime.datetime.now())[:16]

        # подключаю мой файл сделаный в pqt
        uic.loadUi('Uwedomlenie.ui', self)
        # кнопки, окна и тд я задал в ui файле
        # что сократило обем программы

        # задаю название для окна
        self.setWindowTitle('Уведомление')

        # открываю таблицу с сервера
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
        f.close()

        # считываю сообщения которые записал пользователь
        # и преобрахововаю их в список
        self.message = [i for i in self.a]
        self.message = [i[0] for i in self.message]
        self.messageId = [i for i in self.a]
        self.messageId = [i[-2] for i in self.messageId]

        # создаю вотрой список с id сообщений что бы определить какое сообзение показывать
        for i in range(len(self.messageId)):
            # задаю переменную с конретным id
            id = self.messageId[i]
            id = id[1:-1]
            # в месседж задаеться нужное сообщение
            if id == now[11:13]:
                message = self.message[i]

        # сообщение задаеться в строку
        self.textBrowser.setText(message[1:-1])


class OpenMe:
    def __init__(self):
        # задаю промежуточную переменную
        t = []

        # завожу переенную с итоговым временем
        datatime = []

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
        # запускаю бесконечный цикл со считываниемм времени
        while True:
            # в начале цикла считываю время
            # что бы программа знала какое сейчас время
            now = str(datetime.datetime.now())[:16]
            # принчу время что бы понимать что все работает правильно
            print(now)
            # если время находиться в списке нужных нам
            if [now] in datatime:
                # то мы вызываем звук
                # вызываем функцией что бы
                # не завершать наш бесконечный цикл
                Sound()
                # и открываем окно
                # вызываем функцией что бы
                # не завершать наш бесконечный цикл
                Open()
            # ждем 60 секунд что бы обновить время
            # такой перерыв позволяет не нагрушать компютер
            time.sleep(60)



def Open():
    # безопасно открываем окно
    # если оно не откроеться звук всеравно будет играть
    app = QApplication(sys.argv)
    ex = WindowWhitchMessage()
    ex.show()
    app.exec()


def Sound():
    # загружаем звук
    song = pyglet.media.load('din-iphone.mp3')
    # играем звук
    song.play()


# бесконечный цикл служит для того
# чтобы если программа закроеться она открывалась снова
while True:
    OpenMe()