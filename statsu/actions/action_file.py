import logging
from typing import Tuple

import pandas as pd
from PySide6.QtWidgets import QFileDialog

import statsu.data.file_loader as file_loader
from statsu.actions.action_base import ActionBase
from statsu.ui.data_container import DataContainer

logger = logging.getLogger(__name__)


class ActionFile(ActionBase):
    def create_new_sheet(self):
        sheet_name = f'Sheet {self.main_window.main_data_tab_widget.count()}'
        sheet = DataContainer(name=sheet_name)
        self.main_window.add_sheet(sheet)

    def create_sheet_from_file(self):
        file_path: Tuple[str, str] = QFileDialog.getOpenFileName(
            self.main_window, 'Import file', './'
        )
        if file_path[0] != '':
            raw: pd.DataFrame = file_loader.load_dataframe_from_file(
                file_path[0]
            )
            if raw is not None:
                container = DataContainer(data=raw)
                self.main_window.add_sheet(container)

    def close_window(self):
        self.main_window.close()
