import logging
from ast import literal_eval

import numpy as np
import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import (QPushButton, QTableWidget, QTableWidgetItem,
                             QWidget)

logger = logging.getLogger(__name__)


class ItemType(int):
    TYPE_DEFINITION = {
        object: 1000,
        int: 1001,
        np.integer: 1001,
        float: 1002,
        np.floating: 1002,
        str: 1003,
        np.character: 1003
    }

    def __new__(cls, item_type: type):
        key = item_type
        while(key != None):
            if key in ItemType.TYPE_DEFINITION:
                obj = int.__new__(cls, ItemType.TYPE_DEFINITION[key])
                obj.type = key
                obj.original_type = item_type

                if key == object:
                    logger.warn(f'Unknown Type: {item_type}')
                break
            else:
                key = key.__base__

        return obj

    def __init__(self, type: type) -> None:
        super().__init__()
        self.type = self.type
        self.original_type = self.original_type


class DataSheetItem(QTableWidgetItem):
    def __init__(self, text: str, item_type: ItemType = ItemType(object)):
        super().__init__(text, item_type)
        self.item_type = item_type

    def value(self):
        return self.item_type.type(self.text())


class DataSheetWidget(QWidget, uic.loadUiType('src/datasheet.ui')[0]):
    def __init__(self, excel_path=None) -> None:
        super().__init__()
        self.setupUi(self)
        self.data_widget: QTableWidget = self.data_widget
        self.add_col_button: QPushButton = self.add_col_button

        self.data_widget.cellChanged.connect(self.add_row)
        self.add_col_button.clicked.connect(self.add_col)

        if excel_path is not None:
            self.name, df = self.load_excel(excel_path)
            self.initialize_all(df)
        else:
            self.initialize_all()

    def load_excel(self, path: str):
        temp = pd.ExcelFile(path)
        df = temp.parse(header=0, index_col=0)
        name = temp.sheet_names[0]
        temp.close()

        return name, df

    def add_row(self, row: int):
        if row == self.data_widget.rowCount() - 1:
            self.data_widget.setRowCount(self.data_widget.rowCount() + 1)
            self.data_widget.setVerticalHeaderItem(self.data_widget.rowCount() - 2, None)

        self.data_widget.setVerticalHeaderItem(
            self.data_widget.rowCount() - 1, QTableWidgetItem('...'))

    def add_col(self):
        self.data_widget.setColumnCount(self.data_widget.columnCount() + 1)

    def initialize_all(self, data=pd.DataFrame(columns=['Value'])) -> None:
        self.data_widget.clear()
        data = data.fillna('')

        self.data_widget.setRowCount(data.shape[0] + 1)
        self.data_widget.setColumnCount(data.shape[1])

        for cidx, col_name in enumerate(data):
            col = data[col_name]
            for ridx, value in enumerate(col):
                val_type = ItemType(type(value))
                item = DataSheetItem(str(value), val_type)
                self.data_widget.setItem(ridx, cidx, item)

        self.data_widget.setHorizontalHeaderLabels([str(e) for e in data.columns])
        self.data_widget.setVerticalHeaderLabels([str(e) for e in data.index])

        self.data_widget.setVerticalHeaderItem(
            self.data_widget.rowCount() - 1, QTableWidgetItem('...'))

    def delete_row(self) -> None:
        for selection_range in self.data_widget.selectedRanges():
            print(
                f't: {selection_range.topRow()}, b: {selection_range.bottomRow()}')

        self.initialize_all()

    def export_to_dataframe(self):
        number_of_rows = self.data_widget.rowCount()
        number_of_columns = self.data_widget.columnCount()

        data = []

        for row_num in range(number_of_rows - 1):
            row = []
            for col_num in range(number_of_columns):
                item: DataSheetItem = self.data_widget.item(row_num, col_num)
                if item is not None:
                    row.append(item.value())
                else:
                    row.append('')
            data.append(row)

        column_labels = [
            self.data_widget.horizontalHeaderItem(n).text() 
            if self.data_widget.horizontalHeaderItem(n) is not None 
            else n 
            for n in range(number_of_columns)
        ]
        index_labels = [
            self.data_widget.verticalHeaderItem(n).text() 
            if self.data_widget.verticalHeaderItem(n) is not None 
            else n 
            for n in range(number_of_rows - 1)
        ]

        return pd.DataFrame(data, index=index_labels, columns=column_labels)
