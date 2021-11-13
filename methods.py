from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QBrush, QPixmap
from PIL import Image, ImageQt


def set_picture_to_table(x, y, n, table, im_size):
    picture = QTableWidgetItem()
    img = Image.open(f"objects/{n}.png")
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