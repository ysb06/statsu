from typing import Union
import logging

from PyQt5 import uic
from PyQt5.QtWidgets import QAction, QMainWindow, QTabWidget, QTextEdit, QMenu, QGroupBox
from statsu_legacy.widgets.analysis.general_bridge import GeneralBridge

from statsu_legacy.widgets.datasheet import DataSheetWidget
from statsu_legacy.statistics import FuncDef, FuncDefGroup, Function_List

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, uic.loadUiType('statsu/widgets/main_window.ui')[0]):  # type: ignore
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.datasheet_tab: QTabWidget = self.datasheet_tab
        self.terminal_text_box: QTextEdit = self.terminal_text_box
        self.status_bar = self.statusBar()

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
                    add_func_to_menu(new_menu, item)  # type: ignore
                elif type(item) == FuncDef:
                    menu.addAction(AnalysisAction(item, self))  # type: ignore

        add_func_to_menu(self.analysis_menu, Function_List)


class AnalysisAction(QAction):
    def __init__(self, core: FuncDef, parent: MainWindow) -> None:
        super().__init__(core.name, parent)
        self.core = core
        self.triggered.connect(self.run)

    def run(self):
        dialogue = GeneralBridge(self.core.func, self.parent())
        dialogue.setWindowTitle(self.core.name)
        res = dialogue.exec()
        for e in dialogue.elements:
            print(f'{e.name}:= {e.get_value()}')
        print(f'Run analysis {self.core.name} -> {res}')
        # 특별히 정해진 인터페이스가 없는 경우 general bridge dialogue 호출
