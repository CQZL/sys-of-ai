
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


from view.SortWidget import SortWidget
from view.ResultWidget import ResultWidget
from view.PatientWidget import PatientWidget


class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.font = QFont("Arial", 12)
        self.sortWin = SortWidget()
        self.resultWin = ResultWidget()
        self.patientWin = PatientWidget()
        self.init_control()

        #RunModel()

    def init_control(self):
        # 总布局
        self.totallayout = QHBoxLayout()
        self.setLayout(self.totallayout)

        # 1.左侧布局，分为上中下三部分
        self.left_column = QVBoxLayout()
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.sortWin)
        self.stacked_widget.addWidget(self.resultWin)
        self.stacked_widget.addWidget(self.patientWin)

        # 1.1左上 图片信息区
        self.left_column_top = QLabel("请选择图片...")
        self.left_column_top.setFont(self.font)
        self.left_column_top.setFixedHeight(15)
        self.left_column.addWidget(self.left_column_top, 1)

        # 1.2.1左中 - 按钮组
        button_layout = QHBoxLayout()
        self.button_sort = QPushButton("整体排序")
        self.button_sort.setFixedSize(60, 40)
        self.button_result = QPushButton("检测结果")
        self.button_result.setFixedSize(60, 40)
        self.button_patient = QPushButton("病人信息")
        self.button_patient.setFixedSize(60, 40)

        # 为按钮设置最小宽度
        self.button_sort.setMinimumWidth(120)
        self.button_result.setMinimumWidth(120)
        self.button_patient.setMinimumWidth(120)

        # 定义一个通用的样式字符串
        common_button_style = """
            /* 正常状态下的 QPushButton 样式 */
            QPushButton {
                background-color: #696969; /* 浅灰色背景，比白色更柔和 */
                color: black; 
                border: none;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
                padding: 4px 4px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
                transition: background-color 0.3s ease, border-color 0.3s ease; /* 添加过渡效果 */
            }
            /* 鼠标悬停在 QPushButton 上时的样式 */
            QPushButton:hover {
                background-color: #e0e0e0; /* 更浅的灰色背景 */
                border: 1px solid #999999;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 悬停时阴影加深 */
            }
            /* 鼠标按下 QPushButton 时的样式 */
            QPushButton:pressed {
                background-color: red; /* 按下时更深的灰色背景 */
                border: 1px solid #777777;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); /* 按下时阴影变浅 */
                transform: translateY(1px); /* 按下时按钮稍微下沉 */
            }
            /* 按钮获得焦点时的样式 */
            QPushButton:focus {
                outline: none; /* 去除默认的焦点边框 */
                border: 1px solid #0078d7; /* 设置蓝色边框 */
            }
        """

        # 为三个按钮分别设置样式
        self.button_sort.setStyleSheet(common_button_style)
        self.button_result.setStyleSheet(common_button_style)
        self.button_patient.setStyleSheet(common_button_style)

        button_layout.addWidget(self.button_sort)
        button_layout.addWidget(self.button_result)
        button_layout.addWidget(self.button_patient)
#        button_layout.addStretch(1)

        # 创建一个QWidget作为按钮布局的容器，并设置其固定高度
        buttons_container = QWidget()
        buttons_container.setLayout(button_layout)
        buttons_container.setFixedHeight(50)  # 设置固定高度为50像素

        self.left_column.addWidget(buttons_container, 1)

        # 1.2.2左中 - 堆栈层
        self.left_column.addWidget(self.stacked_widget, 8)
        self.stacked_widget.setCurrentWidget(self.patientWin)

        # 添加左侧布局到主布局
        self.totallayout.addLayout(self.left_column, 1)

        # 2.右侧布局
        self.right_column = QVBoxLayout()
        # 2.1第一行
        self.line1 = QHBoxLayout()
        # 2.1.1第一行左侧
        self.line1_left = QVBoxLayout()

        # （1）样本满意度
        label1 = QHBoxLayout()
        text1 = QLabel("样本满意度")
        self.box1 = QComboBox(self)
        self.box1.setStyleSheet("""
            QComboBox { 
                border: 2px solid white; 
            }
            QComboBox:hover { 
                border-color: #FF0000; 
            }
        """)
        self.box1.addItem("满意")
        self.box1.addItem("不满意")
        self.box1.setCurrentIndex(0)  # 设置默认值
        self.box1.currentIndexChanged.connect(self.on_box1_changed)
        label1.addWidget(text1)
        label1.addWidget(self.box1)
        self.line1_left.addLayout(label1)

        # （2）上皮细胞数
        label2 = QHBoxLayout()
        text2 = QLabel("上皮细胞数")
        self.box2 = QComboBox(self)
        self.box2.setStyleSheet("""
            QComboBox { 
                border: 2px solid white; 
            }
            QComboBox:hover { 
                border-color: #FF0000; 
            }
        """)
        self.box2.addItem(">5000个细胞")
        self.box2.addItem("其他")
        self.box2.setCurrentIndex(0)  # 设置默认值
        self.box2.currentIndexChanged.connect(self.on_box2_changed)
        label2.addWidget(text2)
        label2.addWidget(self.box2)
        self.line1_left.addLayout(label2)

        # （3）颈管细胞
        label3 = QHBoxLayout()
        text3 = QLabel("颈管细胞")
        self.option1_1 = QRadioButton("有", self)
        self.option1_2 = QRadioButton("无", self)
        group1 = QButtonGroup(self)  # 创建第一个按钮组
        group1.addButton(self.option1_1)
        group1.addButton(self.option1_2)
        self.option1_1.setChecked(True)
        label3.addWidget(text3)
        label3.addWidget(self.option1_1)
        label3.addWidget(self.option1_2)
        self.option1_1.toggled.connect(self.on_option_1_toggled)
        self.option1_2.toggled.connect(self.on_option_1_toggled)
        self.line1_left.addLayout(label3)

        # （4）化生细胞
        label4 = QHBoxLayout()
        text4 = QLabel("化生细胞")
        self.option2_1 = QRadioButton("有", self)
        self.option2_2 = QRadioButton("无", self)
        group1 = QButtonGroup(self)  # 创建第一个按钮组
        group1.addButton(self.option2_1)
        group1.addButton(self.option2_2)
        self.option2_1.setChecked(True)
        label4.addWidget(text4)
        label4.addWidget(self.option2_1)
        label4.addWidget(self.option2_2)
        self.option2_1.toggled.connect(self.on_option_2_toggled)
        self.option2_2.toggled.connect(self.on_option_2_toggled)
        self.line1_left.addLayout(label4)

        # （5）炎症程度
        label5 = QHBoxLayout()
        text5 = QLabel("炎症程度")
        self.box5 = QComboBox(self)
        self.box5.setStyleSheet("""
            QComboBox { 
                border: 2px solid white; 
            }
            QComboBox:hover { 
                border-color: lightgray; 
            }
        """)
        self.box5.addItem("无")
        self.box5.addItem("其他")
        self.box5.setCurrentIndex(0)  # 设置默认值
        self.box5.currentIndexChanged.connect(self.on_box5_changed)
        label5.addWidget(text5)
        label5.addWidget(self.box5)
        self.line1_left.addLayout(label5)
        # 第一行左侧添加进第一行
        self.line1.addLayout(self.line1_left)

        # 2.1.2第一行右侧
        self.line1_right = QVBoxLayout()

        # 初始化用于存储选择的字典
        self.selected_options_1 = {}
        # 创建多选题的选项并设置信号槽
        options = ["放线菌", "菌群转变", "滴虫感染", "霉菌感染", "HPV感染", "疱疹病毒感染"]
        for option in options:
            checkbox = QCheckBox(option)
            self.line1_right.addWidget(checkbox)
            # 将每个复选框的toggled信号连接到处理函数
            checkbox.toggled.connect(lambda checked, text=option: self.on_checkbox_toggled_1(text, checked))

        # 第一行添加到布局
        self.line1.addLayout(self.line1_right)
        self.right_column.addLayout(self.line1)

        # 2.2第二行
        self.line2 = QVBoxLayout()
        text_line_2_2 = QLabel("鳞状上皮细胞")
        text_line_2_2.setStyleSheet("font: bold; font-size: 18px;")
        text_line_2_2.setFixedSize(150, 50)
        self.line2.addWidget(text_line_2_2)
        # 初始化用于存储选择的字典
        self.selected_options_2 = {}
        # 选项列表
        options_1 = ["未见上皮内病变", "非典型鳞状细胞", "正常", "不能明确意义", "炎症",
                     "倾向上皮细胞内高度病变", "表皮细胞萎缩", "倾向上皮内瘤变", "宫内节育器反应",
                     "上皮内低度病变", "妊娠反应", "上皮内高度病变", "放疗反应", "CIN-II级",
                     "其他", "CIN-III级", "鳞状细胞癌"]

        # 当前行的水平布局和计数器
        current_h_layout_1 = QHBoxLayout()
        option_counter_1 = 0
        for option in options_1:
            checkbox_1 = QCheckBox(option)
            # 将每个复选框的toggled信号连接到处理函数
            checkbox_1.toggled.connect(lambda checked, text=option: self.on_checkbox_toggled_2(text, checked))

            # 添加复选框到当前行布局
            current_h_layout_1.addWidget(checkbox_1)
            option_counter_1 += 1

            # 如果当前行已达到两个选项，则更新主布局，并重置当前行布局和计数器
            if option_counter_1 == 2:
                self.line2.addLayout(current_h_layout_1)
                current_h_layout_1 = QHBoxLayout()
                option_counter_1 = 0

        # 如果最后一行未满两个选项，也需要将它加入主布局
        if option_counter_1 > 0:
            self.line2.addLayout(current_h_layout_1)

        # 第二行添加到布局
        self.right_column.addLayout(self.line2)

        # 2.3第三行
        self.line3 = QVBoxLayout()
        text_line_2_3 = QLabel("腺上皮细胞")
        text_line_2_3.setStyleSheet("font: bold; font-size: 18px;")
        text_line_2_3.setFixedSize(150, 50)
        self.line3.addWidget(text_line_2_3)
        # 初始化用于存储选择的字典
        self.selected_options_3 = {}
        # 选项列表
        options_2 = ["非典型腺细胞", "腺癌", "非典型性腺细胞", "倾向原位腺癌", "宫颈管",
                     "宫内膜", "不能明确意义", "宫内膜", "来源不明",
                     "倾向良性反应性改变", "其他", "可疑腺癌"]

        # 当前行的水平布局和计数器
        current_h_layout_2 = QHBoxLayout()
        option_counter_2 = 0
        for option in options_2:
            checkbox_2 = QCheckBox(option)
            # 将每个复选框的toggled信号连接到处理函数
            checkbox_2.toggled.connect(lambda checked, text=option: self.on_checkbox_toggled_3(text, checked))

            # 添加复选框到当前行布局
            current_h_layout_2.addWidget(checkbox_2)
            option_counter_2 += 1

            # 如果当前行已达到三个选项，则更新主布局，并重置当前行布局和计数器
            if option_counter_2 == 3:
                self.line3.addLayout(current_h_layout_2)
                current_h_layout_2 = QHBoxLayout()
                option_counter_2 = 0

        # 如果最后一行未满三个选项，也需要将它加入主布局
        if option_counter_2 > 0:
            self.line2.addLayout(current_h_layout_2)
        # 第三行添加到布局
        self.right_column.addLayout(self.line3)

        # 2.4第四行
        self.line4 = QHBoxLayout()
        self.line4.setAlignment(Qt.AlignLeft)
        # 左侧文字
        text_line_4 = QLabel("选\n取\n截\n图", self)
        text_line_4.setAlignment(Qt.AlignCenter)
        text_line_4.setStyleSheet("font: bold; font-size: 18px;")
        # 右侧框框
        # 按钮，包含虚线边框和图片
        button_with_image = QPushButton(self)
        button_with_image.setStyleSheet("""
            QPushButton {
                border: 2px dashed gray;
                border-radius: 5px;
                padding: 5px;
                background-color: transparent; 
            }
            QPushButton:hover {
                background-color: gray; 
            }
            QPushButton:pressed {
                background-color: blue;
            }
        """)
        button_with_image.setIconSize(button_with_image.size())
        button_with_image.setFixedSize(150, 100)  # 设置固定大小

        # 加载并设置图片
        pixmap = QPixmap("icon/picture.png")  # 替换为你的图片路径
        button_with_image.setIcon(pixmap)
        button_with_image.clicked.connect(self.on_button_with_image_clicked)
        self.line4.addWidget(text_line_4)
        self.line4.addWidget(button_with_image)
        # 第四行添加到布局
        self.right_column.addLayout(self.line4)

        # 第五行
        self.line5 = QVBoxLayout()
        self.line5.setSpacing(0)
        text_line_5 = QLabel("诊断结果")
        text_line_5.setStyleSheet("font: bold")
        text_line_5.setFixedSize(100, 50)
        self.box_line_5 = QComboBox(self)
        self.box_line_5.setStyleSheet("""
            QComboBox { 
                border: 2px solid white; 
            }
            QComboBox:hover { 
                border-color: lightgray; 
            }
        """)
        self.box_line_5.setFixedHeight(30)
        self.box_line_5.addItem("未见上皮内病变或恶性细胞(NILM).")
        self.box_line_5.addItem("其他")
        self.box_line_5.setCurrentIndex(0)  # 设置默认值
        self.box_line_5.currentIndexChanged.connect(self.on_box_line_5_changed)
        self.line5.addWidget(text_line_5)
        self.line5.addWidget(self.box_line_5)
        self.right_column.addLayout(self.line5)

        # 第六行
        self.line6 = QVBoxLayout()
        self.line6.setSpacing(0)
        text_line_6 = QLabel("附注建议")
        text_line_6.setStyleSheet("font: bold")
        text_line_6.setFixedSize(100, 50)
        self.box_line_6 = QComboBox(self)
        self.box_line_6.setStyleSheet("""
            QComboBox { 
                border: 2px solid white; 
            }
            QComboBox:hover { 
                border-color: lightgray; 
            }
        """)
        self.box_line_6.setFixedHeight(30)
        self.box_line_6.addItem("请选择")
        self.box_line_6.addItem("其他")
        self.box_line_6.setCurrentIndex(0)  # 设置默认值
        self.box_line_6.currentIndexChanged.connect(self.on_box_line_6_changed)
        self.line6.addWidget(text_line_6)
        self.line6.addWidget(self.box_line_6)
        self.right_column.addLayout(self.line6)

        # 第七行
        self.line7 = QVBoxLayout()
        self.line7.setAlignment(Qt.AlignCenter)  # 设置布局中的组件居中对齐

        # 创建三个按钮并设置样式
        button_preview = QPushButton("预览", self)
        button_save = QPushButton("保存", self)
        button_diagnose = QPushButton("诊断", self)

        #设置诊断按钮响应
        button_diagnose.clicked.connect(self.on_diagnose_button_clicked)

        # 设置按钮固定大小
        fixed_size = (90, 40)  # 宽度100像素，高度50像素
        button_preview.setFixedSize(*fixed_size)
        button_save.setFixedSize(*fixed_size)
        button_diagnose.setFixedSize(*fixed_size)

        # 设置按钮的样式表
        button_preview.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: gray;
                        border: none;
                        font: bold;
                    }
                    QPushButton:hover {
                        background-color: #cccccc;
                    }
                    QPushButton:pressed {
                        background-color: #999999;
                    }
                """)
        button_save.setStyleSheet("""
                    QPushButton {
                        background-color: blue;
                        color: white;
                        border: none;
                        font: bold;
                    }
                    QPushButton:hover {
                        background-color: #0000aa;
                    }
                    QPushButton:pressed {
                        background-color: #000088;
                    }
                """)
        button_diagnose.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                        border: none;
                        font: bold;
                    }
                    QPushButton:hover {
                        background-color: #008800;
                    }
                    QPushButton:pressed {
                        background-color: #005500;
                    }
                """)

        # 将按钮添加到水平布局中，以确保它们之间没有空隙
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(button_preview)
        buttons_layout.addWidget(button_save)
        buttons_layout.addWidget(button_diagnose)
        buttons_layout.setSpacing(0)  # 移除按钮之间的间距
        buttons_layout.setContentsMargins(0, 0, 0, 0)  # 移除布局的边距
        # 将水平布局添加到第七行布局中
        self.line7.addLayout(buttons_layout)

        # 第七行添加到主布局
        self.right_column.addLayout(self.line7)

        # 添加右侧布局到主布局
        self.totallayout.addLayout(self.right_column, 1)

    def on_box1_changed(self, index):
        selected_text = self.box1.itemText(index)
        print(f"样本满意度: {selected_text}")

    def on_box2_changed(self, index):
        selected_text = self.box2.itemText(index)
        print(f"上皮细胞数: {selected_text}")

    def on_option_1_toggled(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print(f"颈管细胞：{radioButton.text()}")

    def on_option_2_toggled(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print(f"化生细胞：{radioButton.text()}")

    def on_box5_changed(self, index):
        selected_text = self.box2.itemText(index)
        print(f"炎症程度: {selected_text}")

    def on_checkbox_toggled_1(self, text, checked):
        if checked:
            self.selected_options_1[text] = True  # 记录选择
        else:
            del self.selected_options_1[text]  # 移除取消选择的选项

        # 这里可以根据需要对selected_options进行进一步处理
        print(f"样本种类: {list(self.selected_options_1.keys())}")

    def on_checkbox_toggled_2(self, text, checked):
        if checked:
            self.selected_options_2[text] = True  # 记录选择
        else:
            del self.selected_options_2[text]  # 移除取消选择的选项

        # 这里可以根据需要对selected_options进行进一步处理
        print(f"鳞状上皮细胞: {list(self.selected_options_2.keys())}")

    def on_checkbox_toggled_3(self, text, checked):
        if checked:
            self.selected_options_3[text] = True  # 记录选择
        else:
            del self.selected_options_3[text]  # 移除取消选择的选项

        # 这里可以根据需要对selected_options进行进一步处理
        print(f"腺上皮细胞: {list(self.selected_options_3.keys())}")

    def on_button_with_image_clicked(self):
        print("选取截图按钮被点击")

    def on_box_line_5_changed(self, index):
        selected_text = self.box_line_5.itemText(index)
        print(f"诊断结果: {selected_text}")

    def on_box_line_6_changed(self, index):
        selected_text = self.box_line_6.itemText(index)
        print(f"附注建议: {selected_text}")

    def on_diagnose_button_clicked(self):
        from view.RunModel import RunModel
        self.run = RunModel()
        self.run.run_model()

