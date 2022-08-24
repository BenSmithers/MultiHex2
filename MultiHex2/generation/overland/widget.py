"""
Defining the widget(s) used to configure the overland module world generator
"""



from PyQt5 import QtWidgets, QtGui, QtCore
from MultiHex2.generation.generation_config_widget import GenConfigWidget

import os
import json

"""
I want this to be able to configure 
    - the number of continents
    - the dimensions (preset - small, medium, large)

"""

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

        self.cont_lbl = QtWidgets.QLabel(Form)
        self.cont_lbl.setObjectName("cont_lbl")
        self.cont_n = QtWidgets.QSpinBox(Form)
        self.cont_n.setObjectName("cont_n")
        self.cont_n.setMinimum(1)
        self.cont_n.setMaximum(90)
        self.cont_n.setValue(4)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.cont_lbl)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cont_n)

        self.range_lbl = QtWidgets.QLabel(Form)
        self.range_lbl.setObjectName("range_lbl")
        self.range_spin = QtWidgets.QSpinBox(Form)
        self.range_spin.setMinimum(1)
        self.range_spin.setMaximum(99)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.range_lbl)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.range_spin)

        self.spread_lbl = QtWidgets.QLabel(Form)
        self.spread_lbl.setObjectName("spread_lbl")
        self.spread_combo = QtWidgets.QDoubleSpinBox(Form)
        self.spread_combo.setMinimum(0.0)
        self.spread_combo.setMaximum(1.0)
        self.spread_combo.setSingleStep(0.01)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.spread_lbl)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spread_combo)


        # mountain range len, continent spread? 

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

        self.size_lbl.setText(_translate("Form", "Size (Preset)"))
        self.cont_lbl.setText(_translate("Form","Number of Continents"))
        self.range_lbl.setText(_translate("Form", "Mountain Range Len"))
        self.spread_lbl.setText(_translate("Form","Land Spread Rate"))


class OverlandConfigWidget(GenConfigWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.ui = UI()
        self.ui.setupUi(self)

        _fpath = os.path.join(os.path.dirname(__file__), "config.json")
        _obj = open(_fpath, 'r')
        self.data = json.load(_obj)
        _obj.close()

        self.ui.size_combo.setCurrentIndex(1)
        self.ui.cont_n.setValue( self.data["continental"]["mountains"]["values"]["zones"] )
        self.ui.range_spin.setValue(self.data["continental"]["mountains"]["values"]["avg_range"])
        self.ui.spread_combo.setValue(self.data["continental"]["land"]["values"]["land_spread"])
        
        self.ui.size_combo.currentIndexChanged.connect(self.change_size)

    def change_size(self):
        if self.ui.size_combo.currentIndex()==2:
            self.ui.cont_n.setValue( int(self.data["continental"]["mountains"]["values"]["zones"]*1.5) )
            self.ui.range_spin.setValue(int(self.data["continental"]["mountains"]["values"]["avg_range"]*0.75))
            self.ui.spread_combo.setValue(self.data["continental"]["land"]["values"]["land_spread"]*0.5)
        elif self.ui.size_combo.currentIndex()==0:
            self.ui.cont_n.setValue( int(self.data["continental"]["mountains"]["values"]["zones"]*.25) )
            self.ui.range_spin.setValue(int(self.data["continental"]["mountains"]["values"]["avg_range"]*0.5))
            self.ui.spread_combo.setValue(self.data["continental"]["land"]["values"]["land_spread"]*0.25)
        elif self.ui.size_combo.currentIndex()==1:
            self.ui.cont_n.setValue( self.data["continental"]["mountains"]["values"]["zones"] )
            self.ui.range_spin.setValue(self.data["continental"]["mountains"]["values"]["avg_range"])
            self.ui.spread_combo.setValue(self.data["continental"]["land"]["values"]["land_spread"])
        else:
            raise NotImplementedError("Did you add another size category?")

    def get_config(self) -> dict:
        print("Called get config")
        self.data["continental"]["mountains"]["values"]["zones"] = self.ui.cont_n.value()
        self.data["continental"]["mountains"]["values"]["avg_range"] = self.ui.range_spin.value()
        self.data["continental"]["land"]["values"]["land_spread"] = self.ui.spread_combo.value()
         # mountains values dimx/dimy
        
        if self.ui.size_combo.currentIndex()==0:
            self.data["continental"]["mountains"]["values"]["dimx"] = int(self.data["continental"]["mountains"]["values"]["dimx"]*0.5)
            self.data["continental"]["mountains"]["values"]["dimy"] = int(self.data["continental"]["mountains"]["values"]["dimy"]*0.5)
        elif self.ui.size_combo.currentIndex()==2:
            self.data["continental"]["mountains"]["values"]["dimx"] = int(self.data["continental"]["mountains"]["values"]["dimx"]*1.5)
            self.data["continental"]["mountains"]["values"]["dimy"] = int(self.data["continental"]["mountains"]["values"]["dimy"]*1.5)

        
        return self.data["continental"]
"""

        self.state_lbl = QtWidgets.QLabel(Form)
        self.state_lbl.setObjectName("state_lbl")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.state_lbl)
        self.state_display = QtWidgets.QLabel(Form)
        self.state_display.setObjectName("state_display")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.state_display)
"""
