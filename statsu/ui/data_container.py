from typing import Optional
import logging

import pandas as pd
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QContextMenuEvent

from statsu.data.data_model import PandasModel
from statsu.ui.design.data_container import Ui_DataContainer

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

        if data is None:
            data = pd.DataFrame([['']])
        self.raw_data = data
        self.name = name
        self.data_path = data_path

        self.model = PandasModel(data, self)
        self.data_view.setModel(self.model)
        
    def setupUi(self, DataContainer):
        super().setupUi(DataContainer)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        return super().contextMenuEvent(event)
