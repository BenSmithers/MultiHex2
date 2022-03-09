#!/usr/bin/python3.8

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFileDialog, QGraphicsScene
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from MultiHex2.guis.main_gui import main_gui
from MultiHex2.tools import Clicker
from MultiHex2.tools.hextools import HexBrush,HexSelect
from MultiHex2.tools.regiontools import RegionAdd
from MultiHex2.tools import Basic_Tool

import os
import sys

SAVEDIR = os.path.join(os.environ["HOME"], ".local", "MultiHex")
if not os.path.exists(SAVEDIR):
    os.mkdir(SAVEDIR)

class main_window(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__),'assets','multihex_small_logo.svg')))

        # standard boiler-plate gui initialization
        # we instantiate the default GUI before anything else 
        self.ui = main_gui()
        self.ui.setupUi(self)

        self.scene = Clicker( self.ui.graphicsView, self )
        # Allow the graphics view to follow the mouse when it isn't being clicked, and associate the clicker control with the ui 
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )
        self.ui.actionOpen.triggered.connect(self.load)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionQuit.triggered.connect(self.quit)


        self.add_tool("hex_brush", HexBrush)
        self.add_tool("hex_select", HexSelect)
        self.add_tool("region_add", RegionAdd)

    def save(self):
        self.scene.reset_save()

    def saveAs(self):
        pathto = QFileDialog.getSaveFileName(None, 'Save As',SAVEDIR, 'Json (*.json)')[0]
        if pathto is not None:
            if pathto!="":
                self.scene.save(pathto)
                self.scene.reset_save()

    def quit(self):
        if self.scene.unsaved:
            print("WARN")

        sys.exit()

    def load(self)->str:
        pathto = QFileDialog.getOpenFileName(None, 'Save As',SAVEDIR, 'Json (*.json)')[0]
        if pathto is not None:
            if pathto!="":
                self.scene.load( pathto)
                self.scene.reset_save()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key()==Qt.Key_Escape:
            print("escape?")
            self.select_tool("basic")

    def add_tool(self,tool_name:str, tool:Basic_Tool):
        self.ui.add_button(tool_name, tool.buttonIcon(), tool.altText() )
        def tempfunc():
            return self.select_tool(tool_name)
        self.ui.buttons[tool_name].clicked.connect(tempfunc)
        self.scene.add_tool(tool_name, tool)

    def select_tool(self, tool_name:str):
        self.scene.select_tool(tool_name)
        
        if self.ui.toolwidget is not None:
            self.ui.toolPane.removeWidget(self.ui.toolwidget)
            self.ui.toolwidget.deleteLater()
            self.ui.toolwidget = None
        self.ui.toolwidget = self.scene.tool.widget()(self.ui.centralwidget, self.scene.tool)
        self.ui.toolPane.addWidget(self.ui.toolwidget)
        self.ui.toolPane.update()
        

app = QApplication(sys.argv)
app_instance = main_window()

if __name__=="__main__":
    # make sure the base saves folder exists 
    app_instance.show()
    sys.exit(app.exec_())
