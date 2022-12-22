import logging
import sys
from typing import List

import pandas as pd
from PySide6.QtWidgets import QApplication

from statsu.actions.action_file import ActionFile
from statsu.ui.data_container import DataContainer
from statsu.ui.main_window import MainWindow

from dataclasses import dataclass

logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
app = QApplication(sys.argv)

@dataclass
class DataObject:
    data_frame_origin: pd.DataFrame
    name: str = 'Data'

    def __post_init__(self):
        self.data_frame = self.data_frame_origin.copy()


@dataclass
class WindowSettings:
    in_memory_target: List[DataObject]


class WindowUnit:

    def __init__(self, in_memory_data: List[DataObject] = None) -> None:
        self.main_window = MainWindow()
        self.settings = WindowSettings(in_memory_data)

        if self.settings.in_memory_target is not None:
            for data_obj in in_memory_data:
                data_container = DataContainer(
                    data=data_obj.data_frame,
                    name=data_obj.name + ' (In Memory)',
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


def show(input_data: pd.DataFrame = None, name: str = None) -> pd.DataFrame:
    """
    프로그램을 잠시 멈추고 입력된 데이터를 보여준다.
    """
    if input_data is not None:
        window = WindowUnit(
            in_memory_data=[DataObject(input_data, name=name if name is not None else 'Data')]
        )
    else:
        window = WindowUnit()

    window.show()
    app.exec()

    return window.settings.in_memory_target[0].data_frame

def show_bundle(input_data: List[DataObject]):
    window = WindowUnit(input_data)
    window.show()
    app.exec()
        
