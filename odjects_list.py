import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QBrush
from PIL import Image, ImageQt
from showing_form import Ui_Form
from loading import LoadWidget
import sqlite3
from constants import LIST_HEADERS, WIDTH_HEADERS, SHOWING_LIST_IMAGE_SIZE as IMG_SIZE
from methods import set_picture_to_table, get_ending


class ObjectList(QMainWindow, Ui_Form):
    def __init__(self, parent_form=None):
        super().__init__()
        self.parent_form = parent_form
        self.setupUi(self)
        self.setMinimumSize(self.size())

        self.lbl = QLabel(self)
        self.lbl.setGeometry(20, 200, 100, 100)

        self.current_type = "Все"

        self.object_list.setColumnCount(len(LIST_HEADERS))
        self.object_list.setHorizontalHeaderLabels(LIST_HEADERS)
        for i in range(len(WIDTH_HEADERS)):
            self.object_list.setColumnWidth(i, WIDTH_HEADERS[i] * self.size().width() // 100)
        self.load_btn.clicked.connect(self.upload_object)
        self.connection = sqlite3.connect("objects_db.db")

        self.update_list()
        self.update_btn.clicked.connect(self.update_list)
        self.update_btn.setToolTip("F5")

        self.delete_btn.clicked.connect(self.delete_object)
        self.delete_btn.setToolTip("Delete")

        db_cursor = self.connection.cursor()
        types = db_cursor.execute("SELECT type FROM types ORDER BY type").fetchall()
        self.types.addItem("Все")
        for t in types:
            self.types.addItem(t[0])
        self.types.activated[str].connect(self.item_changed)

    def delete_object(self):
        selected = list(set([i.row() for i in self.object_list.selectedItems()]))
        selected = [self.object_list.item(i, 0).data(Qt.UserRole)[1] for i in selected]
        if not selected:
            self.statusBar().showMessage("Не выбран ни один объект")
            return
        self.statusBar().showMessage("")
        count = len(selected)
        accepted = QMessageBox.question(self, "Подтверждение удаления",
                                        f"Удалить {count} элемент{get_ending(count)}?",
                                        QMessageBox.Yes, QMessageBox.No)
        if accepted != QMessageBox.Yes:
            return
        db_cursor = self.connection.cursor()
        query = f"DELETE FROM objects WHERE id IN ({', '.join(map(str, selected))})"
        db_cursor.execute(query).fetchall()
        self.connection.commit()
        self.update_list()
        if self.parent_form:
            self.parent_form.update_list()

    def upload_object(self):
        self.loading = LoadWidget([self.parent_form, self])
        self.loading.show()

    def update_list(self):
        db_cursor = self.connection.cursor()
        query = ""
        if self.current_type == "Все":
            query = "SELECT objects.id, objects.name, types.type FROM objects\
             LEFT JOIN types ON objects.type == types.id"
        else:
            query = f"SELECT objects.id, objects.name, types.type FROM objects\
             LEFT JOIN types ON objects.type == types.id WHERE types.type == '{self.current_type}'"
        result = db_cursor.execute(query).fetchall()
        search = self.name_search.text().lower()
        if search:
            result = filter(lambda e: search in str(e[1]).lower(), result)
        for i, row in enumerate(result):
            self.object_list.setRowCount(i + 1)
            set_picture_to_table(i, 0, row[0], self.object_list, IMG_SIZE)
            self.object_list.setItem(i, 1, QTableWidgetItem(row[1]))
            self.object_list.setItem(i, 2, QTableWidgetItem(row[2]))
            self.object_list.setRowHeight(i, IMG_SIZE)

    def resizeEvent(self, event):
        self.object_list.resize(self.size().width(), self.size().height() - self.object_list.y())
        self.object_list.setColumnWidth(0, IMG_SIZE)
        left_size = self.size().width() - IMG_SIZE
        for i in range(len(WIDTH_HEADERS)):
            self.object_list.setColumnWidth(i + 1, WIDTH_HEADERS[i] * left_size // 100)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5 or event.key() == Qt.Key_Return:
            self.update_list()
        elif event.key() == Qt.Key_Delete:
            self.delete_object()

    def item_changed(self, text):
        self.current_type = text
        self.update_list()

    def closeEvent(self, event):
        db_cursor = self.connection.cursor()
        types = db_cursor.execute("SELECT id FROM types").fetchall()
        for t in types:
            cnt_type = db_cursor.execute(f"SELECT COUNT(id) FROM objects WHERE type == {t[0]}").fetchone()[0]
            if not cnt_type:
                db_cursor.execute(f"DELETE FROM types WHERE id == {t[0]}")
        self.connection.commit()
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ObjectList()
    ex.show()
    sys.exit(app.exec())
