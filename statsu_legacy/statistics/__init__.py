from typing import Any, Union, Callable, List
from typing_extensions import Self

import pandas as pd
import scipy.stats


class FuncDef:
    def __init__(self, name: str, func: Union[Callable, str]) -> None:
        self.name = name
        self.func = func

    def call_pandas_type_func(self, data: pd.DataFrame):
        return getattr(data, self.func)


class FuncDefGroup:
    def __init__(self, name: str, func_list: List[Union[Self, FuncDef]]) -> None:
        self.name = name
        self.func_list = func_list


Function_List = FuncDefGroup('Analysis', [
    FuncDefGroup('Descriptive Analysis', [
            FuncDef('Pandas Description', 'describe'),
            FuncDef('Scipy.stats Description', scipy.stats.describe)
        ]
    ),
    FuncDef('Scipy.stats Description', scipy.stats.describe)
])
