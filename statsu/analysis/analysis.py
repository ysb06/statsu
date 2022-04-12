from window_module import TerminalManager


class Analysis:
    def __init__(self, terminal_manager: TerminalManager) -> None:
        self.terminal_manager = terminal_manager

        self.terminal_manager.print('Analysis module initialized')