import logging
import sys

from PyQt5.QtWidgets import QApplication

from statsu_legacy.actions import MenuActionGroup
from statsu_legacy.widgets.main_window import MainWindow

logging.basicConfig(
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class AppController:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.menu_actions = MenuActionGroup(self.window)

        self.window.action_file_new.triggered.connect(
            self.menu_actions.file.create_new_doc
        )
        self.window.action_file_load.triggered.connect(
            self.menu_actions.file.load_doc
        )
        self.window.action_file_save.triggered.connect(
            self.menu_actions.file.save_doc
        )
        self.window.action_file_save_as.triggered.connect(
            self.menu_actions.file.save_doc_as
        )
        self.window.action_file_quit.triggered.connect(
            self.menu_actions.file.quit_program
        )

        self.window.action_tools_run_scripts.triggered.connect(
            self.menu_actions.tools.run_script
        )

        self.window.action_analysis_frequency_analysis.triggered.connect(
            self.menu_actions.analysis.do_frequency_analysis
        )

    def activate(self) -> None:
        logger.info('Activate')
        self.window.show()
        self.app.exec_()


def show():
    app = AppController()
    app.menu_actions.file.create_new_doc()
    app.activate()
