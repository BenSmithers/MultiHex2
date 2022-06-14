"""
    Implementing the main menu Dialog 
"""
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QWidget

import typing
import json

from MultiHex2.guis.main_menu_gui import main_menu_gui, SettingsGui

class MainMenuDialog(QDialog):
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)
        self.parent = parent
        self.ui = main_menu_gui()
        self.ui.setupUi(self)

        self.ui.load_map_button.clicked.connect(self.button_load)
        self.ui.new_map_button.clicked.connect(self.button_new)
        self.ui.settings_button.clicked.connect(self.button_settings)
        self.ui.quit_button.clicked.connect(self.button_quit)

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

    def button_new(self):
        success = self.parent.new()
        if success:
            self.accept()
        else:
            self.reject()

    def button_load(self):
        loaded = self.parent.load()
        if loaded!="":
            self.accept()
    def button_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

        dialog.deleteLater()

    def button_quit(self):
        sys.exit()
    

        
class SettingsDialog(QDialog):
    """
    This is used for changing global settings used by MultiHex. Only two so far...
        default module
        primary mouse (left/right)
    """
    def __init__(self, parent)->None:
        super().__init__(parent)
        self.ui = SettingsGui()
        self.ui.setupUi(self)
        self.parent = parent

        self.accepted.connect(self.on_accept)
        self.path = self.parent.parent.config_filepath
        f = open(self.path, 'rt')
        self.config = json.load(f)
        f.close()

        if self.config["primary_mouse"]=="left":
            self.ui.primary_mouse_combo.setCurrentIndex(0)
        else:
            self.ui.primary_mouse_combo.setCurrentIndex(1)

        count = 0 
        
        while self.ui.module_combo.currentText()!=self.config["module"]:
            self.ui.module_combo.setCurrentIndex(count)
            count+=1
        
            if self.ui.module_combo.count()==count:
                self.ui.module_combo.setCurrentIndex(0)
                print("WARNING! Incorrect configuration loaded!")
                break


    def on_accept(self):
        """
            Change the config, then write it to the settings file 
        """
        self.was_accepted = True

        if self.ui.primary_mouse_combo.currentText()=="Left Button":
            self.config["primary_mouse"]="left"
        else:
            self.config["primary_mouse"]="right"

        self.config["module"] = self.ui.module_combo.currentText()

        f = open(self.path, 'wt')
        json.dump(self.config, f)
        f.close()

        self.parent.parent.reload_config()
        

