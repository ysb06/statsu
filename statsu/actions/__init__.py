from statsu.actions.menu_action.analysis import AnalysisAction
from statsu.actions.menu_action.file import FileAction
from statsu.actions.menu_action.tools import ToolsAction
from statsu.widgets.main_window import MainWindow


class MenuActionGroup:
    def __init__(self, main_window: MainWindow) -> None:
        self.file = FileAction(main_window)
        self.tools = ToolsAction(main_window)
        self.analysis = AnalysisAction(main_window)


