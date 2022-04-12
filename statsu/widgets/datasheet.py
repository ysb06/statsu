import logging
from ast import literal_eval
import time

import numpy as np
import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import (QPushButton, QTableWidget, QTableWidgetItem,
                             QWidget)

logger = logging.getLogger(__name__)


class DataSheetWidget(QWidget, uic.loadUiType('statsu/widgets/datasheet.ui')[0]):
    def __init__(self, initial_data=pd.DataFrame([[1]], columns=['id']), name='sheet', path=None) -> None:
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.path = path

        self.data_widget: QTableWidget = self.data_widget
        self.add_col_button: QPushButton = self.add_col_button

        self.data_widget.cellChanged.connect(self.add_row)
        self.data_widget.cellChanged.connect(self.change_value)
        self.add_col_button.clicked.connect(self.add_col)

        self.data = initial_data
        self.update_col()
        self.update_row()
        self.update_value()

    def update_row(self):
        self.data_widget.setRowCount(self.data.shape[0] + 1)
        self.data_widget.setVerticalHeaderLabels(
            [str(e) for e in self.data.index]
        )

        self.data_widget.setVerticalHeaderItem(
            self.data_widget.rowCount() - 1,
            QTableWidgetItem('...')
        )

    def update_col(self):
        self.data_widget.setColumnCount(self.data.shape[1])
        self.data_widget.setHorizontalHeaderLabels(
            [str(e) for e in self.data.columns]
        )

    def update_value(self):
        refined_data = self.data.fillna('')
        # 왜 nan -> '' 변환이 일어나는가?

        for cidx, col_name in enumerate(refined_data):
            col = refined_data[col_name]
            for ridx, value in enumerate(col):
                self.data_widget.setItem(
                    ridx, cidx, QTableWidgetItem(str(value))
                )

    def add_row(self, row: int, col: int):
        if row == self.data_widget.rowCount() - 1 and self.data_widget.item(row, col).text() != '':
            new_row = [
                np.array([0]).astype(self.data[column_series].dtype)[0]
                for column_series in self.data
            ]
            self.data = pd.concat([
                self.data,
                pd.DataFrame(
                    [new_row], 
                    columns=self.data.columns, 
                    index=[len(self.data.index)]
                )
            ])
            self.update_row()

    def add_col(self):
        new_col = np.array(
            [0 for _ in range(self.data.shape[0])], dtype='object')
        self.data = pd.concat(
            [
                self.data,
                pd.DataFrame(
                    new_col,
                    columns=[len(self.data.columns)],
                    index=self.data.index
                )
            ],
            axis=1
        )
        self.update_col()

    def change_value(self, row: int, col: int):
        if row < self.data.shape[0]:
            old_val = str(self.data.iat[row, col])
            new_val = self.data_widget.item(row, col).text()

            if old_val != new_val:
                try:
                    if new_val != '':
                        self.data.iat[row, col] = literal_eval(new_val)
                    else:
                        self.data.iat[row, col] = ''
                except ValueError:
                    self.data.iat[row, col] = self.data_widget.item(row, col).text()