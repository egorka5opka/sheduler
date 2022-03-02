import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QLinearGradient, QIcon
from showing_form import Ui_Form
from loading import LoadWidget
import sqlite3
from constants import *
from methods import *


class ObjectList(QMainWindow, Ui_Form):
    def __init__(self, parent_form=None):
        super().__init__()
        self.parent_form = parent_form
        self.setupUi(self)
        self.setMinimumSize(self.size())

        self.lbl = QLabel(self)
        self.lbl.setGeometry(20, 200, 100, 100)

        self.current_type = "Все"
        self.period = 'Все'

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
        self.name_search.textEdited.connect(self.update_list)
        self.min_height_box.valueChanged.connect(self.update_list)
        self.max_height_box.valueChanged.connect(self.update_list)

        db_cursor = self.connection.cursor()
        types = db_cursor.execute("SELECT type FROM types ORDER BY type").fetchall()
        self.types.addItem("Все")
        self.types.setItemData(0, QBrush(QColor(INTERACTION_COLOR)), Qt.BackgroundRole)
        for t in range(len(types)):
            self.types.addItem(types[t][0])
            self.types.setItemData(t + 1, QBrush(QColor(INTERACTION_COLOR)), Qt.BackgroundRole)
        self.types.activated[str].connect(self.item_changed)

        periods = db_cursor.execute("SELECT period from periods").fetchall()
        self.period_edit.addItem("Все")
        self.period_edit.setItemData(0, QBrush(QColor(INTERACTION_COLOR)), Qt.BackgroundRole)
        for p in range(len(periods)):
            self.period_edit.addItem(periods[p][0])
            self.period_edit.setItemData(p + 1, QBrush(QColor(INTERACTION_COLOR)), Qt.BackgroundRole)
        self.period_edit.activated[str].connect(self.period_item_changed)

        self.customize_elements()

    def customize_elements(self):
        interact_css = f"""border: 2px solid {DARK_MAIN_COLOR};
                                border-radius: 5px;
                                background: {INTERACTION_COLOR};
                                padding: 1px 5px 1px 5px;
                                min-width: 60px;"""

        self.setStyleSheet("QMainWindow {"
                           f"background: {MAIN_COLOR};"
                           "}"
                           "QPushButton {" + interact_css + "}"
                           "QLineEdit {" + interact_css + "}"
                           "QDialog { background: " + MAIN_COLOR + "}"
                           "QComboBox {" + interact_css + "} " +
                           get_horizontal_scroll_bar_style() + get_vertical_scroll_bar_style() +
                           "QSpinBox {"
                           f"background: {INTERACTION_COLOR};"
                           "padding-right: 15px;"
                           f"border: 3px solid {DARK_MAIN_COLOR};"
                           "border-radius: 5px"
                           "}")
        self.object_list.setStyleSheet(f"background: {MAIN_COLOR};"
                                       f"selection-background-color: {SELECTION_COLOR};"
                                       f"gridline-color: {EXTRA_COLOR};"
                                       "color: black;"
                                       "font-size: 18px;"
                                       "font-weight: bold;"
                                       "text-align: center;")

        for t in range(self.types.count()):
            self.types.setItemData(t, QBrush(QColor(INTERACTION_COLOR)), Qt.BackgroundRole)

        self.object_list.horizontalHeader().setStyleSheet(get_header_background(0))
        self.corner_widget = QWidget(self)
        self.corner_widget.resize(20, 20)
        self.corner_widget.setStyleSheet(f"background: {DARK_EXTRA_COLOR}")

        self.setWindowIcon(QIcon("customizing/icon.png"))

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
        query = f"SELECT objects.id, objects.name, types.type, objects.height, periods.period FROM objects\
             LEFT JOIN types ON objects.type == types.id LEFT JOIN periods ON objects.flowering == periods.id \
             WHERE {self.min_height_box.value()} <= objects.height AND objects.height <= {self.max_height_box.value()}"
        if self.current_type != 'Все':
            query += f" AND objects.type in (SELECT types.id FROM types WHERE types.type == '{self.current_type}')"
        if self.period != 'Все':
            query += f" AND objects.flowering in (SELECT id FROM periods WHERE period == '{self.period}')"
        result = db_cursor.execute(query).fetchall()
        search = self.name_search.text().lower()
        if search:
            result = filter(lambda e: search in str(e[1]).lower(), result)
            self.name_search.setStyleSheet(f"background: {SELECTION_COLOR}")
        else:
            self.name_search.setStyleSheet(f"background: {INTERACTION_COLOR}")
        self.object_list.setRowCount(0)
        for i, row in enumerate(result):
            self.object_list.setRowCount(i + 1)
            set_picture_to_table(i, 0, row[0], self.object_list, SHOWING_LIST_IMAGE_SIZE, update=True)
            for j in range(len(LIST_HEADERS) - 1):
                self.object_list.setItem(i, j + 1, QTableWidgetItem(str(row[j + 1])))
                set_item_background(self.object_list.item(i, j + 1), SHOWING_LIST_IMAGE_SIZE)
            self.object_list.setRowHeight(i, SHOWING_LIST_IMAGE_SIZE)

    def resizeEvent(self, event):
        self.object_list.resize(self.size().width(), self.size().height() - self.object_list.y())
        self.object_list.setColumnWidth(0, SHOWING_LIST_IMAGE_SIZE)
        left_size = self.size().width() - SHOWING_LIST_IMAGE_SIZE - 23
        for i in range(len(WIDTH_HEADERS)):
            self.object_list.setColumnWidth(i + 1, WIDTH_HEADERS[i] * left_size // 100)
        self.corner_widget.move(self.width() - 21, self.height() - 21)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.update_list()
        elif event.key() == Qt.Key_Delete:
            self.delete_object()

    def item_changed(self, text):
        self.current_type = text
        self.update_list()

    def period_item_changed(self, text):
        self.period = text
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
    app.exec()

