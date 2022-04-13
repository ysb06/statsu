from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

class GeneralBridge(QDialog, uic.loadUiType('statsu/widgets/general_bridge.ui')[0]):
    pass