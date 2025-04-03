
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ResultWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.font = QFont("Arial", 12)
        self.init_windows()
        self.init_control()  # 初始化控件，创建并布置窗口中的各个控件

    def init_windows(self):
        """初始化窗口属性"""
        pass

    def init_control(self):
        pass
