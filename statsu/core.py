import logging
import sys

import pandas as pd
from PySide6.QtWidgets import QApplication

from statsu.actions.action_file import ActionFile
from statsu.ui.data_container import DataContainer
from statsu.ui.main_window import MainWindow

logging.basicConfig(
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
app = QApplication(sys.argv)


class WindowUnit:
    def __init__(self) -> None:
        self.main_window = MainWindow()

        self.action_file = ActionFile(self.main_window)
        self.main_window.action_file_new.triggered.connect(
            self.action_file.create_new_sheet
        )
        self.main_window.action_file_open.triggered.connect(
            self.action_file.create_sheet_from_file
        )
        self.main_window.action_file_close.triggered.connect(
            self.action_file.close_window
        )

    def create_sheet_from_data(self, data: pd.DataFrame, name: str):
        data_container = DataContainer(data)
        data_container.name = name
        self.main_window.add_sheet(data_container)

    def show(self) -> None:
        self.main_window.show()


def show(data: pd.DataFrame = None, name: str = 'Data') -> MainWindow:
    window = WindowUnit()

    if data is not None:
        window.create_sheet_from_data(data, name=name)

    window.show()
    app.exec()
