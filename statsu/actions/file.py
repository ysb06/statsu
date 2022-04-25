from statsu.actions import MenuActionGroup, MenuAction
from statsu.widgets.pgui_window import PguiWindow
import logging

logger = logging.getLogger(__name__)

class FileActionGroup(MenuActionGroup):
    def __init__(self, parent: PguiWindow) -> None:
        super().__init__('File')
        self.parent = parent

        self.action_list = [
            MenuAction('New Dataframe', parent, self.create_new_doc,'Ctrl+N'),
            MenuAction('Open File...', parent, parent.import_dialog,'Ctrl+O'),
            MenuAction('Switch Dataframe...', parent, self.open_navigator,'Ctrl+O'),
            MenuAction('Quit', parent, parent.close,'Ctrl+Q'),
        ]
    
    def create_new_doc(self):
        logger.info('New!!!')
        print(self.parent.get_dataframes())

    def open_navigator(self):
        self.parent.navigator.show()