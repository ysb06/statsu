import logging

import statsu_legacy.statistics.descriptive_statistics as d_stat
from statsu_legacy.actions.menu_action import MenuAction

logger = logging.getLogger(__name__)

class AnalysisAction(MenuAction):
    def do_frequency_analysis(self):
        result = d_stat.descriptive_analysis(self.main_window.get_current_datasheet().data)
        self.main_window.terminal_text_box.append(f"{str(result)}\r\n{'-'*10}")

        logger.info('Frequency Analysis')
        
