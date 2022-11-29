import statsu.ui.main_window


class ActionBase:
    def __init__(self, window: statsu.ui.main_window.MainWindow) -> None:
        self.main_window = window