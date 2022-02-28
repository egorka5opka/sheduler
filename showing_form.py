# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'showing_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(932, 510)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 931, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.load_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.load_btn.setMinimumSize(QtCore.QSize(0, 28))
        self.load_btn.setObjectName("load_btn")
        self.horizontalLayout.addWidget(self.load_btn)
        self.delete_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.delete_btn.setMinimumSize(QtCore.QSize(0, 28))
        self.delete_btn.setObjectName("delete_btn")
        self.horizontalLayout.addWidget(self.delete_btn)
        self.update_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.update_btn.setMinimumSize(QtCore.QSize(0, 28))
        self.update_btn.setObjectName("update_btn")
        self.horizontalLayout.addWidget(self.update_btn)
        self.types = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.types.setMinimumSize(QtCore.QSize(0, 0))
        self.types.setObjectName("types")
        self.horizontalLayout.addWidget(self.types)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.name_search = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.name_search.setMinimumSize(QtCore.QSize(0, 24))
        self.name_search.setMaximumSize(QtCore.QSize(100, 16777215))
        self.name_search.setObjectName("name_search")
        self.horizontalLayout.addWidget(self.name_search)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(53, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.min_height_box = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.min_height_box.setMaximumSize(QtCore.QSize(70, 16777215))
        self.min_height_box.setMaximum(10000)
        self.min_height_box.setObjectName("min_height_box")
        self.horizontalLayout.addWidget(self.min_height_box)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(10, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.max_height_box = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.max_height_box.setMaximumSize(QtCore.QSize(70, 16777215))
        self.max_height_box.setMaximum(10000)
        self.max_height_box.setProperty("value", 10000)
        self.max_height_box.setObjectName("max_height_box")
        self.horizontalLayout.addWidget(self.max_height_box)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.period_edit = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.period_edit.setObjectName("period_edit")
        self.horizontalLayout.addWidget(self.period_edit)
        self.object_list = QtWidgets.QTableWidget(Form)
        self.object_list.setGeometry(QtCore.QRect(0, 50, 933, 461))
        self.object_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.object_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.object_list.setCornerButtonEnabled(True)
        self.object_list.setObjectName("object_list")
        self.object_list.setColumnCount(0)
        self.object_list.setRowCount(0)
        self.object_list.verticalHeader().setVisible(False)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Список объектов"))
        self.load_btn.setText(_translate("Form", "Загрузить"))
        self.delete_btn.setText(_translate("Form", "Удалить"))
        self.update_btn.setText(_translate("Form", "Обновить"))
        self.label.setText(_translate("Form", "По имени:"))
        self.label_2.setText(_translate("Form", "Высота:"))
        self.label_3.setText(_translate("Form", "-"))
        self.label_4.setText(_translate("Form", "Период:"))
