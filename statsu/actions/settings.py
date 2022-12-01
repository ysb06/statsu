import pandas as pd


class WindowSettings:
    def __init__(self) -> None:
        self.in_memory_target: pd.DataFrame = None