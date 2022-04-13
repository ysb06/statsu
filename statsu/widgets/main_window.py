import logging
from typing import Union

from PyQt5 import uic
from PyQt5.QtWidgets import QAction, QMainWindow, QTabWidget, QTextEdit, QMenu

from statsu.widgets.datasheet import DataSheetWidget
from statsu.statistics import FuncDef, FuncDefGroup, Function_List

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
        self.action_tools_run_scripts: QAction = self.action_tools_run_scripts

        self.action_analysis_frequency_analysis: QAction = self.action_analysis_frequency_analysis

        self.init_ui()

    def get_current_datasheet(self) -> DataSheetWidget:
        return self.datasheet_tab.currentWidget()

    def init_ui(self) -> None:
        self.datasheet_tab.clear()

        def add_func_to_menu(menu: QMenu, group: FuncDefGroup):
            func_list = group.func_list
            for item in func_list:
                if type(item) == FuncDefGroup:
                    new_menu = menu.addMenu(item.name)
                    add_func_to_menu(new_menu, item)
                elif type(item) == FuncDef:
                    menu.addAction(AnalysisAction(item, self))

        add_func_to_menu(self.analysis_menu, Function_List)


class AnalysisAction(QAction):
    def __init__(self, core: FuncDef, parent: MainWindow) -> None:
        super().__init__(core.name, parent)
        self.core = core
        self.triggered.connect(self.run)

    def run(self):
        print(f'Run analysis {self.core.name}')
        # 특별히 정해진 인터페이스가 없는 경우 general bridge dialogue 호출
