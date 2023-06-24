from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QFileDialog, QMessageBox, QMainWindow
from Calculation import initdata, calculation
from WindowData import WindowData
from CacheFile import CacheFile
from UpgradetWidgets import UpgradedTableWidget


class Window(QMainWindow):
    def __init__(self):
        # Инициализация
        super(Window, self).__init__()
        self.ui = uic.loadUi("UIWindow.ui", self)

        # НАЗНАЧЕНИЕ ПЕРЕМЕННЫХ
        self.WindowData = WindowData()  # Класс со всеми входными данными
        self.cache_gelling = None  # гелеобразующие составы
        # файлы кэша
        self.cachefile_gelling = CacheFile("Gelling")
        self.cachefile_gelling_selected = CacheFile("Gelling_selected")
        self.cachefile_tableBeforeWatering = CacheFile("TableBeforeWatering")
        self.cachefile_tableAfterWatering = CacheFile("TableAfterWatering")
        self.cachefile_tableWatering = CacheFile("TableWatering")
        # выпадающие списки
        self.combobox_gelling1 = self.ui.comboGelling1  # Выпадающий список с гелеобразующими составами
        self.combobox_gelling2 = self.ui.comboGelling2
        self.combobox_gelling3 = self.ui.comboGelling3
        # таблицы
        self.tableWatering = UpgradedTableWidget(self.ui.tableWatering)  # ГИС
        self.tableGelling = UpgradedTableWidget(self.ui.tableWidgetGelling)  # Гелеобразующие составы
        self.tableAfterWatering = UpgradedTableWidget(self.ui.tableAfterWatering)  # Данные после обводнения
        self.tableBeforeWatering = UpgradedTableWidget(self.ui.tableBeforeWatering)  # Данные до обводнения

        # Связывание кнопок (событий) с функциями (слотами)
        self.ui.btnGetData.clicked.connect(self.btn_getdata_clicked)  # Получить данные
        self.ui.bntCalculate.clicked.connect(self.btn_calculate_clicked)  # Рассчитать
        self.ui.btnAddGelling.clicked.connect(self.btn_addgelling_clicked)  # Добавить гелеобразующий состав
        self.combobox_gelling1.currentIndexChanged.connect(self.combobox_gelling_changed1)  # Выбор гелеобразующего состава
        self.combobox_gelling2.currentIndexChanged.connect(self.combobox_gelling_changed2)
        self.combobox_gelling3.currentIndexChanged.connect(self.combobox_gelling_changed3)

        # инициализация моих функций
        self.init_table_after_watering()
        self.init_table_before_watering()
        self.init_table_gelling()
        self.init_gelling_items()
        self.init_table_watering()

    def closeEvent(self, *args, **kwargs):
        self.save_data()
        return super().closeEvent(*args, **kwargs)

    # ФУНКЦИИ ИНИЦИАЛИЗАЦИИ

    def init_table_after_watering(self):
        table = self.tableAfterWatering

        rows = ('Пласт',
                   'Pпл, атм',
                   'Pзаб, атм',
                   'Qж, м3/сут',
                   'Qг, тыс. м3/сут',
                   'ВГФ, м3/тыс. м3',
                   'Dэ/к, мм',
                   'Dнкт, мм',
                   'Rс, м',
                   'Hвд, м',
                   'Удл, м',
                   'D скв. дол., мм',
                   'Н перф, м',
                   'Толщина стенок НКТ, мм',
                   'Толщина стенок Э/К, мм',
                   'Давл. опрессовки, атм',
                   'Закачка с пакером',
                   'Вяз-ть пл.воды, сПз',
                   'Вяз-ть газа, сПз',
                   'Плотность газа,  г/см3',
                   'Пл-ть пл.воды, г/см3',
                   'К-т сверхсжимаемости газа',
                   'ΔT м/у устьем и забоем, ℃',
                   'Pбуф, атм',
                   'P конечное на устье, атм;',
                   'Расход жидкости, м3/сут',
                   'Pзаб план-е после РИР, атм')

        table.fill_labels(rows, ('Данные',))

        cache = self.cachefile_tableAfterWatering.read()
        if cache is not None:
            table.fill_data(self.cachefile_tableAfterWatering.read())

    def init_table_before_watering(self):
        table = self.tableBeforeWatering

        rows = ('Пласт',
                'Pпл, атм',
                'Pзаб, атм',
                'Qж, м3/сут',
                'Qг, тыс. м3/сут',
                'ВГФ, м3/тыс. м3')

        table.fill_labels(rows, ('Данные',))

        cache = self.cachefile_tableBeforeWatering.read()
        if cache is not None:
            table.fill_data(cache)

    def init_table_gelling(self):
        columns = DialogAddGelling.columns.copy()  # получаем колонки из объекта добавления составов
        columns.pop('Name')
        rows = ('1', '2', '3')

        self.tableGelling.fill_labels(rows, columns)

    def init_table_watering(self):
        cache = self.cachefile_tableWatering.read()
        if cache is None:
            return

        self.tableWatering.fill_labels(cache['vertical'], cache['horizontal'])
        self.tableWatering.fill_data(cache['data'])

    # ОБРАБОТЧИКИ СОБЫТИЙ

    def btn_getdata_clicked(self):  # Нажатие на кнопку "получить данные"
        self.tableWatering.table.clear()
        self.load_data()

    def btn_calculate_clicked(self):  # Нажатие на кнопку "рассчитать"
        self.fill_WindowData()
        calculation.get_const(self.WindowData)
        res_list = calculation.calculation_click(self.WindowData)
        radius, stability, _, _ = tuple(res_list)
        result_window = DialogResult(radius, stability, self.WindowData)
        result_window.show()

    def btn_addgelling_clicked(self):  # Нажатие на кнопку "Добавить гелеобразующий состав"
        dialog_gelling = DialogAddGelling(self.cachefile_gelling)  # создаем окно выбора полимеров
        res = dialog_gelling.add_data()  # вызываем окно
        if res is None:
            return
        (name, new_gelling) = res
        self.cache_gelling = self.cachefile_gelling.read()
        self.combobox_gelling1.addItem(name)
        self.combobox_gelling2.addItem(name)
        self.combobox_gelling3.addItem(name)

    def combobox_gelling_changed1(self):
        gelling_key = self.combobox_gelling1.currentText()

        self.fill_table_gelling(1, gelling_key)

    def combobox_gelling_changed2(self):
        gelling_key = self.combobox_gelling2.currentText()

        self.fill_table_gelling(2, gelling_key)

    def combobox_gelling_changed3(self):
        gelling_key = self.combobox_gelling3.currentText()

        self.fill_table_gelling(3, gelling_key)

    # ПРОЧИЕ ФУНКЦИИ

    def load_data(self):  # Загружает данные в таблицу из входного Excel

        file_name = QFileDialog.getOpenFileName(self, 'Открыть файл')

        try:
            file_data = initdata.get_gis(file_name[0])
        except BaseException:
            Window.show_error(informative_text='Не удалось прочитать файл с данными')
            return
            # raise ImportError("Не удалось прочитать файл с данными")

        self.init_gis_to_table(file_data, self.tableWatering)

    def fill_WindowData(self):  # Заполнение класса WindowData
        self.WindowData.gis = self.table_to_init_gis(self.tableWatering.items())

        self.WindowData.gis_after_watering = self.tableAfterWatering.dict_column()
        self.WindowData.gis_before_watering = self.tableBeforeWatering.dict_column()

        gelling_columns = DialogAddGelling.columns
        gelling_columns.pop('Name')
        for index, item in enumerate(self.tableGelling.items()):
            self.WindowData.gelling[index] = dict(zip(gelling_columns, item))

    def init_gelling_items(self):  # обновляем данные в выпадающих списках
        self.combobox_gelling1.clear()
        self.combobox_gelling2.clear()
        self.combobox_gelling3.clear()

        self.cache_gelling = self.cachefile_gelling.read()

        if self.cache_gelling is None:
            return

        if len(self.cache_gelling) == 0:
            return

        for gelling in self.cache_gelling:
            self.combobox_gelling1.addItem(gelling)
            self.combobox_gelling2.addItem(gelling)
            self.combobox_gelling3.addItem(gelling)

        self.fill_table_gelling(1, self.combobox_gelling1.currentText())
        self.fill_table_gelling(2, self.combobox_gelling2.currentText())
        self.fill_table_gelling(3, self.combobox_gelling3.currentText())

        combo_gelling_mas = (self.combobox_gelling1, self.combobox_gelling2, self.combobox_gelling3)
        for index, key in enumerate(self.cachefile_gelling_selected.read()):
            if key == '':
                continue
            combo_index = combo_gelling_mas[index].findText(key)
            if combo_index == -1:
                continue
            combo_gelling_mas[index].setCurrentIndex(combo_index)
            self.fill_table_gelling(index + 1, key)

    def fill_table_gelling(self, num: int, key: str):
        if key == '':
            return

        num -= 1  # индекс стоки на 1 меньше номера строки

        gelling_data = self.cache_gelling[key]
        data = gelling_data.values()
        self.tableGelling.fill_row(data, num)

    def save_data(self):  # сохраняем данные при закрытии проги
        self.cachefile_tableBeforeWatering.write(self.tableBeforeWatering.items())
        self.cachefile_tableAfterWatering.write(self.tableAfterWatering.items())

        gelling1 = self.combobox_gelling1.currentText()
        gelling2 = self.combobox_gelling2.currentText()
        gelling3 = self.combobox_gelling3.currentText()
        selected = (gelling1, gelling2, gelling3)
        self.cachefile_gelling_selected.write(selected)

        dict_gis = {'vertical': self.tableWatering.VerticalHeaderLabels,
                    'horizontal': self.tableWatering.HorizontalHeaderLabels,
                    'data': self.tableWatering.items()}
        self.cachefile_tableWatering.write(dict_gis)

    @staticmethod
    def init_gis_to_table(file_data: list, table: UpgradedTableWidget):  # костыльный метод для отделения мух от котлет
        if len(file_data) < 2:  # Название и 1-й столбец
            return

        vertical_labels = tuple(file_data[0].__dict__.values())[1:]

        file_data.pop(0)  # удаляем колонку с именами
        horizontal_labels = tuple(interval.name for interval in file_data)

        vertical_keys = tuple(file_data[0].__dict__.keys())[1:]
        data = tuple(tuple(col.__dict__[key] for col in file_data) for key in vertical_keys)
        table.fill_labels(vertical_labels, horizontal_labels, )
        table.fill_data(data)

    @staticmethod
    def table_to_init_gis(data):
        if len(data) == 0:
            return None

        intervals = len(data[0])
        # использует тот факт, что Ильдару не нужны имена для расчетов и передаем пустую строку в имени
        return [initdata.InitGis('', *tuple(data[index][interval] for index in range(len(data)))) for interval in range(intervals)]

    @staticmethod
    def show_error(text='Error', informative_text='More information', title='Error'):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(informative_text)
        msg.setWindowTitle(title)
        msg.exec_()


class DialogAddGelling(QDialog):
    columns = {"Name": None,
               "К, Па*с": None,
               "n": None,
               "Rост_в": None,
               "Rост_г": None,
               "Кр.гр.дав_в, атм/м": None,
               "Кр.гр.дав_г, атм/м": None,
               "Q, м3/сут": None,
               "V, м3": None,
               "Пл-ть, г/см3": None,
               "Время геле-обр-я., мин": None}

    def __init__(self, cache_file):
        super(DialogAddGelling, self).__init__()
        self.ui = uic.loadUi("DialogAddGelling.ui", self)
        self.setWindowTitle("Добавление гелеобразующего состава")
        self.cache_file = cache_file
        self.table = UpgradedTableWidget(self.ui.tableWidgetGelling)
        self.init_table()

    def init_table(self):
        self.table.fill_labels(('Состав', ), self.columns.keys())

    def add_data(self):
        if self.exec() == 0:  # Если закрыли окно
            return

        gelling_container = self.cache_file.read()  # считываем данные с файла
        if gelling_container is None:
            gelling_container = dict()

        column_dict = self.table.dict_row()

        name_gelling = ''
        new_gelling = dict()
        for key in column_dict:

            if key == 'Name':
                name_gelling = column_dict[key]
                if name_gelling == '':
                    return None
                else:
                    gelling_container[name_gelling] = new_gelling
                continue

            new_gelling[key] = column_dict[key]

        self.cache_file.write(gelling_container)
        return (name_gelling, self.columns)


class DialogResult(QMainWindow):
    def __init__(self, radius, stability, window_data: WindowData):
        super(DialogResult, self).__init__()
        self.ui = uic.loadUi('ResultWindow.ui', self)
        self.setWindowTitle("Вывод результатов вычислений")

        self.radius = radius
        self.stability = stability
        self.window_data = window_data

        self.table_radius = UpgradedTableWidget(self.ui.table_radius)
        self.table_stability = UpgradedTableWidget(self.ui.table_stability)

        self.ui.btn_show_radius.clicked.connect(self.show_radius)
        self.ui.btn_show_injection.clicked.connect(self.show_injection)
        self.ui.btn_show_radius_2.clicked.connect(self.show_radius2)

        self.fill_radius_table()
        self.fill_stability_table()

    def show_radius(self):
        calculation.get_radius_image(self.window_data)

    def show_injection(self):
        calculation.get_injection_image(self.window_data)

    def show_radius2(self):
        calculation.get_radius_graph(self.window_data)

    def fill_radius_table(self):
        table = self.table_radius

        if len(self.radius) == 0:
            return

        column_names = self.radius[0]
        column_names.pop(0)
        row_names = list(map(lambda x: x[0], self.radius))
        row_names.pop(0)

        self.radius.pop(0)
        for row in self.radius:
            row.pop(0)

        table.fill_labels(row_names, column_names)
        table.fill_data(self.radius)

    def fill_stability_table(self):
        table = self.table_stability

        if len(self.stability) == 0:
            return

        column_names = self.stability[0]
        column_names.pop(0)
        row_names = list(map(lambda x: x[0], self.stability))
        row_names.pop(0)

        self.stability.pop(0)
        for row in self.stability:
            row.pop(0)

        table.fill_labels(row_names, column_names)
        table.fill_data(self.stability)
