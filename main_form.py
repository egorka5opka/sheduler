# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1055, 684)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 311, 631))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vertical_menu = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_menu.setContentsMargins(0, 0, 0, 0)
        self.vertical_menu.setSpacing(3)
        self.vertical_menu.setObjectName("vertical_menu")
        self.types = QtWidgets.QComboBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.types.sizePolicy().hasHeightForWidth())
        self.types.setSizePolicy(sizePolicy)
        self.types.setMinimumSize(QtCore.QSize(0, 30))
        self.types.setObjectName("types")
        self.vertical_menu.addWidget(self.types)
        self.name_search = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.name_search.setReadOnly(False)
        self.name_search.setObjectName("name_search")
        self.vertical_menu.addWidget(self.name_search)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.min_height_box = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.min_height_box.setMaximum(200)
        self.min_height_box.setObjectName("min_height_box")
        self.horizontalLayout.addWidget(self.min_height_box)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setMaximumSize(QtCore.QSize(15, 16777215))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.max_height_box = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.max_height_box.setMaximum(200)
        self.max_height_box.setSingleStep(1)
        self.max_height_box.setProperty("value", 200)
        self.max_height_box.setObjectName("max_height_box")
        self.horizontalLayout.addWidget(self.max_height_box)
        self.vertical_menu.addLayout(self.horizontalLayout)
        self.period_edit = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.period_edit.setObjectName("period_edit")
        self.vertical_menu.addWidget(self.period_edit)
        self.obj_list = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.obj_list.setFont(font)
        self.obj_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.obj_list.setDragEnabled(True)
        self.obj_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.obj_list.setObjectName("obj_list")
        self.obj_list.setColumnCount(0)
        self.obj_list.setRowCount(0)
        self.obj_list.horizontalHeader().setVisible(False)
        self.obj_list.verticalHeader().setVisible(False)
        self.vertical_menu.addWidget(self.obj_list)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(310, 0, 741, 32))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontal_menu = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontal_menu.setContentsMargins(0, 0, 0, 0)
        self.horizontal_menu.setSpacing(1)
        self.horizontal_menu.setObjectName("horizontal_menu")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontal_menu.addWidget(self.label)
        self.bed_width_edit = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.bed_width_edit.setMaximum(2000)
        self.bed_width_edit.setProperty("value", 100)
        self.bed_width_edit.setObjectName("bed_width_edit")
        self.horizontal_menu.addWidget(self.bed_width_edit)
        self.new_row_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.new_row_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.new_row_btn.setSizeIncrement(QtCore.QSize(0, 0))
        self.new_row_btn.setObjectName("new_row_btn")
        self.horizontal_menu.addWidget(self.new_row_btn)
        self.new_row_edit = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.new_row_edit.setMaximum(0)
        self.new_row_edit.setObjectName("new_row_edit")
        self.horizontal_menu.addWidget(self.new_row_edit)
        self.mode_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.mode_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.mode_btn.setObjectName("mode_btn")
        self.horizontal_menu.addWidget(self.mode_btn)
        self.rubber_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.rubber_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.rubber_btn.setMaximumSize(QtCore.QSize(70, 16777215))
        self.rubber_btn.setObjectName("rubber_btn")
        self.horizontal_menu.addWidget(self.rubber_btn)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(310, 30, 741, 601))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.flowerbed_rows = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.flowerbed_rows.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.flowerbed_rows.setContentsMargins(0, 0, 0, 0)
        self.flowerbed_rows.setObjectName("flowerbed_rows")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1055, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.open_action = QtWidgets.QAction(MainWindow)
        self.open_action.setObjectName("open_action")
        self.create_action = QtWidgets.QAction(MainWindow)
        self.create_action.setObjectName("create_action")
        self.load_action = QtWidgets.QAction(MainWindow)
        self.load_action.setObjectName("load_action")
        self.show_list_action = QtWidgets.QAction(MainWindow)
        self.show_list_action.setObjectName("show_list_action")
        self.save_action = QtWidgets.QAction(MainWindow)
        self.save_action.setObjectName("save_action")
        self.save_as_action = QtWidgets.QAction(MainWindow)
        self.save_as_action.setObjectName("save_as_action")
        self.menu.addAction(self.open_action)
        self.menu.addAction(self.create_action)
        self.menu.addAction(self.save_action)
        self.menu.addAction(self.save_as_action)
        self.menu_2.addAction(self.load_action)
        self.menu_2.addAction(self.show_list_action)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Планировщик"))
        self.label_4.setText(_translate("MainWindow", "Высота:"))
        self.label_5.setText(_translate("MainWindow", "-"))
        self.label.setText(_translate("MainWindow", "   Ширина клумбы (см):"))
        self.new_row_btn.setText(_translate("MainWindow", "Вставить новый ряд:"))
        self.mode_btn.setText(_translate("MainWindow", "Текстовый режим"))
        self.rubber_btn.setText(_translate("MainWindow", "Ластик"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Объект"))
        self.open_action.setText(_translate("MainWindow", "Открыть (Ctrl + O)"))
        self.create_action.setText(_translate("MainWindow", "Создать (Ctrl+N)"))
        self.load_action.setText(_translate("MainWindow", "Загрузить (Ctrl+U)"))
        self.show_list_action.setText(_translate("MainWindow", "Посмотреть список"))
        self.save_action.setText(_translate("MainWindow", "Сохранить (Ctrl+S)"))
        self.save_as_action.setText(_translate("MainWindow", "Сохранить как (Ctrl+Shift+S)"))
