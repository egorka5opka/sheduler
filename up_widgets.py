from PyQt5.QtWidgets import QTableWidget
# from up_widgets import ObjectChoice

class ObjectChoice(QTableWidget):
    def __init__(self, data):
        super().__init__(data)

    def dragEnterEvent(self, e):
        print("enter drag")

    def dragMoveEvent(self, event):
        print("moving element")

    def dragLeaveEvent(self, event):
        print("drag leave")

    def dropEvent(self, event):
        print("drop")
