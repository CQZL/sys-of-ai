import sys
import time
from PySide6.QtCore import QPropertyAnimation  # 导入 QPropertyAnimation 类
from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton,
    QFileDialog, QListWidgetItem, QMainWindow, QLabel, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt, QObject, Signal, QThread, QMutex, QMutexLocker, QSize, QEasingCurve
from MainWidget import MainWidget

APP_FONT = QFont()
APP_FONT.setPointSize(14)  # 设置默认字体大小


class ProcessingQueueWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.queue_manager = QueueManager()
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(20)

        top_layout = QHBoxLayout()

        # 标题
        logo_label = QLabel()
        pixmap = QPixmap('../icon/logo1.png')
        scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(75, 40)
        top_layout.addWidget(logo_label)

        header = QLabel("WSI 文件处理队列")
        header.setFont(APP_FONT)
        top_layout.addWidget(header)

        main_layout.addLayout(top_layout)

        # 按钮容器
        btn_frame = QFrame()
        btn_frame.setStyleSheet("""
            QFrame {
                background: #3F51B5;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        btn_container = QHBoxLayout(btn_frame)
        btn_container.setContentsMargins(0, 0, 0, 0)

        # 功能按钮
        self.add_btn = self.create_icon_button("➕ 添加文件", "addBtn")
        self.clear_btn = self.create_icon_button("🗑️ 清空队列", "clearBtn")
        self.remove_btn = self.create_icon_button("✖️ 移除选中", "removeBtn")
        self.show_work_btn = self.create_icon_button("📊 显示工作", "showWorkBtn")

        # 添加按钮到容器
        btn_container.addWidget(self.add_btn)
        btn_container.addWidget(self.clear_btn)
        btn_container.addWidget(self.remove_btn)
        btn_container.addWidget(self.show_work_btn)

        # 队列列表区域
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)

        # 待处理队列
        pending_label = QLabel("待处理队列（勾选要操作的文件）")
        pending_label.setFont(APP_FONT)
        self.pending_list = self.create_styled_list()

        # 处理队列
        processing_label = QLabel("处理队列")
        processing_label.setFont(APP_FONT)
        self.processing_list = self.create_styled_list()

        # 确认按钮栏
        self.confirm_btn = QPushButton("✅ 确认添加")
        self.confirm_btn.setObjectName("confirmBtn")
        self.confirm_btn.setStyleSheet("""
            QPushButton#confirmBtn {
                background-color: #4CAF50;
                padding: 8px 20px;
                border-radius: 15px;
                min-width: 120px;
                font-size: 18px;
                color: white;
            }
            QPushButton#confirmBtn:hover {
                background-color: #66BB6A;
            }
        """)

        # 组装界面
        list_layout.addWidget(pending_label)
        list_layout.addWidget(self.pending_list)
        list_layout.addWidget(self.confirm_btn)
        list_layout.addWidget(processing_label)
        list_layout.addWidget(self.processing_list)

        # 主布局添加组件
        # main_layout.addWidget(logo_label)
        # main_layout.addWidget(header)
        main_layout.addWidget(btn_frame)
        main_layout.addWidget(list_container)
        self.setLayout(main_layout)

    def create_icon_button(self, text, btn_id):
        """创建带样式的图标按钮"""
        btn = QPushButton(text)
        btn.setObjectName(btn_id)
        btn.setFont(APP_FONT)
        btn.setFixedSize(QSize(140, 40))
        btn.setStyleSheet(f"""
            QPushButton#{btn_id} {{
                background-color: #03A9F4;
                color: white;
                border-radius: 15px;
                padding: 8px 12px;
            }}
            QPushButton#{btn_id}:hover {{
                background-color: #29B6F6;
            }}
            QPushButton#{btn_id}:pressed {{
                background-color: #0288D1;
            }}
        """)
        btn.clicked.connect(lambda: self.animate_button(btn))
        return btn

    def animate_button(self, btn):
        """按钮点击动画"""
        animation = QPropertyAnimation(btn, b"geometry")
        animation.setDuration(200)
        animation.setStartValue(btn.geometry())
        animation.setEndValue(btn.geometry().adjusted(-2, -2, 2, 2))
        animation.setEasingCurve(QEasingCurve.OutBack)
        animation.start()

    def create_styled_list(self):
        """创建样式化列表组件"""
        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget {
                background: #F5F5F5;
                border: 1px solid #BDBDBD;
                border-radius: 8px;
                padding: 6px;
                min-height: 200px;
            }
            QListWidget::item {
                background: white;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                margin: 4px;
                padding: 8px;
                color: #424242;
            }
            QListWidget::item:alternate {
                background: #F9F9F9;
            }
            QListWidget::item:selected {
                background: #03A9F4;
                color: white;
            }
        """)
        list_widget.setAlternatingRowColors(True)
        return list_widget

    def connect_signals(self):
        """连接信号与槽"""
        self.add_btn.clicked.connect(self.add_files)
        self.clear_btn.clicked.connect(self.clear_queue)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.confirm_btn.clicked.connect(self.confirm_selection)

        self.queue_manager.task_added.connect(self.add_processing_item)
        self.queue_manager.task_started.connect(self.update_processing_status)
        self.queue_manager.task_finished.connect(self.handle_task_finished)

    # 以下是业务逻辑方法
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择WSI文件", "", "WSI Files (*.ndpi *.svs *.tif)")
        for file in files:
            if not self.is_file_in_list(file, self.pending_list):
                item = QListWidgetItem(file)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self.pending_list.addItem(item)

    def is_file_in_list(self, file_path, list_widget):
        return any(list_widget.item(i).text() == file_path
                   for i in range(list_widget.count()))

    def confirm_selection(self):
        """将选中的文件移入处理队列"""
        for i in reversed(range(self.pending_list.count())):
            item = self.pending_list.item(i)
            if item.checkState() == Qt.Checked:
                file_path = item.text()
                if not self.is_file_in_list(file_path, self.processing_list):
                    self.queue_manager.add_task(file_path)
                self.pending_list.takeItem(i)
        #processing_files = [self.processing_list.item(i).text() for i in range(self.processing_list.count())]

        processing_files = [
            self.processing_list.item(i).text()[6:]  # 去掉前5个字符
            for i in range(self.processing_list.count())
        ]
        print("Processing files:", processing_files)
        #file_paths = self.queue_manager.get_tasks()
        # 假设 processing_files 是已处理好的文件路径列表
        from wsi_mdoel_run import Pipeline
        pipeline = Pipeline()
        for file_path in processing_files:
            try:
                # 调用模型处理文件（根据实际模型接口调整参数）
                pipeline.run(image_path=file_path)  # 或直接 run_model(file_path)
                #print(f"Processing completed: {file_path} → Result: {result}")

            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

    def remove_selected(self):
        """从待处理队列移除选中项"""
        for i in reversed(range(self.pending_list.count())):
            if self.pending_list.item(i).checkState() == Qt.Checked:
                self.pending_list.takeItem(i)

    def add_processing_item(self, file_path):
        """添加任务到处理队列"""
        item = QListWidgetItem(f"等待处理: {file_path}")
        item.file_path = file_path
        self.processing_list.addItem(item)

    def update_processing_status(self, file_path):
        """更新任务状态为处理中"""
        for i in range(self.processing_list.count()):
            item = self.processing_list.item(i)
            if item.file_path == file_path:
                item.setText(f"处理中: {file_path}")
                item.setBackground(Qt.yellow)

    def handle_task_finished(self, file_path):
        """更新任务状态为已完成"""
        for i in range(self.processing_list.count()):
            item = self.processing_list.item(i)
            if item.file_path == file_path:
                item.setText(f"已完成: {file_path}")
                item.setBackground(Qt.green)

    def clear_queue(self):
        """清空处理队列"""
        self.processing_list.clear()
        self.queue_manager.clear_queue()


class QueueManager(QObject):
    """队列管理类，负责线程调度"""
    task_added = Signal(str)
    task_started = Signal(str)
    task_finished = Signal(str)

    def __init__(self):
        super().__init__()
        self.queue = []
        self.mutex = QMutex()
        self.worker = None
        self.running = False

    def add_task(self, file_path):
        with QMutexLocker(self.mutex):
            self.queue.append(file_path)
            self.task_added.emit(file_path)
        self.start_processing()

    def start_processing(self):
        if not self.running:
            self.running = True
            self.worker = Worker(self)
            self.worker.task_started.connect(self.task_started.emit)
            self.worker.task_finished.connect(self.task_finished.emit)
            self.worker.finished.connect(self.on_worker_finished)
            self.worker.start()

    def clear_queue(self):
        with QMutexLocker(self.mutex):
            self.queue.clear()

    def on_worker_finished(self):
        self.running = False


class Worker(QThread):
    """工作线程类"""
    task_started = Signal(str)
    task_finished = Signal(str)

    def __init__(self, queue_manager):
        super().__init__()
        self.queue_manager = queue_manager

    def run(self):
        while True:
            with QMutexLocker(self.queue_manager.mutex):
                if not self.queue_manager.queue:
                    break
                file_path = self.queue_manager.queue.pop(0)

            self.task_started.emit(file_path)
            # 模拟处理过程（实际应替换为真实逻辑）
            time.sleep(2)
            self.task_finished.emit(file_path)


class QueueWork(QMainWindow):
    def __init__(self):
        super().__init__()
        self.queue_widget = ProcessingQueueWidget()
        self.setCentralWidget(self.queue_widget)