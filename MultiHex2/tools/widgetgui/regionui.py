# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'region.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.name_lbl = QtWidgets.QLabel(Form)
        self.name_lbl.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.name_lbl)
        self.name_edit = QtWidgets.QLineEdit(Form)
        self.name_edit.setObjectName("lineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.name_edit)
        self.new_name_button = QtWidgets.QPushButton(Form)
        self.new_name_button.setObjectName("pushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.new_name_button)
        self.color_choice_button = QtWidgets.QPushButton(Form)
        self.color_choice_button.setText("")
        self.color_choice_button.setObjectName("pushButton_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.color_choice_button)
        self.apply_button = QtWidgets.QPushButton(Form)
        self.apply_button.setObjectName("pushButton_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.apply_button)
        self.delete_button = QtWidgets.QPushButton(Form)
        self.delete_button.setObjectName("pushButton_4")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.delete_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.name_lbl.setText(_translate("Form", "Biome"))
        self.name_edit.setText(_translate("Form", "biome_name"))
        self.new_name_button.setText(_translate("Form", "Generate New Name"))
        self.apply_button.setText(_translate("Form", "Apply"))
        self.delete_button.setText(_translate("Form", "Delete"))
        self.label_2.setText(_translate("Form", "Color:"))
