import logging
import os.path
import sys
from enum import Enum

import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
                             QTabWidget)

from widgets.datasheet import DataSheetWidget

logging.basicConfig(
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class DataType(Enum):
    Unknown = 0
    Integer = 1
    Float = 2
    String = 3


class MainWindow(QMainWindow, uic.loadUiType('src/window.ui')[0]):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.datasheet_tab: QTabWidget = self.datasheet_tab

        self.action_file_new: QAction = self.action_file_new
        self.action_file_save: QAction = self.action_file_save
        self.action_file_save_as: QAction = self.action_file_save_as
        self.action_file_load: QAction = self.action_file_load

        self.init_ui()
        self.init_events()

    def init_ui(self) -> None:
        self.datasheet_tab.clear()
        self.onCreateNewDoc()

    def init_events(self) -> None:
        self.action_file_new.triggered.connect(self.onCreateNewDoc)
        self.action_file_save.triggered.connect(self.onSaveDoc)
        self.action_file_load.triggered.connect(self.onLoadDoc)

    def onCreateNewDoc(self) -> None:
        new_doc = DataSheetWidget()
        self.datasheet_tab.addTab(
            new_doc, 
            f'doc {self.datasheet_tab.count() + 1}'
        )
        self.datasheet_tab.setCurrentWidget(new_doc)

    def onSaveDoc(self) -> None:
        data: pd.DataFrame = self.datasheet_tab.currentWidget().data
        data.to_excel('./temp.xlsx')
        logger.info(f'File saved...')
    
    def onSaveAsDoc(self) -> None:
        pass

    def onLoadDoc(self) -> None:
        target_path = QFileDialog.getOpenFileName(
            self, '데이터 열기', 
            filter='Excel Files (*.xlsx *.xls);;CSV files (*.csv);;Text files (*.txt)'
        )
        target_dir_path, target_filename = os.path.split(target_path[0])
        name, ext = os.path.splitext(target_filename)
        if ext == '.xlsx' or ext == '.xls':
            temp = pd.ExcelFile(target_path[0])
            df = temp.parse(header=0, index_col=0)

            new_doc = DataSheetWidget(df)
            self.datasheet_tab.addTab(new_doc, new_doc.name)
            self.datasheet_tab.setCurrentWidget(new_doc)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_ui = MainWindow()
    main_ui.show()
    app.exec_()
