# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hex_select_widg.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class hex_select_gui(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(456, 358)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.geo_lbl = QtWidgets.QLabel(Form)
        self.geo_lbl.setObjectName("geo_lbl")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.geo_lbl)
        self.geo_disp = QtWidgets.QLabel(Form)
        self.geo_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.geo_disp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.geo_disp.setAlignment(QtCore.Qt.AlignCenter)
        self.geo_disp.setObjectName("geo_disp")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.geo_disp)
        self.props_lbl = QtWidgets.QLabel(Form)
        self.props_lbl.setObjectName("props_lbl")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.props_lbl)
        self.hid_lbl = QtWidgets.QLabel(Form)
        self.hid_lbl.setObjectName("hid_lbl")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.hid_lbl)
        self.hid_disp = QtWidgets.QLabel(Form)
        self.hid_disp.setFrameShape(QtWidgets.QFrame.Box)
        self.hid_disp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hid_disp.setAlignment(QtCore.Qt.AlignCenter)
        self.hid_disp.setObjectName("hid_disp")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.hid_disp)

        self.textBrowser = QtWidgets.QLabel(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setFrameShape(QtWidgets.QFrame.Box)
        self.textBrowser.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.textBrowser)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.geo_lbl.setText(_translate("Form", "Geography:"))
        self.geo_disp.setText(_translate("Form", "..."))
        self.textBrowser.setText(_translate("Form", "..."))
        self.props_lbl.setText(_translate("Form", "Properties:"))
        self.hid_lbl.setText(_translate("Form", "Hex ID:"))
        self.hid_disp.setText(_translate("Form", "00-00-00"))
