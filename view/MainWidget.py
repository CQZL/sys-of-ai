# -*- coding: utf-8 -*-
# @Time : 2025/1/10 14:35
# @Author : Li Desheng
# @File : mainWidget.py
# @Project : Interfaces
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from view.InfoWidget import InfoWidget
import tifffile
import numpy as np
class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.dragging = False  # 是否正在拖拽
        self.offset = QPoint(0, 0)  # 图片偏移量
        self.font = QFont("Arial", 12)
        self.InfoWin = InfoWidget()
        self.current_scale_factor = 1  # 当前缩放因子，默认为1（未缩放）
        self.center_statue = 1
        self.rotate_time = 0
        self.init_win()
        self.init_control()

    def init_win(self):
        self.setWindowTitle("宫颈癌病理界面1.0")
        self.setWindowIcon(QIcon("img/view.png"))
        self.setStyleSheet("""
            background-color: black;
            color: white;
        """)
        '''
        # 全屏
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        self.setGeometry(geometry)
        '''
    def init_control(self):
        # 总布局
        self.totallayout = QHBoxLayout()
        self.setLayout(self.totallayout)

        # 1.左侧图片层
        self.left_column = QVBoxLayout()

        # 1.1左上信息层
        self.left_column_top = QHBoxLayout()

        # 1.1.1添加返回按钮
        self.back_button = QPushButton("返回上一菜单")
        self.left_column_top.addWidget(self.back_button)
        self.back_button.setFlat(True)  #设置扁平化
        self.back_button.resize(200, 80) #设置大小
        self.back_button.clicked.connect(self.InfoWin.init_win)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #0000FF;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        '''
        # 空格
        blank = QLabel('\b', self)
        self.left_column_top.addWidget(blank)
        '''
        self.left_column_top.addStretch() # 添加一个伸缩条


        # 5个图片按钮
        icon_names = ["icon/cut.png", "icon/puzzle.png", "icon/rotation.png", "icon/picture.png", "icon/report.png"]
        for index, icon_name in enumerate(icon_names):
            button = QPushButton()
            button.setIcon(QIcon(icon_name))
            button.setIconSize(QSize(20, 20))  # 设置图标大小
            self.left_column_top.addWidget(button)
            button.clicked.connect(lambda: self.reset_center_status())
            button.clicked.connect(lambda *args, idx=index: self.on_icon_button_clicked(idx))

        # 分隔符
        separator = QLabel('|', self)
        self.left_column_top.addWidget(separator)

        # 文字按钮（2x, 4x, 10x, 20x, 40x）
        scales = [("2x", 2), ("4x", 4), ("10x", 10), ("20x", 20), ("40x", 40)]
        for scale_text, scale_factor in scales:
            button = QPushButton(scale_text)
            button.setFixedWidth(30)
            button.clicked.connect(lambda *args, f=1 / scale_factor: self.scale_image(f))
            self.left_column_top.addWidget(button)

        # 添加Fit按钮及其后的输入框
        self.fit_button = QPushButton("Fit")
        self.fit_button.setFixedWidth(30)
        self.left_column_top.addWidget(self.fit_button)
        self.scale_input = QLineEdit(self)
        self.scale_input.setMaximumWidth(50)  # 设置输入框最大宽度
        self.left_column_top.addWidget(self.scale_input)
        # 分隔符
        separator = QLabel('|', self)
        self.left_column_top.addWidget(separator)


        # 上一例和下一例按钮
        self.prev_button = QPushButton("上一例")
        self.next_button = QPushButton("下一例")
        self.left_column_top.addWidget(self.prev_button)
        self.left_column_top.addWidget(self.next_button)

        # 1.2左下图片层
        self.left_column_bottom = QHBoxLayout()

        # 放置图片层
        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(200, 200)
        self.left_column_bottom.addWidget(self.image_label)
        #设置图片层背景为深灰色
        self.image_label.setStyleSheet("background-color: #333333;")

        self.left_column.addLayout(self.left_column_top, 1)# 占1行
        self.left_column.addLayout(self.left_column_bottom, 9)#设置图片层占9行
        self.totallayout.addLayout(self.left_column, 1)#设置左侧占1行

        # 右侧标记层
        self.right_column = QVBoxLayout()
        self.right_column.addWidget(self.InfoWin)
        self.totallayout.addLayout(self.right_column, 1)

    def on_icon_button_clicked(self, index):
        # 根据按钮的索引来判断哪个按钮被点击
        if index == 0:
            print("cut")
        elif index == 1:
            print("puzzle")
        elif index == 2:
            self.rotate_image()
        elif index == 3:
            # 打开文件对话框以选择图片
            filename, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.xpm *.jpg *.tif)")
            #添加读取tif文件格式的图片
            try:
                self.image_data = tifffile.imread(filename)
                self.height, self.width, channel = self.image_data.shape
                bytesPerLine = 3 * self.width
                qImg = QImage(self.image_data.data, self.width, self.height, bytesPerLine,
                              QImage.Format_RGB888).rgbSwapped()
                pixmap = QPixmap.fromImage(qImg)
                self.original_pixmap = pixmap
                self.current_pixmap = pixmap
                self.current_scale_factor = 1
                scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
                self.image_label.setPixmap(scaled_pixmap)
            except Exception as e:
                print(f"加载TIF文件失败: {e}")
        else:
            print("report")
    # 根据按钮的索引来判断哪个按钮被点击

    def rotate_image(self):
        # 顺时针旋转90度并适应image_label的大小
        if hasattr(self, 'original_pixmap'):
            # 获取原始pixmap并根据当前缩放因子调整大小
            original_size = self.original_pixmap.size()
            scaled_original_pixmap = self.original_pixmap.scaled(
                original_size.width() * self.current_scale_factor,
                original_size.height() * self.current_scale_factor,
                Qt.AspectRatioMode.KeepAspectRatio
            )

            # 旋转原始pixmap（已经考虑缩放）
            self.rotate_time += 1
            current_rotate_state = self.rotate_time % 4
            rotated_pixmap = scaled_original_pixmap.transformed(QTransform().rotate(90*current_rotate_state))

            # 计算新的尺寸，确保适应image_label
            target_size = self.image_label.size()
            scaled_rotated_pixmap = rotated_pixmap.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio)

            # 创建一个新的绘图设备来处理裁剪，使得旋转后的图片保持中心对齐
            target_pixmap = QPixmap(target_size)
            target_pixmap.fill(Qt.transparent) # 使用透明背景
            painter = QPainter(target_pixmap)

            # 计算偏移量，使图片的中心点保持不变
            offset_x = (target_size.width() - scaled_rotated_pixmap.width()) / 2
            offset_y = (target_size.height() - scaled_rotated_pixmap.height()) / 2

            # 绘制旋转并调整大小后的图片到目标pixmap上
            painter.drawPixmap(offset_x, offset_y, scaled_rotated_pixmap)
            painter.end()

            # 设置最终的图片到QLabel
            self.image_label.setPixmap(target_pixmap)

    def scale_image(self, factor):
        if hasattr(self, 'original_pixmap'):
            # 确保基于原始图像尺寸进行缩放
            original_width = self.original_pixmap.width()
            original_height = self.original_pixmap.height()

            # 更新缩放因子
            self.current_scale_factor = factor

            # 计算目标尺寸（考虑缩放因子）
            target_width = int(original_width * factor)
            target_height = int(original_height * factor)

            if self.center_statue:
                # 如果有需要裁剪的情况，计算左上角坐标以确保居中裁剪
                start_x = max((original_width - target_width) // 2, 0)
                start_y = max((original_height - target_height) // 2, 0)

                # 存贮放大后的起始坐标
                self.offset = QPoint(-start_x, -start_y)
            else:
                # 图像被移动过，直接读取坐标
                start_x = -self.offset.x()
                start_y = -self.offset.y()

            # 裁剪图像
            # 如果不需要裁剪，可以直接调整pixmap大小
            if self.image_data is not None:
                cropped_image = self.image_data[start_y:start_y + target_height, start_x:start_x + target_width]
                # 确保数据是C连续的，否则会报错
                cropped_image = np.ascontiguousarray(cropped_image)

                # 将裁剪后的图像转换为QImage
                bytesPerLine = 3 * cropped_image.shape[1]
                qImg = QImage(cropped_image.data, cropped_image.shape[1], cropped_image.shape[0], bytesPerLine,
                              QImage.Format_RGB888).rgbSwapped()

                pixmap = QPixmap.fromImage(qImg)
            else:
                # 如果没有image_data，直接从原始pixmap进行缩放
                pixmap = self.original_pixmap.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)

            # 设置最终的图片到 QLabel
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)

    def reset_center_status(self):  # 重置中心位置状态
        self.current_scale_factor = 1

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.image_label.pixmap():
            self.dragging = True
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging and self.image_label.pixmap():
            self.center_statue = 0
            delta = event.pos() - self.drag_start_position
            self.offset += delta
            self.update_image_position()
            self.drag_start_position = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def wheelEvent(self, event: QWheelEvent):
        if self.image_label.pixmap():
            angleDelta = event.angleDelta().y()
            factor = 0.9 if angleDelta > 0 else 1.1
            self.current_scale_factor *= factor
            self.scale_image(self.current_scale_factor)

    def update_image_position(self):
        if hasattr(self, 'original_pixmap'):
            original_size = self.original_pixmap.size()
            # 定位当前位置
            start_x = -self.offset.x()
            start_y = -self.offset.y()

            # 目标大小
            target_width = int(original_size.width() * self.current_scale_factor)
            target_height = int(original_size.height() * self.current_scale_factor)

            cropped_image = self.image_data[start_y:start_y + target_height, start_x:start_x + target_width]
            # 确保数据是C连续的，否则会报错
            cropped_image = np.ascontiguousarray(cropped_image)

            # 将裁剪后的图像转换为QImage
            bytesPerLine = 3 * cropped_image.shape[1]
            qImg = QImage(cropped_image.data, cropped_image.shape[1], cropped_image.shape[0], bytesPerLine,
                          QImage.Format_RGB888).rgbSwapped()

            pixmap = QPixmap.fromImage(qImg)
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)
