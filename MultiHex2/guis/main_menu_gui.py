
from PyQt5 import QtCore, QtGui, QtWidgets
import os

"""
This file defines the UI of the dialog window is displayed when MultiHex first launches 
"""

class main_menu_gui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 279)

        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.picture = QtWidgets.QLabel(Dialog)
        self.picture.setText("")
        self.picture.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..", "assets", 'multihex_logo.png')).scaledToWidth(350) )
        self.picture.setScaledContents(False)
        self.picture.setObjectName("picture")
        self.picture.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.picture)

        self.new_map_button = QtWidgets.QPushButton(Dialog)
        self.new_map_button.setObjectName("new_map_button")
        self.verticalLayout.addWidget(self.new_map_button)

        self.load_map_button = QtWidgets.QPushButton(Dialog)
        self.load_map_button.setObjectName("load_map_button")
        self.verticalLayout.addWidget(self.load_map_button)

        self.settings_button = QtWidgets.QPushButton(Dialog)
        self.settings_button.setObjectName("settings_button")
        self.verticalLayout.addWidget(self.settings_button)

        self.quit_button = QtWidgets.QPushButton(Dialog)
        self.quit_button.setObjectName("quit_button")
        self.verticalLayout.addWidget(self.quit_button)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Welcome to MultiHex!"))
        self.new_map_button.setText(_translate("Dialog","New Map"))
        self.load_map_button.setText(_translate("Dialog","Load Map"))
        self.settings_button.setText(_translate("Dialog","Settings"))
        self.quit_button.setText(_translate("Dialog","Quit"))

class SettingsGui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 279)

        self.verticalLayout = QtWidgets.QFormLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.primary_mouse_label = QtWidgets.QLabel(Dialog)
        self.primary_mouse_label.setObjectName("primary_mouse_label")
        
        self.verticalLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.primary_mouse_label)

        self.primary_mouse_combo = QtWidgets.QComboBox(Dialog)
        self.primary_mouse_combo.setObjectName("primary_mouse_combo")
        self.primary_mouse_combo.addItem("Left Button")
        self.primary_mouse_combo.addItem("Right Button")                
        self.verticalLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.primary_mouse_combo)

        self.module_lbl = QtWidgets.QLabel(Dialog)
        self.module_lbl.setObjectName("module_lbl")
        self.verticalLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.module_lbl)

        self.module_combo = QtWidgets.QComboBox(Dialog)
        self.module_combo.setObjectName("module_combo")            
            
        self.verticalLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.module_combo)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")

        self.verticalLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)

        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MultiHex Settings"))
        self.primary_mouse_label.setText(_translate("Dialog","Primary Mouse Button"))
        self.module_lbl.setText(_translate("Dialog","Use Module"))