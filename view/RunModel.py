
class RunModel:
    def __init__(self):
        self.run_model()

    def run_model(self):
        from view.MainWidget import MainWidget
        self.main = MainWidget()
        # 图片链接,后期换成地址队列
        image_path = self.main.lead_image().fileName()
        # 接入模型-运行
        print(image_path)


