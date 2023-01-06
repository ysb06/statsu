import logging
from typing import Optional

import numpy as np
import pandas as pd
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QWidget

from statsu.data.data_model import PandasModel
from statsu.ui.design.data_container import Ui_DataContainer
from statsu.ui.user_command import UserCommandManager

logger = logging.getLogger(__name__)

class DataContainer(QWidget, Ui_DataContainer):
    def __init__(
            self, 
            data: pd.DataFrame = None, 
            name: str = 'Sheet',
            data_path: Optional[str] = None,
            parent: Optional[QWidget] = None
        ) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.command_manager: UserCommandManager = None

        if data is None:
            data = pd.DataFrame([['']])
        self.raw_data = data
        self.name = name
        self.data_path = data_path

        self.model = PandasModel(data, parent=self)
        self.data_view.setModel(self.model)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        return super().contextMenuEvent(event)

    def set_command_manager(self, manager: UserCommandManager):
        self.command_manager = manager
        self.model.command_manager = manager
