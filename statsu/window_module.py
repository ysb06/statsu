import logging

from PyQt5.QtWidgets import QTextEdit, QStatusBar

logger = logging.getLogger(__name__)


class TerminalManager:
    def __init__(self, terminal_text_edit: QTextEdit, status_bar) -> None:
        self.terminal_ui: QTextEdit = terminal_text_edit
        self.status_ui: QStatusBar = status_bar

    def print(self, text) -> None:
        self.terminal_ui.append(text)
        self.status_ui.showMessage(text)
