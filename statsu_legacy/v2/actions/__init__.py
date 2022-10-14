from typing import Callable, List, Union

from PyQt5.QtWidgets import QAction, QMenu, QMenuBar
from statsu.widgets.pgui_window import PguiWindow
from typing_extensions import Self


class MenuAction(QAction):
    def __init__(self, text: str, parent: PguiWindow, func: Callable, shortcut: str = None) -> None:
        super().__init__(text, parent)
        self.triggered.connect(func)

        if shortcut is not None:
            self.setShortcut(shortcut)


class MenuActionGroup:
    def __init__(self, name: str) -> None:
        self.name = name
        self.action_list: List[Union[Self, MenuAction]] = []

    def bind_menu(self, menu: Union[QMenuBar, QMenu]) -> None:
        for item in self.action_list:
            if type(item) == MenuAction:
                menu.addAction(item)
            else:
                new_menu = menu.addMenu(item.name)
                item.bind_menu(new_menu)


class StatsuMenuBar(QMenuBar):
    def __init__(self, parent: PguiWindow) -> None:
        super().__init__(parent)

        from statsu.actions.file import FileActionGroup
        from statsu.actions.analysis import AnalysisActionGroup

        self.menu_actions = MenuActionGroup('__root')
        self.menu_actions.action_list.append(
            FileActionGroup(parent)
        )
        self.menu_actions.action_list.append(
            AnalysisActionGroup(parent)
        )
        self.menu_actions.bind_menu(self)
