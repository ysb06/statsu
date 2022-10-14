import logging

from scipy.stats import ttest_ind
from statsu.actions import MenuAction, MenuActionGroup
from statsu.widgets.analysis.general_bridge import RunFunctionDialog
from statsu.widgets.pgui_window import PguiWindow

logger = logging.getLogger(__name__)


class AnalysisActionGroup(MenuActionGroup):
    def __init__(self, parent: PguiWindow) -> None:
        super().__init__('Analysis')
        self.parent = parent

        self.action_list = [
            MenuAction('T-Test test', parent, self.ttest),
            MenuAction('Run General Function...', parent, self.run_general_function),
        ]

    def run_general_function(self):
        pass

    def ttest(self):
        dat_M = [117, 108, 105, 89, 101, 93, 96, 108, 108,
                 94, 93, 112, 92, 91, 100, 96, 120, 86, 96, 95]
        dat_F = [121, 101, 102, 114, 103, 105, 101, 131, 96,
                 109, 109, 113, 115, 94, 108, 96, 110, 112, 120, 100]
        dialogue = RunFunctionDialog(ttest_ind, self.parent, dat_M, dat_F)
        result = dialogue.run()
        print(result)
