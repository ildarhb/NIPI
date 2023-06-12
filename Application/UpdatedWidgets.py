from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class UpgradedQTableWidget(QTableWidget):

    def fill_names(self, rows, columns):
        self.VerticalHeaderLabels = rows
        self.HorizontalHeaderLabels = columns

        self.setRowCount(len(rows))
        self.setVerticalHeaderLabels(rows)

        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

    def get_table_items(self):
        row_count = self.rowCount()
        column_count = self.columnCount()
        table_data = list()

        for column_index in range(column_count):
            current_row = (self.item(row_index, column_index) for row_index in range(row_count))  # столбец таблицы
            current_row_text = (item.text() if item is not None else "" for item in current_row)  # текстовый столбец
            table_data.append(tuple(current_row_text))

        return table_data

    def get_dict_column(self, index=0):
        items = self.get_table_items()[index]
        names = self.VerticalHeaderLabels
        return {key: value for key, value in zip(names, items)}

    def fill_data(self, data: list):
        for ind_row, row in enumerate(data):
            for ind_item, item in enumerate(row):
                self.setItem(ind_row, ind_item, QTableWidgetItem(str(item)))
