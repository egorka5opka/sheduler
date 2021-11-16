from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QBrush, QPixmap, QLinearGradient, QColor
from constants import *
from PyQt5.QtCore import Qt
from PIL import Image, ImageQt


def set_picture_to_table(x, y, n, table, im_size):
    picture = QTableWidgetItem()
    if table.item(x, y):
        img = table.item(x, y).data(Qt.UserRole)[0]
    else:
        img = Image.open(f"objects/{n}.png")
    picture.setData(Qt.UserRole, (img, n))
    img = img.resize((im_size, im_size))
    picture.setBackground(QBrush(QPixmap.fromImage(ImageQt.ImageQt(img))))
    table.setItem(x, y, picture)


def get_ending(n):
    if 10 < n < 20:
        return "ов"
    n %= 10
    if n == 1:
        return ""
    if 1 < n < 5:
        return "а"
    return "ов"


def set_item_background(item, img_size):
    background = QLinearGradient(0, 0, 0, img_size)
    background.setColorAt(0, QColor("#96ff96"))
    background.setColorAt(0.4, QColor("#33b533"))
    background.setColorAt(0.7, QColor("#1d691d"))
    background.setColorAt(1, QColor("#34cf34"))
    item.setBackground(background)


def set_item_extra_background(item, size):
    background = QLinearGradient(0, 0, 0, size)
    background.setColorAt(0, QColor(LIGHT_EXTRA_COLOR))
    background.setColorAt(0.5, QColor(EXTRA_COLOR))
    background.setColorAt(0.7, QColor(DARK_EXTRA_COLOR))
    background.setColorAt(1, QColor(EXTRA_COLOR))
    item.setBackground(background)


def get_extra_gradient():
    return f"stop:0 {LIGHT_EXTRA_COLOR}, stop: 0.5 {EXTRA_COLOR},stop: 0.7 {DARK_EXTRA_COLOR},stop:1 {EXTRA_COLOR}"


def get_header_background(type):
    x2 = [0, 1, 1]
    y2 = [1, 0, 1]
    return "QHeaderView::section {" + \
        f"""background-color: qlineargradient(x1:0, y1:0, x2:{x2[type]}, y2:{y2[type]}, {get_extra_gradient()});
        color: white;
        padding-left: 4px;
        border: 1px solid {DARK_EXTRA_COLOR};""" + "}"


def get_horizontal_scroll_bar_style():
    return "QScrollBar:horizontal {"\
                f"""border: 2px solid {DARK_EXTRA_COLOR};
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop: 0 {LIGHT_EXTRA_COLOR}, stop: 1 {DARK_EXTRA_COLOR});
                height: 20px;
                margin: 0px 40px 0 0px;"""\
           "} QScrollBar::handle:horizontal {"\
                f"""background: qlineargradient(x1:0, y1:0, x2:0, y2:1, {get_extra_gradient()});
                min-width: 40px;"""\
           "} QScrollBar::add-line:horizontal {"\
                f"""background: {EXTRA_COLOR};
                width: 16px;
                subcontrol-position: right;
                subcontrol-origin: margin;
                border: 2px solid black;"""\
           "} QScrollBar::sub-line:horizontal {"\
                f"""background: {EXTRA_COLOR};
                width: 16px;
                subcontrol-position: top right;
                subcontrol-origin: margin;
                border: 2px solid black;
                position: absolute;
                right: 20px;"""\
           "} QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {"\
                f"""width: 3px;
                height: 3px;
                background: white;"""\
           "} QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {"\
                f"background: none;"\
           "}"


def get_vertical_scroll_bar_style():
    return "QScrollBar:vertical {"\
                f"""border: 2px solid {DARK_EXTRA_COLOR};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                 stop: 0 {LIGHT_EXTRA_COLOR}, stop: 1 {DARK_EXTRA_COLOR});
                width: 20px;
                margin: 40px 0px 0 0px;"""\
           "} QScrollBar::handle:vertical {"\
                f"""background: qlineargradient(x1:0, y1:0, x2:1, y2:0, {get_extra_gradient()});
                min-height: 40px;"""\
           "} QScrollBar::add-line:vertical {"\
                f"""background: {EXTRA_COLOR};
                height: 16px;
                subcontrol-position: top;
                subcontrol-origin: margin;
                border: 2px solid black;
                position: absolute;
                top: 20px;"""\
           "} QScrollBar::sub-line:vertical {"\
                f"""background: {EXTRA_COLOR};
                height: 16px;
                subcontrol-position: top;
                subcontrol-origin: margin;
                border: 2px solid black;"""\
           "} QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {"\
                f"""width: 3px;
                height: 3px;
                background: white;"""\
           "} QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {"\
                f"background: none;"\
           "}"
