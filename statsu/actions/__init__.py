from typing import Dict

from PyQt5.QtWidgets import QAction
from statsu.actions.file import FileAction
from statsu.actions.tools import ToolsAction
from statsu.widgets.main_window import MainWindow


class MenuAction:
    def __init__(self, main_window: MainWindow) -> None:
        self.file = FileAction(main_window)
        # self.tools = ToolsAction()
