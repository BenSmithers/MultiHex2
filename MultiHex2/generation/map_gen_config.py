"""
Define a Widget Dialog for grabbing map configuration parameters. 

The widget accepts a dictionary to configure itself with various config parameters. 
It can then provide a similarly structured dictionary with those config parameters after user modifications. 
"""

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

import typing
import numpy as np

from MultiHex2.generation.generation_config_widget import GenConfigWidget

relate = {
    int:QtWidgets.QSpinBox
}

class MapMakerDialogGui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 250))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName("formLayout")

        

        self.seedLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.seedLabel.setObjectName("seedLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.seedLabel)
        self.seedEdit = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.seedEdit.setObjectName("seedEdit")
        self.seedEdit.setMinimum(-2147483647)
        self.seedEdit.setMaximum(2147483647)
        self.seedEdit.setValue(np.random.randint(-2147483647,2147483647))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.seedEdit)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Map Generation Options"))
        self.seedLabel.setText(_translate("Dialog", "Seed"))


class MapGenConfigDialog(QDialog):
    def __init__(self, parent: typing.Optional[QWidget] = ..., sub_widget = GenConfigWidget) -> None:
        super().__init__(parent)
        self.parent = parent

        self.ui = MapMakerDialogGui()
        self.ui.setupUi(self)

        self.sub_widget = sub_widget(self.ui.scrollAreaWidgetContents)
        self.sub_widget.setObjectName("sub_widget")
        self.ui.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sub_widget)

        self._accepted = False

    @property
    def Accepted(self):
        return self._accepted
    @property
    def Rejected(self):
        return not self._accepted

    def accept(self):
        self._accepted = True
        QDialog.accept(self)
    def reject(self):
        self._accepted = False
        QDialog.reject(self)

    def set_config(self, config:dict)->None:
        pass

    def get_config(self)->dict:
        return self.sub_widget.get_config()

    def get_seed(self)->int:
        return self.ui.seedEdit.value()
