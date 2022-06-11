# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temporary.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(285, 293)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.brushlabel = QtWidgets.QLabel(Form)
        self.brushlabel.setObjectName("brushlabel")
        self.verticalLayout.addWidget(self.brushlabel)
        self.sizelayout = QtWidgets.QHBoxLayout()
        self.sizelayout.setObjectName("sizelayout")
        self.leftbutton = QtWidgets.QPushButton(Form)
        self.leftbutton.setObjectName("leftbutton")
        self.sizelayout.addWidget(self.leftbutton)
        self.sizelbl = QtWidgets.QLabel(Form)
        self.sizelbl.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sizelbl.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sizelbl.setAlignment(QtCore.Qt.AlignCenter)
        self.sizelbl.setObjectName("sizelbl")
        self.sizelayout.addWidget(self.sizelbl)
        self.rightbutton = QtWidgets.QPushButton(Form)
        self.rightbutton.setObjectName("rightbutton")
        self.sizelayout.addWidget(self.rightbutton)
        self.verticalLayout.addLayout(self.sizelayout)
        self.tilesetlyt = QtWidgets.QHBoxLayout()
        self.tilesetlyt.setObjectName("tilesetlyt")
        self.tilesetlbl = QtWidgets.QLabel(Form)
        self.tilesetlbl.setObjectName("tilesetlbl")
        self.tilesetlyt.addWidget(self.tilesetlbl)
        self.tilesetbutton = QtWidgets.QPushButton(Form)
        self.tilesetbutton.setObjectName("tilesetbutton")
        self.tilesetlyt.addWidget(self.tilesetbutton)
        self.verticalLayout.addLayout(self.tilesetlyt)
        self.combobox = QtWidgets.QComboBox(Form)
        self.combobox.setObjectName("combobox")
        self.verticalLayout.addWidget(self.combobox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)


        self.hex_sub_list = QtWidgets.QListView(Form)
        self.hex_sub_list.setObjectName("hex_sub_list")
        self.verticalLayout.addWidget(self.hex_sub_list)

        self.hex_list_entry = QtGui.QStandardItemModel()
        self.hex_sub_list.setModel( self.hex_list_entry )

        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.brushlabel.setText(_translate("Form", "Brush Size:"))
        self.leftbutton.setText(_translate("Form", "<-"))
        self.sizelbl.setText(_translate("Form", "1"))
        self.rightbutton.setText(_translate("Form", "->"))
        self.tilesetlbl.setText(_translate("Form", "Tileset: NULL"))
        self.tilesetbutton.setText(_translate("Form", "Load New Tileset"))
