# -*- coding: utf-8 -*-
# @Time : 2025/1/11 14:02
# @Author : Li Desheng
# @File : SortWidget.py
# @Project : Interfaces
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class SortWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.font = QFont("Arial", 12)
        self.init_windows()  # 初始化窗口，设置窗口的基本属性和布局
        self.init_control()  # 初始化控件，创建并布置窗口中的各个控件

    def init_windows(self):
        """初始化窗口属性"""
        self.setWindowTitle("Medical Info System")
        self.setGeometry(300, 100, 800, 600)

    def init_control(self):
        pass

