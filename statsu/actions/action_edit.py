import logging
import math
from typing import List

import pandas as pd
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QApplication, QMainWindow

from statsu.actions.action_base import ActionBase
from statsu.data.data_model import ChangeValuesCommand

logger = logging.getLogger(__name__)

class ActionEdit(ActionBase):
    def undo(self):
        self.main_window.command_manager.undo_command()
        self.main_window.refresh_data_layout()

    def redo(self):
        self.main_window.command_manager.redo_command()
        self.main_window.refresh_data_layout()

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
        min_x = math.inf
        for selection in selections:
            min_y = min(min_y, selection.row())
            min_x = min(min_x, selection.column())

        data_text = QApplication.clipboard().text()
        data = [row.split('\t') for row in data_text.split('\r\n')]

        origin = container.raw_data.iloc[min_y:min_y + len(data), min_x:min_x + len(data[0])]

        for idx, (_, row) in enumerate(origin.iterrows()):
            for n in range(len(data[idx])):
                if data[idx][n] == '':
                    data[idx][n] = row.iloc[n]

        # container.raw_data.iloc[min_y:min_y + len(data), min_x:min_x + len(data[0])] = data
        command = ChangeValuesCommand(
            container.raw_data,
            min_y, min_y + len(data),
            min_x, min_x + len(data[0]),
            data,
            desc='Paste values'
        )
        self.main_window.command_manager.execute_command(command)
        self.main_window.refresh_data_layout()