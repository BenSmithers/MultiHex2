"""
    Implementing the main menu Dialog 
"""
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QWidget

import typing

from MultiHex2.guis.main_menu_gui import main_menu_gui

class MainMenuDialog(QDialog):
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)
        self.parent = parent
        self.ui = main_menu_gui()
        self.ui.setupUi(self)

        self.ui.load_map_button.clicked.connect(self.button_load)
        self.ui.new_map_button.clicked.connect(self.button_new)
        self.ui.quit_button.clicked.connect(self.button_quit)

    def button_new(self):
        self.accept()
        self.parent.new()
    def button_load(self):
        loaded = self.parent.load()
        if loaded!="":
            self.accept()
    def button_settings(self):
        pass
    def button_quit(self):
        sys.exit()
    

        