from typing import Dict
from pandasgui.gui import PandasGui
from PyQt5.QtGui import QCloseEvent


class PguiWindow(PandasGui):
    def __init__(self, settings: dict = {}, **kwargs):
        super().__init__(settings, **kwargs)

    def init_ui(self):
        super().init_ui()

        self.setCentralWidget(self.stacked_widget)

        self.navigator.setParent(None)
        self.navigator.setWindowTitle('Dataframe Navigator')

    def make_menu_bar(self):
        from statsu.actions import StatsuMenuBar

        self.setMenuBar(StatsuMenuBar(self))

    def closeEvent(self, e: QCloseEvent) -> None:
        self.navigator.close()
        super().closeEvent(e)
