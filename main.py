import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPixmap, QColor
from PIL import Image, ImageQt
import sqlite3
import csv
from main_form import Ui_MainWindow
from odjects_list import ObjectList
from loading import LoadWidget
from constants import LIST_HEADERS_MAIN, MAIN_SHOWING_IMAGE_SIZE as IMG_SIZE, TYPE_ROLE
from methods import set_picture_to_table

'''
PLAN
обработать изменение размеров тблицы и ячеек        DONE
реализовать возможность помещать объекты в ячейки
сделать текстовое отображение
реализовать сохранение как
просто сохранение
открытие файлов
создание новой клумбы
конец
'''


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showing = None
        self.connection = sqlite3.connect("objects_db.db")
        self.current_type = "Все"
        self.selected_obj = -1
        self.cell_size = self.cell_size_edit.value()
        self.show_list_action.triggered.connect(self.show_object_list)
        self.load_action.triggered.connect(self.upload_object)
        self.create_action.triggered.connect(self.create_flowerbed)
        self.open_action.triggered.connect(self.open_flowerbed)
        self.save_action.triggered.connect(self.save_flowerbed)
        self.save_as_action.triggered.connect(self.save_flowerbed_as)
        self.setMinimumSize(self.flowerbed.x() + 1, self.flowerbed.y() + 1)
        self.name_search.textEdited.connect(self.update_list)

        self.obj_list.setColumnCount(len(LIST_HEADERS_MAIN))
        self.obj_list.setHorizontalHeaderLabels(LIST_HEADERS_MAIN)

        db_cursor = self.connection.cursor()
        types = db_cursor.execute("SELECT type FROM types ORDER BY type").fetchall()
        self.types.addItem("Все")
        for t in types:
            self.types.addItem(t[0])
        self.types.activated[str].connect(self.item_changed)

        self.width_edit.editingFinished.connect(self.rebuild_flowerbed)
        self.height_edit.editingFinished.connect(self.rebuild_flowerbed)
        self.cell_size_edit.valueChanged.connect(self.rebuild_flowerbed)
        self.obj_list.cellClicked.connect(self.choose_object)
        self.flowerbed.cellClicked.connect(self.choose_cell)

        self.update_list()
        self.create_flowerbed()

    def choose_object(self):
        chose = self.obj_list.currentRow()
        self.obj_list.clearSelection()
        print(chose)
        if chose == self.selected_obj or self.obj_list.item(chose, 1).data(Qt.UserRole) == TYPE_ROLE:
            self.selected_obj = -1
            return
        self.obj_list.selectRow(chose)
        self.selected_obj = chose

    def choose_cell(self):
        x = self.flowerbed.currentRow()
        y = self.flowerbed.currentColumn()
        self.flowerbed.clearSelection()
        if self.selected_obj != -1:
            self.set_object(x, y)

    def set_object(self, x, y):
        set_picture_to_table(x, y, self.obj_list.item(self.selected_obj, 0).data(Qt.UserRole),
                             self.flowerbed, self.cell_size)
        self.flowerbed.item(x, y).setData(Qt.UserRole, self.selected_obj)

    def rebuild_flowerbed(self):
        width = self.width_edit.value()
        height = self.height_edit.value()
        self.cell_size = self.cell_size_edit.value()
        self.flowerbed.setColumnCount(width)
        self.flowerbed.setRowCount(height)
        for i in range(width):
            self.flowerbed.setColumnWidth(i, self.cell_size)
        for i in range(height):
            self.flowerbed.setRowHeight(i, self.cell_size)
        for i in range(width):
            for j in range(height):
                pass

    def update_list(self):
        db_cursor = self.connection.cursor()
        self.obj_list.setRowCount(0)
        self.obj_list.clearSelection()
        if self.current_type == "Все":
            in_types = db_cursor.execute("SELECT type FROM types ORDER BY type").fetchall()
            in_types = list(map(lambda e: e[0], in_types))
        else:
            in_types = [self.current_type]
        vert_headers = []
        for t in in_types:
            query = f"SELECT objects.id, objects.name, types.type FROM objects LEFT JOIN types ON" \
                    f" types.id == objects.type WHERE types.type == '{t}' ORDER BY objects.name"
            result = list(db_cursor.execute(query).fetchall())
            search = self.name_search.text().lower()
            if search:
                result = filter(lambda e: search in str(e[1]).lower(), result)
            if not result:
                continue
            i = self.obj_list.rowCount()
            self.obj_list.setRowCount(i + 1)
            color = QColor(111, 111, 111, 111)
            self.obj_list.setItem(i, 0, QTableWidgetItem())
            self.obj_list.item(i, 0).setBackground(color)
            type_item = QTableWidgetItem(t)
            type_item.setBackground(color)
            type_item.setData(Qt.UserRole, TYPE_ROLE)
            self.obj_list.setItem(i, 1, type_item)
            self.obj_list.setRowHeight(i, 30)
            vert_headers += [""]
            for row in result:
                i = self.obj_list.rowCount()
                self.obj_list.setRowCount(i + 1)
                set_picture_to_table(i, 0, row[0], self.obj_list, IMG_SIZE)
                self.obj_list.item(i, 0).setData(Qt.UserRole, row[0])
                self.obj_list.setItem(i, 1, QTableWidgetItem(row[1]))
                self.obj_list.setRowHeight(i, IMG_SIZE)
                if vert_headers[-1]:
                    vert_headers += [str(int(vert_headers[-1]) + 1)]
                else:
                    vert_headers += ["1"]
            self.obj_list.setColumnWidth(0, IMG_SIZE)
            left_width = self.verticalLayoutWidget.width() - IMG_SIZE - 2
            self.obj_list.setColumnWidth(1, left_width)
        self.obj_list.setVerticalHeaderLabels(vert_headers)

    def show_object_list(self):
        self.showing = ObjectList(self)
        self.showing.show()

    def upload_object(self):
        self.loading = LoadWidget([self, self.showing])
        self.loading.show()

    def create_flowerbed(self):
        self.rebuild_flowerbed()
        print("create")

    def open_flowerbed(self):
        print("open")

    def save_flowerbed(self):
        print("save")

    def save_flowerbed_as(self):
        print("save_as")

    def item_changed(self, text):
        self.current_type = text
        self.update_list()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_O:
                self.open_flowerbed()
            elif event.key() == Qt.Key_S:
                self.save_flowerbed()
            elif event.key() == Qt.Key_N:
                self.create_flowerbed()
            elif event.key() == Qt.Key_U:
                self.upload_object()
        elif int(event.modifiers()) == (Qt.ControlModifier + Qt.ShiftModifier):
            if event.key() == Qt.Key_S:
                self.save_flowerbed_as()

    def resizeEvent(self, event):
        self.flowerbed.resize(self.centralwidget.width() - self.flowerbed.x() + 1,
                              self.centralWidget().height() - self.flowerbed.y() + 1)
        self.verticalLayoutWidget.resize(self.verticalLayoutWidget.width(),
                                         self.centralWidget().height() - self.verticalLayoutWidget.y() + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    exit(app.exec())
