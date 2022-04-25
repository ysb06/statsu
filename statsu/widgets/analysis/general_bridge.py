import inspect
from ast import literal_eval
from typing import Any, Callable, List, Optional, Union

from PyQt5 import uic
from PyQt5.QtWidgets import (QCheckBox, QDialog, QFormLayout, QGroupBox,
                             QLineEdit, QWidget)


class RunFunctionDialog(QDialog, uic.loadUiType('statsu/widgets/analysis/run_function_dialog.ui')[0]):
    def __init__(self, target: Callable, parent: Optional[QWidget] = None, *args) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)

        self.param_option_group_box: QGroupBox = self.param_option_group_box
        self.param_value_group_box: QGroupBox = self.param_value_group_box
        self.elements: List[BridgeElement] = []
        self.target_func = target
        self.data_list = args

        spec = inspect.getfullargspec(target)
        params = spec.args[(len(spec.args) - len(spec.defaults)):]
        for arg, val in zip(params, spec.defaults):
            if type(val) == bool:
                elem = OptionBridgeElement(arg, 2 if val else 0, self.param_option_group_box)
            else:
                elem = StringBridgeElement(arg, val, self.param_value_group_box)
            self.elements.append(elem)

    def run(self) -> Any:
        action_result = self.exec()

        if action_result == 0:
            return None
        else:
            args = {}
            for element in self.elements:
                args[element.name] = element.value

            return self.target_func(*self.data_list, **args)


class BridgeElement(QWidget):
    def __init__(self, name: str, init_value: Union[bool, int, float, str, None] = None, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.name = name
        self.value: Union[bool, int, float, str, None] = init_value
        self.value_input: Optional[QWidget] = None

    def onChange(self, value: str):
        try:
            self.value = literal_eval(value)
        except ValueError:
            self.value = value

    def initialize(self):
        parent: QGroupBox = self.parent()
        parent_layout: QFormLayout = parent.layout()
        parent_layout.addRow(self.name, self.value_input)
    
    def get_value(self):
        return self.value


class StringBridgeElement(BridgeElement):
    def __init__(self, name: str, init_value, parent: Optional[QWidget] = None) -> None:
        super().__init__(name, init_value, parent)
        self.value_input = QLineEdit(parent)
        self.value_input.textChanged.connect(self.onChange)
        self.value_input.setText(str(self.value))

        self.initialize()


class OptionBridgeElement(BridgeElement):
    def __init__(self, name: str, init_value, parent: Optional[QWidget] = None) -> None:
        super().__init__(name, init_value, parent)
        self.value_input = QCheckBox(parent)
        self.value_input.stateChanged.connect(self.onChange)
        self.value_input.setCheckState(self.value)

        self.initialize()
    
    def get_value(self):
        return False if self.value == 0 else True
