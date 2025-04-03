# view/main.py
import sys

from PySide6.QtCore import QEvent
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QStackedWidget, QVBoxLayout, QWidget  # 添加QDialog导入
from LoginDialog import LoginDialog
from MainWidget import MainWidget
from QueueWork import QueueWork


class QueueAndMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 创建堆叠窗口部件
        self.stacked_widget = QStackedWidget()

        # 创建任务界面和详情界面实例
        self.main_interface = MainWidget()
        self.queue_interface = QueueWork()

        # 将任务界面和详情界面添加到堆叠窗口部件中
        self.stacked_widget.addWidget(self.queue_interface)
        self.stacked_widget.addWidget(self.main_interface)

        # 连接任务界面按钮的点击信号到切换界面的槽函数
        self.main_interface.show_queue_btn.clicked.connect(self.show_queue_interface)
        self.queue_interface.queue_widget.show_work_btn.clicked.connect(self.show_main_interface)

        # 设置主窗口布局
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        self.window_style()

    def window_style(self):
        self.setWindowTitle("宫颈癌细胞病理学AI辅助诊断系统")
        self.setStyleSheet("""
            QComboBox { 
                border: 2px solid white; 
            }
            QComboBox:hover { 
                border-color: lightgray; 
            }
        """)

    def show_queue_interface(self):
        # 切换到队列界面
        self.stacked_widget.setCurrentIndex(0)

    def show_main_interface(self):
        # 切换到主界面
        self.stacked_widget.setCurrentIndex(1)

    def showEvent(self, event: QEvent):
        # 获取屏幕的尺寸
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = self.geometry()

        # 计算窗口居中时的位置
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # 将窗口移动到居中位置
        self.move(x, y)
        super().showEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.Accepted:
        window = QueueAndMainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


