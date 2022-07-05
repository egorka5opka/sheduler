from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog


class Row(QWidget):
    DEFAULT_SPACE = 15

    def __init__(self, par, width):
        super().__init__(par)
        self.width = width
        self.space = self.DEFAULT_SPACE
        btns_widget = QWidget(self)
        btns_layout = QVBoxLayout(btns_widget)
        self.delete_btn = QPushButton('delete', btns_widget)
        self.delete_btn.clicked.connect(self.delete)
        btns_layout.addWidget(self.delete_btn)
        self.edit_btn = QPushButton('edit', btns_widget)
        btns_layout.addWidget(self.edit_btn)

        self.rebuild_row()

    def delete(self):
        self.deleteLater()

    def edit(self):
        space, ok_pressed = QInputDialog.getInt(self, 'Параметры ряда', 'Расcтояние между посевами',
                                                self.space, 1, self.width, 1)
        if ok_pressed:
            self.space = space
            self.rebuild_row()

    def rebuild_row(self):
        pass




