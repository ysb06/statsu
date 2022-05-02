import logging

from pandas import DataFrame
from PyQt5.QtWidgets import QFileDialog
from statsu.actions import MenuAction, MenuActionGroup
from statsu.widgets.pgui_window import PguiWindow
from os.path import basename

logger = logging.getLogger(__name__)

class FileActionGroup(MenuActionGroup):
    def __init__(self, parent: PguiWindow) -> None:
        super().__init__('File')
        self.parent = parent

        self.action_list = [
            MenuAction('New Dataframe', parent, self.create_new_doc,'Ctrl+N'),
            MenuAction('Open File...', parent, parent.import_dialog,'Ctrl+O'),
            MenuAction('Switch Dataframe...', parent, self.open_navigator,'Ctrl+O'),
            MenuAction('Save As...', parent, self.save_dialog,'Ctrl+S'),
            MenuAction('Quit', parent, parent.close,'Ctrl+Q'),
        ]
    
    def create_new_doc(self):
        self.parent.store.add_dataframe(DataFrame({'0': [0, 0], '1': [0, 0]}))

    def open_navigator(self):
        self.parent.navigator.show()
    
    def save_dialog(self):
        dialog = QFileDialog(parent=self.parent)
        pgdf = self.parent.store.selected_pgdf
        path, _ = dialog.getSaveFileName(directory=pgdf.name, filter='Excel Files (*.xlsx);;CSV files (*.csv)')

        if path == False:
            return
        elif path.endswith('.xlsx'):
            pgdf.df.to_excel(path)
        elif path.endswith('csv'):
            pgdf.df.to_csv(path, index=False)
        
        pgdf.name = basename(path)
