from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor


class UpgradedTableWidget:
    def __init__(self, qt_table: QTableWidget):
        self.table = qt_table
        self.VerticalHeaderLabels = tuple()
        self.HorizontalHeaderLabels = tuple()

    def fill_labels(self, vertical, horizontal):
        self.fill_VerticalLabels(vertical)
        self.fill_HorizontalLabels(horizontal)

    def fill_HorizontalLabels(self, labels):
        self.HorizontalHeaderLabels = tuple(labels)
        self.table.setColumnCount(len(self.HorizontalHeaderLabels))
        self.table.setHorizontalHeaderLabels(self.HorizontalHeaderLabels)

    def fill_VerticalLabels(self, labels):
        self.VerticalHeaderLabels = tuple(labels)
        self.table.setRowCount(len(self.VerticalHeaderLabels))
        self.table.setVerticalHeaderLabels(self.VerticalHeaderLabels)

    def dict_column(self, index=0):
        names = self.VerticalHeaderLabels
        items = [item[index] for item in self.items()]
        return dict(zip(names, items))

    def dict_row(self, row=0):
        names = self.HorizontalHeaderLabels
        items = self.items()[row]
        return dict(zip(names, items))

    def fill_data(self, data):
        for ind_row, row in enumerate(data):
            self.fill_row(row, ind_row)

    def fill_row(self, row, row_index):
        for ind_item, item in enumerate(row):
            self.table.setItem(row_index, ind_item, QTableWidgetItem(str(item)))

    def fill_column(self, column, col_index):
        for ind_item, item in enumerate(column):
            self.table.setItem(ind_item, col_index, QTableWidgetItem(str(item)))

    def items(self):
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()
        table_data = list()

        for row_index in range(row_count):
            current_row = (self.table.item(row_index, column_index) for column_index in range(column_count))  # строка таблицы
            current_row_text = (item.text() if item is not None else "" for item in current_row)  # текстовый столбец
            table_data.append(tuple(current_row_text))

        return table_data

    def fill_data_dict(self, data_dict: dict, horizontal_label=''):
        vertical_labels = tuple(data_dict.keys())
        horizontal_labels = (horizontal_label, )
        self.fill_labels(vertical_labels, horizontal_labels)
        column = data_dict.values()
        self.fill_column(column, 0)

    def colorize_items(self, text: str, color: QColor):
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()

        for row in range(row_count):
            for column in range(column_count):
                item = self.table.item(row, column)
                if item.text() == text:
                    item.setBackground(color)
                    self.table.setItem(row, column, item)

    def clear(self, keepHorzontalLabels=False, keepVerticalLabels=False):
        self.table.clear()

        if keepHorzontalLabels:
            self.fill_HorizontalLabels(self.HorizontalHeaderLabels)
            self.table.setColumnCount(len(self.HorizontalHeaderLabels))
        else:
            self.HorizontalHeaderLabels = tuple()
            self.table.setColumnCount(0)

        if keepVerticalLabels:
            self.fill_VerticalLabels(self.VerticalHeaderLabels)
            self.table.setRowCount(len(self.VerticalHeaderLabels))
        else:
            self.VerticalHeaderLabels = tuple()
            self.table.setRowCount(0)

    def add_column(self, amount=1):
        self.table.setColumnCount(self.table.columnCount() + amount)

        




