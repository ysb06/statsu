import logging

from PyQt5 import uic
from PyQt5.QtWidgets import QAction, QMainWindow, QTabWidget, QTextEdit

from statsu.window_module import TerminalManager

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, uic.loadUiType('statsu/widgets/main_window.ui')[0]):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.datasheet_tab: QTabWidget = self.datasheet_tab
        self.terminal_text_box: QTextEdit = self.terminal_text_box
        self.status_bar = self.statusBar()

        self.action_file_quit: QAction = self.action_file_quit
        self.action_file_new: QAction = self.action_file_new
        self.action_file_save: QAction = self.action_file_save
        self.action_file_save_as: QAction = self.action_file_save_as
        self.action_file_load: QAction = self.action_file_load
        self.action_analysis_frequencyanalysis: QAction = self.action_analysis_frequencyanalysis
        
        self.init_ui()

    def init_ui(self) -> None:
        self.datasheet_tab.clear()
