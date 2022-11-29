import logging
from typing import Optional, Union

import pandas as pd
from PySide6.QtCore import (QAbstractTableModel, QModelIndex, QObject,
                            QPersistentModelIndex, Qt)

logger = logging.getLogger(__name__)


class PandasModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.raw_data = data

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = None) -> int:
        return self.raw_data.shape[0]

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = None) -> int:
        return self.raw_data.shape[1]

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.raw_data.iloc[index.row()][index.column()])

        return None

    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags:
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.raw_data.columns[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.raw_data.columns[section]
            except:
                pass
        return super().headerData(section, orientation, role)

    def setData(self, index: Union[QModelIndex, QPersistentModelIndex], value, role: int = Qt.EditRole) -> bool:
        if role == Qt.EditRole:
            self.raw_data.iat[index.row(), index.column()] = value
            return True
        else:
            return False
