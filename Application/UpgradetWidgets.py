from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class UpgradedTableWidget:
    def __init__(self, qt_table: QTableWidget):
        self.table = qt_table
        self.VerticalHeaderLabels = tuple()
        self.HorizontalHeaderLabels = tuple()

    def fill_labels(self, rows, columns):
        self.VerticalHeaderLabels = tuple(rows)
        self.HorizontalHeaderLabels = tuple(columns)

        self.table.setRowCount(len(self.VerticalHeaderLabels))
        self.table.setVerticalHeaderLabels(self.VerticalHeaderLabels)

        self.table.setColumnCount(len(self.HorizontalHeaderLabels))
        self.table.setHorizontalHeaderLabels(self.HorizontalHeaderLabels)

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

    def items(self):
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()
        table_data = list()

        for row_index in range(row_count):
            current_row = (self.table.item(row_index, column_index) for column_index in range(column_count))  # строка таблицы
            current_row_text = (item.text() if item is not None else "" for item in current_row)  # текстовый столбец
            table_data.append(tuple(current_row_text))

        return table_data
