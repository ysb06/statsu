from typing import Optional
import logging

import pandas as pd
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QContextMenuEvent

from data.data_model import PandasModel
from ui.design.data_container import Ui_DataContainer

logger = logging.getLogger(__name__)

class DataContainer(QWidget, Ui_DataContainer):
    def __init__(
            self, 
            data: pd.DataFrame = None, 
            name: str = 'Sheet', 
            parent: Optional[QWidget] = None
        ) -> None:
        super().__init__(parent)
        self.setupUi(self)

        if data is None:
            data = pd.DataFrame([['']])
        self.raw_data = data
        self.name = name

        model = PandasModel(data, self)
        self.data_view.setModel(model)
    def setupUi(self, DataContainer):
        super().setupUi(DataContainer)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        print(self.data_view.selectedIndexes())
        return super().contextMenuEvent(event)
