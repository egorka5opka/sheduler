import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QIcon
import sqlite3
import csv
from main_form import Ui_MainWindow
from odjects_list import ObjectList
from loading import LoadWidget
from constants import *
from methods import *


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.showing = None
        self.connection = sqlite3.connect("objects_db.db")
        self.current_type = "Все"
        self.selected_obj = -1
        self.cell_size = self.cell_size_edit.value()
        self.rubber = False
        self.text_mode = False
        self.file_name = None
        self.saved = True

        self.show_list_action.triggered.connect(self.show_object_list)
        self.load_action.triggered.connect(self.upload_object)
        self.create_action.triggered.connect(self.create_flowerbed)
        self.open_action.triggered.connect(self.open_flowerbed)
        self.save_action.triggered.connect(self.save_flowerbed)
        self.save_as_action.triggered.connect(self.save_flowerbed_as)
        self.setMinimumSize(self.flowerbed.x() + 1, self.flowerbed.y() + 1)
        self.name_search.textEdited.connect(self.update_list)
        self.rubber_btn.clicked.connect(self.rubber_click)
        self.mode_btn.clicked.connect(self.text_mode_click)

        self.obj_list.setColumnCount(len(LIST_HEADERS_MAIN))
        self.obj_list.setHorizontalHeaderLabels(LIST_HEADERS_MAIN)

        db_cursor = self.connection.cursor()
        types = db_cursor.execute("SELECT type FROM types ORDER BY type").fetchall()
        self.types.addItem("Все")
        self.types.setItemData(0, QBrush(QColor(INTERACTION_COLOR)), Qt.BackgroundRole)
        for t in range(len(types)):
            self.types.addItem(types[t][0])
            self.types.setItemData(t + 1, QBrush(QColor(INTERACTION_COLOR)), Qt.BackgroundRole)
        self.types.activated[str].connect(self.item_changed)

        self.width_edit.editingFinished.connect(self.rebuild_flowerbed)
        self.height_edit.editingFinished.connect(self.rebuild_flowerbed)
        self.cell_size_edit.valueChanged.connect(self.rebuild_flowerbed)
        self.obj_list.cellClicked.connect(self.choose_object)
        self.flowerbed.cellClicked.connect(self.choose_cell)

        self.update_list()
        self.create_flowerbed()
        self.customize_elements()

    def customize_elements(self):
        interact_css = f"""border: 2px solid {DARK_MAIN_COLOR};
                        border-radius: 5px;
                        background: {INTERACTION_COLOR};
                        padding: 1px 5px 1px 5px;
                        min-width: 50px;"""
        self.setStyleSheet("QMainWindow {"
                                f"background: {MAIN_COLOR};"
                           "}"
                           "QPushButton {" + interact_css + "}"
                           "QLineEdit {" + interact_css + "}"
                           "QSpinBox {"
                                f"background: {INTERACTION_COLOR};"
                                "padding-right: 15px;"
                                f"border: 3px solid {DARK_MAIN_COLOR};"
                                "border-radius: 5px"
                           "}"
                           "QDialog { background: " + MAIN_COLOR + "}"
                           "QComboBox {" + interact_css + "}" +
                           get_horizontal_scroll_bar_style() + get_vertical_scroll_bar_style())
        self.setWindowIcon(QIcon("customizing/icon.png"))
        self.flowerbed.setStyleSheet(f"background: {MAIN_COLOR};"
                                     f"gridline-color: {EXTRA_COLOR}")
        self.flowerbed.horizontalHeader().setStyleSheet(get_header_background(0))
        self.flowerbed.verticalHeader().setStyleSheet(get_header_background(1))

        self.obj_list.setStyleSheet(f"background: {MAIN_COLOR};"
                                    f"gridline-color: {EXTRA_COLOR}")
        self.menubar.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
                                   f" {get_extra_gradient()}); color: white;")
        groove_background = f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {LIGHT_MAIN_COLOR}," \
                            f" stop:1 {DARK_MAIN_COLOR})"
        self.cell_size_edit.setStyleSheet("QSlider::groove:horizontal {"
                                          f"border: 1px solid {DARK_MAIN_COLOR};"
                                          "height: 8px;"
                                          f"background: {groove_background};"
                                          "margin: 2px 0;"
                                          "}"
                                          "QSlider::handle:horizontal {"
                                          f"background: {INTERACTION_COLOR};"
                                          f"border: 1px solid {DARK_MAIN_COLOR};"
                                          "width: 18px;"
                                          "margin: -3px 3;"
                                          "border-radius: 3px;"
                                          "}")
        self.corner_widget = QWidget(self)
        self.corner_widget.setStyleSheet(f"""background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
         stop: 0 {LIGHT_EXTRA_COLOR}, stop: 0.85 {DARK_EXTRA_COLOR});""")
        self.flowerbed.horizontalHeader().setMaximumSize(16777215, 30)
        self.flowerbed.horizontalHeader().setMinimumSize(0, 30)
        self.flowerbed.verticalHeader().setMaximumSize(30, 16777215)
        self.flowerbed.verticalHeader().setMinimumSize(30, 0)
        self.corner_widget.setGeometry(311, 57,
                                       self.flowerbed.verticalHeader().width(),
                                       self.flowerbed.horizontalHeader().height())

        for t in range(self.types.count()):
            self.types.setItemData(t, QBrush(QColor(INTERACTION_COLOR)), Qt.BackgroundRole)

    def choose_object(self):
        if self.rubber:
            self.rubber_click()
        chose = self.obj_list.currentRow()
        if chose == self.selected_obj:
            self.obj_list.item(chose, 1).setBackground(QColor(MAIN_COLOR))
            self.selected_obj = -1
            return
        if self.obj_list.item(chose, 1).data(Qt.UserRole) == TYPE_ROLE:
            if self.selected_obj != -1:
                self.obj_list.item(self.selected_obj, 1).setBackground(QColor(MAIN_COLOR))
            self.selected_obj = -1
            return
        self.obj_list.item(chose, 1).setBackground(QColor(SELECTION_COLOR))
        if self.selected_obj != -1:
            self.obj_list.item(self.selected_obj, 1).setBackground(QColor(MAIN_COLOR))
        self.selected_obj = chose

    def text_mode_click(self):
        self.text_mode = not self.text_mode
        if self.text_mode:
            self.mode_btn.setStyleSheet(f"background: {BTN_CLICKED_COLOR};")
        else:
            self.mode_btn.setStyleSheet(f"background: {INTERACTION_COLOR};")
        self.rebuild_flowerbed()

    def choose_cell(self):
        x = self.flowerbed.currentRow()
        y = self.flowerbed.currentColumn()
        self.flowerbed.clearSelection()
        if self.rubber:
            self.flowerbed.setItem(x, y, None)
            return
        if self.selected_obj != -1:
            obj = self.obj_list.item(self.selected_obj, 0).data(Qt.UserRole)[1]
            self.flowerbed.setItem(x, y, None)
            self.set_object(x, y, obj)

    def set_object(self, x, y, obj):
        self.saved = False
        set_picture_to_table(x, y, obj, self.flowerbed, self.cell_size)
        self.flowerbed.item(x, y).setText("")
        if self.text_mode:
            self.flowerbed.item(x, y).setBackground(QBrush())
            self.flowerbed.item(x, y).setText(self.objects[self.flowerbed.item(x, y).data(Qt.UserRole)[1]])

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
        for i in range(height):
            for j in range(width):
                if not self.flowerbed.item(i, j):
                    continue
                obj = self.flowerbed.item(i, j).data(Qt.UserRole)[1]
                self.set_object(i, j, obj)

    def rubber_click(self):
        self.rubber = not self.rubber
        if self.rubber:
            self.rubber_btn.setStyleSheet(f"background: {BTN_CLICKED_COLOR};")
        else:
            self.rubber_btn.setStyleSheet(f"background: {INTERACTION_COLOR};")

    def update_list(self):
        db_cursor = self.connection.cursor()

        id_and_objects = db_cursor.execute("SELECT id, name from objects").fetchall()
        self.objects = dict()
        for i, o in id_and_objects:
            self.objects[int(i)] = o

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
            color = QColor(EXTRA_COLOR)
            self.obj_list.setItem(i, 0, QTableWidgetItem())
            type_item = QTableWidgetItem(t)
            type_item.setForeground(QBrush(QColor(Qt.white)))
            type_item.setData(Qt.UserRole, TYPE_ROLE)
            self.obj_list.setItem(i, 1, type_item)
            self.obj_list.setRowHeight(i, 30)
            set_item_extra_background(self.obj_list.item(i, 0), self.obj_list.rowHeight(i))
            set_item_extra_background(self.obj_list.item(i, 1), self.obj_list.rowHeight(i))
            vert_headers += [""]
            for row in result:
                i = self.obj_list.rowCount()
                self.obj_list.setRowCount(i + 1)
                set_picture_to_table(i, 0, row[0], self.obj_list, MAIN_SHOWING_IMAGE_SIZE)
                self.obj_list.setItem(i, 1, QTableWidgetItem(row[1]))
                set_item_background(self.obj_list.item(i, 1), MAIN_SHOWING_IMAGE_SIZE)
                self.obj_list.setRowHeight(i, MAIN_SHOWING_IMAGE_SIZE)
                if vert_headers[-1]:
                    vert_headers += [str(int(vert_headers[-1]) + 1)]
                else:
                    vert_headers += ["1"]
            self.obj_list.setColumnWidth(0, MAIN_SHOWING_IMAGE_SIZE)
            left_width = self.verticalLayoutWidget.width() - MAIN_SHOWING_IMAGE_SIZE - 22
            self.obj_list.setColumnWidth(1, left_width)
        self.obj_list.setVerticalHeaderLabels(vert_headers)

    def show_object_list(self):
        self.showing = ObjectList(self)
        self.showing.show()

    def upload_object(self):
        self.loading = LoadWidget([self, self.showing])
        self.loading.show()

    def ask_for_saving(self):
        quest = QMessageBox(self)
        quest.setText("Сохранинть последние изменения?")
        quest.setWindowTitle("Сохранине")
        quest.addButton(QMessageBox.Yes)
        quest.addButton(QMessageBox.No)
        quest.addButton(QMessageBox.Cancel)
        return quest.exec()

    def create_flowerbed(self):
        if not self.saved:
            acception = self.ask_for_saving()
            if acception == QMessageBox.Yes:
                self.save_flowerbed()
            elif acception != QMessageBox.No:
                return -1
        self.flowerbed.setColumnCount(0)
        self.flowerbed.setRowCount(0)
        self.rebuild_flowerbed()
        self.saved = True
        self.file_name = None

    def open_flowerbed(self):
        res = self.create_flowerbed()
        if res == -1:
            return
        self.file_name = QFileDialog.getOpenFileName(self, 'Открытие файла', '', "Клумба (*.fwb)")[0]
        file = open(self.file_name, "r")
        reader = csv.reader(file, delimiter=";", quotechar='"')
        header = reader.__next__()
        if len(header) != 4 or header[0] != FLOWERBED_FILE:
            self.statusbar.showMessage("Не удалось открыть файл")
            return
        try:
            h, w, size = map(int, header[1:])
        except Exception:
            self.statusbar.showMessage("Не удалось открыть файл")
            return
        self.width_edit.setValue(w)
        self.height_edit.setValue(h)
        self.cell_size = size
        self.cell_size_edit.setValue(size)
        fwb = list(reader)
        for i in range(h):
            for j in range(w):
                if fwb[i][j] != "None":
                    self.set_object(i, j, int(fwb[i][j]))
        self.saved = True
        self.statusbar.showMessage(self.file_name.split("/")[-1])

    def save_flowerbed(self):
        if not self.file_name:
            fname, ok_pressed = QFileDialog.getSaveFileName(self, 'Сохранение файла', '', "Клумба (*.fwb)")
            if not ok_pressed:
                return
            self.file_name = fname
        self.saved = True
        file = open(self.file_name, "w", newline="")
        writer = csv.writer(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([FLOWERBED_FILE, self.flowerbed.rowCount(), self.flowerbed.columnCount(), self.cell_size])
        for i in range(self.flowerbed.rowCount()):
            row = []
            for j in range(self.flowerbed.columnCount()):
                if self.flowerbed.item(i, j):
                    row.append(self.flowerbed.item(i, j).data(Qt.UserRole)[1])
                else:
                    row.append("None")
            writer.writerow(row)
        file.close()
        self.statusbar.showMessage(self.file_name.split("/")[-1])

    def save_flowerbed_as(self):
        fname, ok_pressed = QFileDialog.getSaveFileName(self, 'Сохранение файла', '', "Клумба (*.fwb)")
        if not ok_pressed:
            return
        self.file_name = fname
        self.save_flowerbed()

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
        self.flowerbed.resize(self.centralwidget.width() - self.flowerbed.x(),
                              self.centralWidget().height() - self.flowerbed.y() - 4)
        self.verticalLayoutWidget.resize(self.verticalLayoutWidget.width(),
                                         self.centralWidget().height() - self.verticalLayoutWidget.y() - 4)

    def closeEvent(self, event):
        self.connection.close()
        if not self.saved:
            do_save = self.ask_for_saving()
            if do_save == QMessageBox.Yes:
                self.save_flowerbed()
                event.accept()
            elif do_save == QMessageBox.No:
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    exit(app.exec())
