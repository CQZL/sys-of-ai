import os
import pandas as pd
from pathlib import Path
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ImageWidget import ImageWidget


class PatientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = None
        self.current_page = 0
        self.page_size = 18
        self.image_paths = []
        self.init_ui()
        self.show_placeholder("请先选择图片文件")

    def init_ui(self):
        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # 图片显示区域
        self.image_widget = QWidget()
        self.image_layout = QGridLayout()
        self.image_layout.setSpacing(0)
        self.image_widget.setLayout(self.image_layout)
        self.main_layout.addWidget(self.image_widget)

        # 分页导航布局
        self.pagination_layout = QHBoxLayout()
        self.last_layout = QVBoxLayout()

        # 上一页按钮
        self.prev_page_button = QPushButton("上一页")
        self.prev_page_button.clicked.connect(self.prev_page)
        self.pagination_layout.addWidget(self.prev_page_button)

        # 下一页按钮
        self.next_page_button = QPushButton("下一页")
        self.next_page_button.clicked.connect(self.next_page)
        self.pagination_layout.addWidget(self.next_page_button)

        # 输入框和跳转按钮
        self.page_input = QLineEdit()
        self.page_input.setMaximumWidth(50)
        self.pagination_layout.addWidget(self.page_input)

        self.go_button = QPushButton("跳转")
        self.go_button.clicked.connect(self.go_to_page)
        self.pagination_layout.addWidget(self.go_button)



        # 显示当前页和总页数的标签
        self.page_info_label = QLabel()
        self.last_layout.addWidget(self.page_info_label)

        self.main_layout.addLayout(self.last_layout)
        self.main_layout.addLayout(self.pagination_layout)


    def set_filename(self, filename: str):
        """接收主界面传递的文件路径"""
        self.filename = filename
        print(f"接收到文件路径: {filename}")
        csv_path = self._get_csv_path()
        print(f"正在读取文件: {csv_path}")

        if not csv_path or not csv_path.exists():
            print("未找到检测结果文件")
            self.show_placeholder("未找到检测结果文件")
            return

        try:
            # 读取CSV文件
            print(f"正在读取文件: {csv_path}")
            df = pd.read_csv(csv_path)
            if df.empty:
                self.show_placeholder("检测结果文件为空")
                return

            # 获取第一列数据（排除表头）
            self.image_paths = df.iloc[1:, 0].tolist()  # 假设第一行是表头
            print(self.image_paths)
            valid_paths = [p for p in self.image_paths if os.path.exists(p)]
            print(valid_paths)

            if not valid_paths:
                self.show_placeholder("未找到有效图片路径")
                return

            self.current_page = 0
            self.update_page_info_label()
            self.display_images()

        except Exception as e:
            print(f"读取检测结果失败: {str(e)}")
            self.show_placeholder(f"读取检测结果失败: {str(e)}")

    def _get_csv_path(self):
        """生成CSV文件路径"""
        if not self.filename:
            return None

        try:
            path = Path(self.filename)
            # 构建结果路径：原文件所在目录/原文件名_result/detection_result.csv
            print(path)
            print(path.parent / path.stem / "result" / "detection_results.csv")
            return path.parent / path.stem / "result" / "detection_results.csv"
        except Exception as e:
            print(f"路径生成错误: {str(e)}")
            return None

    def display_images(self):
        """显示当前页的图片列表"""
        # 清空现有内容
        while self.image_layout.count():
            item = self.image_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size
        current_page_paths = self.image_paths[start_index:end_index]

        if not current_page_paths:
            self.show_placeholder("没有更多图片")
            return

        for idx, img_path in enumerate(current_page_paths):
            try:
                image_widget = ImageWidget(img_path, os.path.basename(img_path))
                row = idx // 3  # 每行3张图片
                col = idx % 3
                self.image_layout.addWidget(image_widget, row * 2, col)

                # 添加行间距（奇数行作为间距）
                if row > 0:
                    self.image_layout.addItem(
                        QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed),
                        row * 2 - 1, 0, 1, 3
                    )

            except Exception as e:
                print(f"加载图片失败 [{img_path}]: {str(e)}")

        # 添加底部伸缩空间
        total_rows = (len(current_page_paths) + 2) // 3 * 2
        self.image_layout.setRowStretch(total_rows, 1)

        # 更新分页按钮状态
        self.prev_page_button.setEnabled(self.current_page > 0)
        self.next_page_button.setEnabled(end_index < len(self.image_paths))

        # 更新页码信息
        self.update_page_info_label()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_images()

    def next_page(self):
        end_index = (self.current_page + 1) * self.page_size
        if end_index < len(self.image_paths):
            self.current_page += 1
            self.display_images()

    def go_to_page(self):
        try:
            page = int(self.page_input.text()) - 1
            total_pages = len(self.image_paths) // self.page_size + (
                1 if len(self.image_paths) % self.page_size != 0 else 0)
            if 0 <= page < total_pages:
                self.current_page = page
                self.display_images()
        except ValueError:
            pass

    def show_placeholder(self, message="请先选择图片文件"):
        """显示提示信息"""
        # 清空布局
        while self.image_layout.count():
            item = self.image_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 创建占位标签
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; color: #666;")

        # 将标签添加到布局中心
        self.image_layout.addWidget(label, 0, 0, Qt.AlignCenter)

    def image_clicked(self, path):
        """图片点击事件"""
        print(f"图片被点击: {path}")

    def update_page_info_label(self):
        total_pages = len(self.image_paths) // self.page_size + (
            1 if len(self.image_paths) % self.page_size != 0 else 0)
        self.page_info_label.setText(f"当前页: {self.current_page + 1} / 总页数: {total_pages}")

