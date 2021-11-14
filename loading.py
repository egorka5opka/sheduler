import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QFileDialog, QLineEdit,\
    QMessageBox, QComboBox
from PyQt5.QtWidgets import QPushButton
from PIL import Image
from PIL.ImageQt import ImageQt
import sqlite3
from constants import NEW_TYPE, LOAD_SCREEN_SIZE, LOAD_IMAGE_SIZE, MAIN_COLOR, INTERACTION_COLOR, DARK_MAIN_COLOR


class LoadWidget(QWidget):
    def __init__(self, parents=[None]):
        super().__init__()
        self.init_ui()
        self.im = None
        self.parents = parents

    def init_ui(self):
        self.setGeometry(400, 400, *LOAD_SCREEN_SIZE)
        self.setWindowTitle('Создание объекта')
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())
        self.setStyleSheet("background: " + MAIN_COLOR)

        self.image_lbl = QLabel(self)
        self.image_lbl.move(10, 10)
        self.image_lbl.resize(*LOAD_IMAGE_SIZE)

        self.load_btn = QPushButton("Загрузить", self)
        self.load_btn.setGeometry(270, 10, 200, 30)
        self.load_btn.clicked.connect(self.load_picture)
        self.load_btn.setStyleSheet("QPushButton {"
                                    f"border: 2px solid {DARK_MAIN_COLOR};"
                                    "border-radius: 5px;"
                                    f"background: {INTERACTION_COLOR};"
                                    "}")

        self.lbl1 = QLabel("Введите название:", self)
        self.lbl1.setGeometry(270, 50, 200, 20)
        self.name_edit = QLineEdit(self)
        self.name_edit.setGeometry(270, 70, 200, 30)
        self.name_edit.setStyleSheet("QLineEdit {"
                                     f"border: 2px solid {DARK_MAIN_COLOR};"
                                     "border-radius: 5px;"
                                     f"background: {INTERACTION_COLOR};"
                                     "}")

        self.lbl2 = QLabel("Выберите тип (для сортировки): ", self)
        self.lbl2.setGeometry(270, 110, 200, 20)
        self.types = QComboBox(self)
        self.types.setGeometry(270, 130, 200, 30)
        self.types.setEditable(True)
        connection = sqlite3.connect("objects_db.db")
        db_cursor = connection.cursor()
        types = db_cursor.execute("SELECT type FROM types").fetchall()
        self.types.addItem("Новый тип")
        for t in types:
            self.types.addItem(t[0])
        self.types.activated[str].connect(self.item_changed)
        self.types.setStyleSheet("QComboBox {"
                                 f"border: 2px solid {DARK_MAIN_COLOR};"
                                 "border-radius: 5px;"
                                 f"background-color: {INTERACTION_COLOR};"
                                 "}")
        self.types.setEditable(False)
        self.type = NEW_TYPE

        self.lbl3 = QLabel("Введите новый тип:", self)
        self.lbl3.setGeometry(270, 170, 200, 20)
        self.type_edit = QLineEdit(self)
        self.type_edit.setGeometry(270, 190, 200, 30)
        self.type_edit.setStyleSheet("QLineEdit {"
                                     f"border: 2px solid {DARK_MAIN_COLOR};"
                                     "border-radius: 5px;"
                                     f"background: {INTERACTION_COLOR};"
                                     "}")

        self.save_btn = QPushButton("Сохранить", self)
        self.save_btn.setGeometry(10, 280, 460, 40)
        self.save_btn.clicked.connect(self.save_object)
        self.save_btn.setStyleSheet("QPushButton {"
                                    f"border: 2px solid {DARK_MAIN_COLOR};"
                                    "border-radius: 5px;"
                                    f"background: {INTERACTION_COLOR};"
                                    "}")
        self.status_lbl = QLabel(self)
        self.status_lbl.setGeometry(270, 260, 200, 20)

    def load_picture(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', "")[0]
        if not fname:
            return
        try:
            self.im = Image.open(fname)
            self.im = self.im.convert("RGBA")
            size = min(self.im.size)
            dif_x = (self.im.size[0] - size) // 2
            dif_y = (self.im.size[1] - size) // 2
            self.im = self.im.crop((dif_x, dif_y, dif_x + size, dif_y + size))
            self.im = self.im.resize((250, 250))
            self.image_lbl.setPixmap(QPixmap.fromImage(ImageQt(self.im)))
        except Exception:
            self.status_lbl.setText("Непредвиденная ошибка при откртии файла")

    def save_object(self):
        if not self.im:
            self.status_lbl.setText("Загрузите изображение объекта")
            return
        name = self.name_edit.text().strip()
        type = self.type
        if type == NEW_TYPE:
            type = self.type_edit.text().lower().strip()
            type = type[0].upper() + type[1:]
            for p in self.parents:
                if p:
                    p.types.addItem(type)
        elif type == "Все" or type == NEW_TYPE:
            self.status_lbl.setText("Недопустимое название типа")
            return
        connection = sqlite3.connect("objects_db.db")
        cursor = connection.cursor()
        have_type = cursor.execute(f"SELECT id FROM types where type == '{type}'").fetchone()
        if not have_type:
            cursor.execute(f"INSERT INTO types (type) VALUES ('{type}')")
            have_type = cursor.execute(f"SELECT id FROM types where type == '{type}'").fetchone()

        type_id = have_type[0]
        same = cursor.execute(f"SELECT id FROM objects WHERE name == '{name}' AND type == '{type_id}'").fetchone()
        if same:
            acception = QMessageBox.question(self, "Подтверждение",
                                    "Уже существует объект с таким именем и типом. Создать ещё один?",
                                    QMessageBox.Yes, QMessageBox.No)
            if acception == QMessageBox.No:
                connection.close()
                return
        idexec = cursor.execute("SELECT MAX(id) FROM objects").fetchone()
        id = 1
        if idexec[0]:
            id = idexec[0] + 1
        cursor.execute(f"INSERT INTO objects (id, name, type) VALUES ({id}, '{name}', {type_id})")
        connection.commit()
        connection.close()
        self.im.save(f"objects/{id}.png")
        self.close()
        for p in self.parents:
            if p:
                p.update_list()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.save_object()

    def item_changed(self, text):
        self.type = text
        if text != NEW_TYPE:
            self.lbl3.setVisible(False)
            self.type_edit.setVisible(False)
        else:
            self.lbl3.setVisible(True)
            self.type_edit.setVisible(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoadWidget()
    ex.show()
    sys.exit(app.exec())
