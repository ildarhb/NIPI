from PyQt5 import QtWidgets
import sys
from MainWindow import Window


def create_app():
    app = QtWidgets.QApplication(sys.argv)
    try:
        win = Window()
    except FileNotFoundError as err:
        Window.show_error('Не найдены файлы Дизайнера',
                          'Рядом с исполняемым файлом должна быть папка UI, содержащая .ui файлы',
                          str(err))
        return
    except Exception as err:
        Window.show_error('Ошибка создания окна', str(err))
        return
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    create_app()

