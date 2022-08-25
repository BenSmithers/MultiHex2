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

        self.state_lbl = QtWidgets.QLabel(Form)
        self.state_lbl.setObjectName("state_lbl")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.state_lbl)
        self.state_display = QtWidgets.QLabel(Form)
        self.state_display.setObjectName("state_display")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.state_display)

        self.name_lbl = QtWidgets.QLabel(Form)
        self.name_lbl.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.name_lbl)
        self.name_edit = QtWidgets.QLineEdit(Form)
        self.name_edit.setObjectName("lineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.name_edit)
        self.name_shuffle = QtWidgets.QPushButton(Form)
        self.name_shuffle.setObjectName("name_shuffle")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.name_shuffle)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.addItem(spacerItem)

        self.add_to_end = QtWidgets.QPushButton(Form)
        self.add_to_end.setObjectName("add_to_end")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.add_to_end)
        self.add_to_start = QtWidgets.QPushButton(Form)
        self.add_to_start.setObjectName("add_to_start")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.add_to_start)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.name_lbl.setText(_translate("Form", "Path Name:"))
        self.name_edit.setText(_translate("Form", "New Path"))
        self.name_shuffle.setText(_translate("Form", "Shuffle Name"))
        self.state_lbl.setText(_translate("Form", "Selected: "))
        self.state_display.setText(_translate("Form", "Selecting"))
        self.add_to_start.setText(_translate("Form", "Add To Start"))
        self.add_to_end.setText(_translate("Form", "Add To End"))
        


class road_ui(Ui_Form):
    def setupUi(self, Form):
        

        self.quality_lbl = QtWidgets.QLabel(Form)
        self.quality_lbl.setObjectName("quality_lbl")
        self.quality_spin = QtWidgets.QDoubleSpinBox(Form)
        self.quality_spin.setMinimum(0.50)
        self.quality_spin.setMaximum(5.00)
        self.quality_spin.setSingleStep(0.10)
        self.quality_spin.setObjectName("quality_spin")
        
        super().setupUi(Form)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.quality_lbl)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.quality_spin)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.quality_lbl.setText(_translate("Form","Quality"))
        return super().retranslateUi(Form)
        