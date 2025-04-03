from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from InfoWidget import InfoWidget
import tifffile
import numpy as np


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.original_pixmap = None  # 原始图像
        self.current_pixmap = None  # 当前显示的图像
        self.image_data = None  # 图像数据

        self.dragging = False  # 是否正在拖拽
        self.offset = QPoint(0, 0)  # 图片偏移量

        self.font = QFont("Arial", 12)
        self.InfoWin = InfoWidget()
        self.current_scale_factor = 1  # 当前缩放因子，默认为1（未缩放）
        self.center_statue = 1
        self.rotate_time = 0
        self.init_control()
        self.current_index = -1  # 当前显示的图片索引，初始化为-1表示没有加载图片
        self.default_background_path = "../icon/back.png"

        self.set_default_background()

    def init_control(self):
        # 总布局
        self.totallayout = QHBoxLayout()
        self.setLayout(self.totallayout)

        # 1.左侧图片层
        self.left_column = QVBoxLayout()

        # 1.1左上信息层
        self.left_column_top = QHBoxLayout()

        # 1.1.0 添加logo
        self.logo_label = QLabel()
        pixmap = QPixmap('../icon/logo1.png')
        scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(75, 40)
        self.left_column_top.addWidget(self.logo_label)

        # 1.1.1添加返回按钮
        self.show_queue_btn = QPushButton("返回上一界面")
        self.left_column_top.addWidget(self.show_queue_btn)
        self.show_queue_btn.setFixedHeight(30)
        self.show_queue_btn.setFlat(True)
        self.show_queue_btn.resize(800, 80)

        icon = QIcon("../icon/return.png")
        self.show_queue_btn.setIcon(icon)
        self.show_queue_btn.setIconSize(QSize(15, 15))

        self.show_queue_btn.setStyleSheet("""
                   QPushButton {
                       background-color:#BBFFFF;
                       padding: 5px;
                       border: 2px solid #555555;
                       border-radius: 5px;
                       font-size: 14px;
                       font: bold;
                   }
                   QPushButton:hover {
                       background-color: #AEEEEE;
                   }
               """)
        self.left_column_top.addStretch()  # 添加一个伸缩条

        # 分隔符
        separator = QLabel('|', self)
        self.left_column_top.addWidget(separator)

        # 导入图片按钮
        load_button = QPushButton("导入图片")
        load_button.setFlat(True)
        load_button.resize(200, 80)
        icon_1 = QIcon("../icon/picture.png")
        self.show_queue_btn.setIcon(icon_1)
        self.left_column_top.addWidget(load_button)
        load_button.setStyleSheet("""
                    QPushButton {
                background-color: #0000FF;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
                """)
        load_button.clicked.connect(self.on_icon_button_clicked)

        # 添加清除图像按钮
        self.remove_queue_btn = QPushButton("清除图像")
        icon_2 = QIcon("../icon/clear.png")
        self.show_queue_btn.setIcon(icon_2)
        self.left_column_top.addWidget(self.remove_queue_btn)
        self.remove_queue_btn.setFixedHeight(30)
        self.remove_queue_btn.setFlat(True)
        self.remove_queue_btn.resize(400, 80)

        icon2 = QIcon()
        self.remove_queue_btn.setIcon(icon2)
        self.remove_queue_btn.setIconSize(QSize(15, 15))

        self.remove_queue_btn.setStyleSheet("""
            QPushButton {
                background-color:#DDA0DD;
                padding: 5px;
                border: 2px solid #555555;
                border-radius: 5px;
                font-size: 12px;
                font: bold;
            }
            QPushButton:hover {
                background-color:#EE82EE;  
            }
        """)
        self.remove_queue_btn.clicked.connect(self.remove_image)

        # 分隔符
        separator = QLabel('|', self)
        self.left_column_top.addWidget(separator)

        # 文字按钮（2x, 4x, 10x, 20x, 40x）
        scales = [("1x", 1),("2x", 2), ("4x", 4), ("10x", 10), ("20x", 20), ("40x", 40)]
        for scale_text, scale_factor in scales:
            button = QPushButton(scale_text)
            button.setFixedHeight(30)
            button.setFixedWidth(35)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FFEFD5; 
                    border: 2px solid #555555;
                    padding: 5px;
                    border-radius: 5px;
                    font-size: 12px;
                    font: bold;
                }  
                QPushButton:hover {
                    background-color: #FFDEAD;  
                }
            """)
            button.clicked.connect(lambda *args, f=scale_factor: self.scale_image(f))
            self.left_column_top.addWidget(button)

        # 添加Fit按钮及其后的输入框
        self.fit_button = QPushButton("Fit")
        self.fit_button.setFixedWidth(40)
        self.fit_button.setStyleSheet("""
                QPushButton {
                    background-color: #FFEFD5; 
                    border: 2px solid #555555;
                    padding: 5px;
                    border-radius: 5px;
                    font-size: 12px;
                    font: bold;
                }  
                QPushButton:hover {
                    background-color: #FFDEAD;  
                }
            """)
        self.scale_input = QLineEdit(self)
        self.scale_input.setMaximumWidth(50)  # 设置输入框最大宽度
        self.left_column_top.addWidget(self.scale_input)
        self.left_column_top.addWidget(self.fit_button)
        # 分隔符
        separator = QLabel('|', self)
        self.left_column_top.addWidget(separator)

        # 上一例和下一例按钮
        self.prev_button = QPushButton("上一例")
        self.next_button = QPushButton("下一例")

        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F8FF; 
                border: 2px solid #555555;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #E6E6FA;  
            }    
        """)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F8FF; 
                border: 2px solid #555555;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #E6E6FA;  
            }
        """)
        self.left_column_top.addWidget(self.prev_button)
        self.left_column_top.addWidget(self.next_button)

        # 1.2左下图片层
        self.left_column_bottom = QHBoxLayout()

        # 放置图片层
        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(200, 200)
        self.left_column_bottom.addWidget(self.image_label)
        # 设置图片层背景为深灰色
        self.left_column.addLayout(self.left_column_top, 1)  # 占1行
        self.left_column.addLayout(self.left_column_bottom, 9)  # 设置图片层占9行
        self.totallayout.addLayout(self.left_column, 1)  # 设置左侧占1行

        # 右侧标记层
        self.right_column = QVBoxLayout()
        self.right_column.addWidget(self.InfoWin)
        self.totallayout.addLayout(self.right_column, 1)

    def on_icon_button_clicked(self):
        self.lead_image()
        print("leading")

    def lead_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.xpm *.jpg *.tif)")
        print(type(filename))
        print(filename)
        if filename:
            self.InfoWin.receive_filename(filename)
        #            self.InfoWin.patientWin.set_filename(filename)
        # 添加读取tif文件格式的图片
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

    def remove_image(self):
        """清除当前显示的图像"""
        if self.current_pixmap:
            self.image_label.clear()
            self.image_data = None
            self.original_pixmap = None
            self.current_pixmap = None
            self.current_scale_factor = 1
            self.offset = QPoint(0, 0)
            self.set_default_background()
            QMessageBox.information(self, "清除成功", "当前图像已清除")
        else:
            QMessageBox.information(self, "提示", "当前没有显示的图像")

    def scale_image(self, factor):  # 图片倍数放大缩小
        if not self.original_pixmap:
            return
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
        if not self.original_pixmap:
            return

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

    def set_default_background(self):
        pixmap = QPixmap(self.default_background_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

