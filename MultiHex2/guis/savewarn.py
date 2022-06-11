# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'savewarn.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import os

class SaveWarnDialogGui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(521, 275)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(75, 75))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__),"..", "assets", "map_icons", "ruin.svg")))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.warnword = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.warnword.setFont(font)
        self.warnword.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.warnword.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.warnword.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.warnword.setScaledContents(False)
        self.warnword.setAlignment(QtCore.Qt.AlignCenter)
        self.warnword.setObjectName("warnword")
        self.horizontalLayout.addWidget(self.warnword)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.warntext = QtWidgets.QLabel(Dialog)
        self.warntext.setMaximumSize(QtCore.QSize(16777215, 59))
        self.warntext.setAutoFillBackground(False)
        self.warntext.setAlignment(QtCore.Qt.AlignCenter)
        self.warntext.setWordWrap(True)
        self.warntext.setObjectName("warntext")
        self.verticalLayout.addWidget(self.warntext)
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Discard|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.warnword.setText(_translate("Dialog", "WARNING!"))
        self.warntext.setText(_translate("Dialog", "There are unsaved changes! Do you want to close without saving, cancel, or save and qut?"))
