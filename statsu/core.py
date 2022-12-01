import logging
import sys

import pandas as pd
from PySide6.QtWidgets import QApplication

from statsu.actions.action_file import ActionFile
from statsu.actions.settings import WindowSettings
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
    def __init__(self, data: pd.DataFrame = None) -> None:
        self.main_window = MainWindow()
        self.settings = WindowSettings()

        self.settings.in_memory_target = data
        if self.settings.in_memory_target is not None:
            data_container = DataContainer(
                data=self.settings.in_memory_target.copy(),
                name='Internal Data',
                data_path='_Internal'
            )
            self.main_window.add_sheet(data_container)

        self._action_file = ActionFile(self.main_window, self.settings)
        self.main_window.action_file_new.triggered.connect(self._action_file.create_new_sheet)
        self.main_window.action_file_open.triggered.connect(self._action_file.create_sheet_from_file)
        self.main_window.action_file_close.triggered.connect(self._action_file.close_window)
        self.main_window.action_file_save.triggered.connect(self._action_file.save_sheet)
        self.main_window.action_file_save_as.triggered.connect(self._action_file.save_sheet_as)

    def show(self) -> None:
        self.main_window.show()

    def update(self) -> None:
        self.main_window.update()


def show(
    input_data: pd.DataFrame = None,
    read_only: bool = True
) -> pd.DataFrame:
    """
    프로그램을 잠시 멈추고 입력된 데이터를 보여준다.
    """
    window = WindowUnit(input_data)
    window.show()
    app.exec()

    if read_only:
        return input_data
    else:
        # Pandas deep-shallow copy에대해 이해가 필요
        return window.settings.in_memory_target.copy()
