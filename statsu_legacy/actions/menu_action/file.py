import logging
import os

import pandas as pd
from PyQt5.QtWidgets import QFileDialog
from statsu_legacy.actions.menu_action import MenuAction
from statsu_legacy.widgets.datasheet import DataSheetWidget

logger = logging.getLogger(__name__)


class FileAction(MenuAction):
    def create_new_doc(self) -> None:
        new_doc = DataSheetWidget()
        self.main_window.datasheet_tab.addTab(
            new_doc,
            f'doc {self.main_window.datasheet_tab.count() + 1}'
        )
        self.main_window.datasheet_tab.setCurrentWidget(new_doc)

    def save_doc(self) -> None:
        datasheet: DataSheetWidget = self.main_window.get_current_datasheet()

        if datasheet.path is not None:
            data: pd.DataFrame = datasheet.data
            data.to_excel(datasheet.path)
            logger.info(f'File saved...')
        else:
            self.save_doc_as()

    def save_doc_as(self) -> None:
        data: pd.DataFrame = self.main_window.get_current_datasheet().data

        target_path = QFileDialog.getSaveFileName(
            self.main_window, 'Save as',
            filter='Excel Files (*.xlsx *.xls)',
            directory=os.path.expanduser('~/')
        )

        if target_path[0] != '':
            data.to_excel(target_path[0])

    def load_doc(self) -> None:
        target_path = QFileDialog.getOpenFileName(
            self.main_window, 'Open File',
            filter='Excel Files (*.xlsx *.xls);;CSV files (*.csv);;Text files (*.txt)',
            initialFilter='CSV files (*.csv)',
            directory=os.path.expanduser('~/')
        )
        target_dir_path, target_filename = os.path.split(target_path[0])
        file_name, ext = os.path.splitext(target_filename)

        name = 'sheet'
        if ext == '.xlsx' or ext == '.xls':
            temp = pd.ExcelFile(target_path[0])
            df: pd.DataFrame = temp.parse(header=0, index_col=0)
            name = temp.sheet_names[0]
        elif ext == '.csv':
            # Header 선택 옵션
            df: pd.DataFrame = pd.read_csv(target_path[0], header=0)
            name = file_name

        new_doc = DataSheetWidget(initial_data=df, name=name, path=target_path)
        self.main_window.datasheet_tab.addTab(new_doc, new_doc.name)
        self.main_window.datasheet_tab.setCurrentWidget(new_doc)

    def quit_program(self):
        self.main_window.close()
