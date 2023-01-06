import logging
from typing import Any, Optional, Union

import numpy as np
import pandas as pd
from PySide6.QtCore import (QAbstractTableModel, QModelIndex, QObject,
                            QPersistentModelIndex, Qt)

from statsu.ui.user_command import UserCommand, UserCommandManager

logger = logging.getLogger(__name__)


class PandasModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.raw_data = data
        self.command_manager: UserCommandManager = None

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = None) -> int:
        return self.raw_data.shape[0]

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = None) -> int:
        return self.raw_data.shape[1]

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.raw_data.iloc[index.row()].iloc[index.column()])

        return None

    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags:
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Orientation.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.raw_data.rename({self.raw_data.columns[section]:data}, inplace=True)
                return True
            except Exception as e:
                logger.warn(f'Change Header Failed -> {e}')
                return False
        elif orientation == Qt.Orientation.Vertical and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.raw_data.rename({self.raw_data.index[section]:data}, inplace=True)
                return True
            except Exception as e:
                logger.warn(f'Change Header Failed -> {e}')
                return False
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Header 표시 방법을 정의하는 함수. DataFrame의 columns는 가로 Header, index는 세로 Header에 표시
        """
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            try:
                return self.raw_data.columns[section]
            except Exception as e: logger.warn(f'Show Header Failed -> {e}')
        elif orientation == Qt.Orientation.Vertical and role == Qt.DisplayRole:
            try:
                return str(self.raw_data.index[section])
            except Exception as e: logger.warn(f'Show Header Failed -> {e}')

        return super().headerData(section, orientation, role)

    def setData(self, index: Union[QModelIndex, QPersistentModelIndex], value, role: int = Qt.EditRole) -> bool:
        """
        표에서 데이터 변경 시 DataFrame에도 반영한다.
        """
        if role == Qt.EditRole:
            self.command_manager.execute_command(ChangeValuesCommand(
                self.raw_data,
                index.row(), index.row() + 1,
                index.column(), index.column() + 1,
                value
            ))
            return True
        else:
            return False


class ChangeValuesCommand(UserCommand):
    def __init__(
            self, 
            raw: pd.DataFrame, 
            top, bottom,
            left, right,
            data: Any,
            desc: str = 'Value Changed'
        ) -> None:
        super().__init__(desc)
        self.raw = raw
        self.t_r = (top, bottom, left, right)
        self.new_data = data
        self.original_data = self.raw.iloc[self.t_r[0]:self.t_r[1], self.t_r[2]:self.t_r[3]].copy()
    
    def execute(self) -> None:
        self.raw.iloc[self.t_r[0]:self.t_r[1], self.t_r[2]:self.t_r[3]] = self.new_data
    
    def undo(self) -> None:
        self.raw.iloc[self.t_r[0]:self.t_r[1], self.t_r[2]:self.t_r[3]] = self.original_data