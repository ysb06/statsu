import inspect
import logging

from statsu.widgets.pgui_window import PguiWindow


logging.basicConfig(
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def show():
    window = PguiWindow()
    window.caller_stack = inspect.currentframe().f_back
