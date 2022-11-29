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

        self._action_file = ActionFile(self.main_window)
        self.main_window.action_file_new.triggered.connect(
            self._action_file.create_new_sheet
        )
        self.main_window.action_file_open.triggered.connect(
            self._action_file.create_sheet_from_file
        )
        self.main_window.action_file_close.triggered.connect(
            self._action_file.close_window
        )

    def create_sheet_from_data(self, data: pd.DataFrame, name: str):
        data_container = DataContainer(data)
        data_container.name = name
        self.main_window.add_sheet(data_container)

    def show(self) -> None:
        self.main_window.show()

    def update(self) -> None:
        self.main_window.update()


def show(
        input_data: pd.DataFrame = None, 
        input_data_title: str = 'Internal Data', 
        force_output: bool = False
    ) -> pd.DataFrame:
    """
    프로그램을 잠시 멈추고 입력된 데이터를 보여준다.
    """
    window = WindowUnit()
    if input_data is not None:
        window.create_sheet_from_data(input_data, input_data_title)

    window.show()
    app.exec()

    if window.main_window.get_data_container_count() > 1 and force_output:
        output = input_data
        logger.warn('Cannot specify output data')
        # 여기에 Output을 사용자가 고르는 부분이 들어가야 함
        return output

    if input_data is None:
        return window.main_window.get_current_data_container().raw_data
    else:
        return input_data
