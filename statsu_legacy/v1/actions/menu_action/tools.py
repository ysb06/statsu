import logging
from statsu_legacy.actions.menu_action import MenuAction

logger = logging.getLogger(__name__)


class ToolsAction(MenuAction):
    def run_script(self):
        data = self.main_window.get_current_datasheet().data
        print(data)
