from PyQt5 import QtWidgets, QtGui, QtCore
from MultiHex2.generation.generation_config_widget import GenConfigWidget

import os
import json


class UI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")

        self.size_lbl = QtWidgets.QLabel(Form)
        self.size_lbl.setObjectName("size_lbl")
        self.size_combo = QtWidgets.QComboBox(Form)
        self.size_combo.setObjectName("size_combo")
        self.size_combo.addItem("Small")
        self.size_combo.addItem("Medium")
        self.size_combo.addItem("Large")
        self.formLayout.setWidget(0,QtWidgets.QFormLayout.LabelRole, self.size_lbl)
        self.formLayout.setWidget(0,QtWidgets.QFormLayout.FieldRole, self.size_combo)


        # mountain range len, continent spread? 

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

        self.size_lbl.setText(_translate("Form", "Size (Preset)"))



class SwoNConfigWidget(GenConfigWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.ui = UI()
        self.ui.setupUi(self)

        _fpath = os.path.join(os.path.dirname(__file__), "config.json")
        _obj = open(_fpath, 'r')
        self.data = json.load(_obj)
        _obj.close()

        self.ui.size_combo.setCurrentIndex(1)
        
        self.ui.size_combo.currentIndexChanged.connect(self.change_size)

    def change_size(self):
        pass

    def get_config(self) -> dict:
        print("Called get config")

         # mountains values dimx/dimy
        
        if self.ui.size_combo.currentIndex()==0:
            self.data["dimx"] = int(self.data["dimx"]*0.5)
            self.data["dimy"] = int(self.data["dimy"]*0.5)
        elif self.ui.size_combo.currentIndex()==2:
            self.data["dimx"] = int(self.data["dimx"]*1.5)
            self.data["dimy"] = int(self.data["dimy"]*1.5)

        
        return self.data
