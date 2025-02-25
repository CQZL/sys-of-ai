# -*- coding: utf-8 -*-
# @Time : 2025/1/10 15:04
# @Author : Li Desheng
# @File : main.py
# @Project : Interfaces
import PySide6
import sys
from PySide6.QtWidgets import QApplication
from view.MainWidget import MainWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWidget()
    mainWin.show()
    sys.exit(app.exec())


