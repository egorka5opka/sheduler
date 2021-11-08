import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from main_form import Ui_MainWindow
from odjects_list import ObjectList
from loading import LoadWidget


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show_list_btn.triggered.connect(self.show_object_list)
        self.load_btn.triggered.connect(self.upload_object)

    def show_object_list(self):
        self.showing = ObjectList()
        self.showing.show()

    def upload_object(self):
        self.loading = LoadWidget()
        self.loading.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    exit(app.exec())
