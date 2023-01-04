import logging
from typing import List

from statsu.actions.action_base import ActionBase
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QModelIndex
import pandas as pd
import math

logger = logging.getLogger(__name__)

class ActionEdit(ActionBase):
    def cut_data(self):
        selections = self.main_window.get_current_data_container().data_view.selectedIndexes()
        result_text = ''
        QApplication.clipboard().setText(result_text)

        self.copy_data(selections=selections)

        container = self.main_window.get_current_data_container()
        for selection in selections:
            container.raw_data.iloc[selection.row(), selection.column()] = ''
        
        container.data_view.model().layoutChanged.emit()

    def copy_data(self, *args, selections = None):
        if selections is None:
            selections = self.main_window.get_current_data_container().data_view.selectedIndexes()

        min_y = math.inf
        max_y = -1
        min_x = math.inf
        max_x = -1
        for selection in selections:
            max_y = max(max_y, selection.row())
            min_y = min(min_y, selection.row())
            max_x = max(max_x, selection.column())
            min_x = min(min_x, selection.column())

        result: List[List] = [
            ['' for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)
        ]

        for selection in selections:
            result[selection.row() - min_y][selection.column() - min_x] = selection.data(Qt.DisplayRole)

        result_text = '\r\n'.join(['\t'.join(item) for item in result])
        QApplication.clipboard().setText(result_text)

    def paste_data(self):
        container = self.main_window.get_current_data_container()
        selections = container.data_view.selectedIndexes()
        if len(selections) <= 0:
            return
        
        min_y = math.inf
        max_y = -1
        min_x = math.inf
        max_x = -1
        for selection in selections:
            max_y = max(max_y, selection.row())
            min_y = min(min_y, selection.row())
            max_x = max(max_x, selection.column())
            min_x = min(min_x, selection.column())

        data_text = QApplication.clipboard().text()
        data = [row.split('\t') for row in data_text.split('\r\n')]

        origin = container.raw_data.iloc[min_y:min_y + len(data), min_x:min_x + len(data[0])]

        for idx, (_, row) in enumerate(origin.iterrows()):
            for n in range(len(data[idx])):
                if data[idx][n] == '':
                    data[idx][n] = row.iloc[n]

        container.raw_data.iloc[min_y:min_y + len(data), min_x:min_x + len(data[0])] = data
        container.data_view.model().layoutChanged.emit()