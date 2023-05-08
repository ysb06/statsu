from collections import deque
from typing import Deque
import logging

from PySide6.QtWidgets import QMainWindow

from statsu.ui.data_container import DataContainer
from statsu.ui.design.main_window import Ui_MainWindow
from statsu.ui.user_command import UserCommandManager

DISPLAY_MAX_LENGTH = 16384

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.command_manager: UserCommandManager = UserCommandManager()
        self.main_data_tab_widget.currentChanged.connect(self.sheet_changed)

    def sheet_changed(self, idx: int):
        container: DataContainer = self.main_data_tab_widget.currentWidget()
        logger.info(f'Sheet Changed to {idx} [{container.raw_data.shape}]')
        if container.raw_data.shape[0] <= DISPLAY_MAX_LENGTH:
            self.container_controller.setVisible(False)
        else:
            self.container_controller.setVisible(True)


    def add_sheet(self, sheet: DataContainer):
        sheet.set_command_manager(self.command_manager)
        idx = self.main_data_tab_widget.addTab(sheet, sheet.name)
        self.main_data_tab_widget.setCurrentIndex(idx)

    def get_current_data_container(self) -> DataContainer:
        return self.main_data_tab_widget.currentWidget()