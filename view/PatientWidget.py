# -*- coding: utf-8 -*-
# @Time : 2025/1/11 14:11
# @Author : Li Desheng
# @File : PatientWidget.py
# @Project : Interfaces
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os
from view.ImageWidget import ImageWidget

class PatientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.font = QFont("Arial", 12)
        self.data_dir = "data"  # 数据目录
        self.init_windows()
        self.init_control()

    def init_windows(self):
        self.setWindowTitle("Medical Info System")
        self.setGeometry(0, 0, 800, 600)


    def init_control(self):
        # 总布局
        self.totallayout = QHBoxLayout()
        self.setLayout(self.totallayout)

        # 左侧布局 - 堆栈与按钮列表
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignTop)  # 确保按钮向上对齐

        # 动态创建按钮，每个按钮对应一个子文件夹
        if os.path.exists(self.data_dir) and os.path.isdir(self.data_dir):
            for folder in sorted(os.listdir(self.data_dir)): # folder是文件名
                folder_path = os.path.join(self.data_dir, folder)
                if os.path.isdir(folder_path):
                    button = QPushButton(folder, self)
                    button.setFixedHeight(35)  # 设置固定高度
                    button.clicked.connect(lambda *args, f=folder: self.on_folder_button_clicked(f))

                    self.left_layout.addWidget(button)
        else:
            print("文件地址不存在")

        # 右侧布局 - 图片展示区
        self.right_widget = QWidget()
        self.right_layout = QGridLayout()  # 使用网格布局
        self.right_layout.setSpacing(0)  # 移除网格间距
        self.right_widget.setLayout(self.right_layout)

        # 添加到总布局
        self.totallayout.addLayout(self.left_layout, 1)
        self.totallayout.addWidget(self.right_widget, 5)

    def on_folder_button_clicked(self, folder_name):
        # 读取文件底下的图片
        folder_path = os.path.join(self.data_dir, folder_name)
        self.display_images(folder_path)

    def display_images(self, folder_path):

        # 清除当前显示的所有图片和标签
        while self.right_layout.count():
            item = self.right_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # 显示新的图片
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            images = [img for img in sorted(os.listdir(folder_path)) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
            for idx, img_name in enumerate(images):
                img_path = os.path.join(folder_path, img_name)

                # 创建包含图片和标题的小部件
                image_widget = ImageWidget(img_path, img_name)

                # 使用网格布局添加控件
                row = idx // 3  # 每行放3个元素
                col = idx % 3
                self.right_layout.addWidget(image_widget, row * 2, col)  # 图片放在偶数行

                # 如果不是第一行，则在前一行下方添加一个高度为5的spacer
                if row > 0:
                    self.right_layout.addItem(QSpacerItem(0, 3, QSizePolicy.Minimum, QSizePolicy.Fixed), row * 2 - 1, 0,
                                              1, -1)

            # 添加一个伸缩因子，将所有内容顶到网格布局的顶部
            self.right_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding),
                                      (len(images) * 2 // 3) + 1, 0)

            # 如果没有图片或只有一行图片，也需要在底部添加间隔
            if len(images) == 0 or len(images) <= 3:
                self.right_layout.addItem(QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed), 1, 0, 1, -1)

    def image_clicked(self, path):
        # 当图片被点击时输出路径
        print(f"图片 {path}被点击")


