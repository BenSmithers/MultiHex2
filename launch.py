#!/usr/bin/python3.8

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFileDialog, QGraphicsScene
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt


from MultiHex2.guis.main_gui import main_gui
from MultiHex2.tools import Clicker
from MultiHex2.tools.hextools import HexBrush,HexSelect
from MultiHex2.tools.regiontools import RegionAdd
from MultiHex2.tools.route_test_tool import RouteTester
from MultiHex2.tools.entity_tools import EntitySelector, AddEntityTool, AddSettlement
from MultiHex2.tools import Basic_Tool
from MultiHex2.generation.overland import fullsim
from MultiHex2.guis.savewarn import SaveWarnDialogGui

import os
import sys
import typing


from tools.basic_tool import ToolLayer

if sys.platform=="linux":
    SAVEDIR = os.path.join(os.environ["HOME"], ".local", "MultiHex")
elif sys.platform=="darwin":
    raise NotImplementedError()
elif sys.platform=="win32":
    SAVEDIR = os.path.join(os.environ["AppData"], "MultiHex")
else:
    raise NotImplementedError("Unrecognized os {}".format(sys.platform))

if not os.path.exists(SAVEDIR):
    os.mkdir(SAVEDIR)

class WarnWidget(QtWidgets.QDialog):
    def __init__(self, parent: typing.Optional[QWidget] = ..., flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = ...) -> None:
        super().__init__(parent, flags)
        self.ui = SaveWarnDialogGui()
        self.ui.setupUi(self)
        self.parent = parent


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
        self.ui.graphicsView.setScene( self.scene )
        self.ui.graphicsView.setMouseTracking(True)

        self.ui.actionOpen.triggered.connect(self.load)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.export_image.triggered.connect(self.export_image)


        self.add_tool("hex_brush", HexBrush)
        self.add_tool("hex_select", HexSelect)
        self.add_tool("region_add", RegionAdd)
        #self.add_tool("route_tester", RouteTester)
        self.add_tool("entity_select", EntitySelector)
        self.add_tool("entity_add", AddEntityTool)
        self.add_tool("settlement_add", AddSettlement)

    def export_image(self):
        temp= QFileDialog.getSaveFileName(None, 'Exoport Image', SAVEDIR, 'PNGs (*.png)')[0]
        if temp is None:
            return
        elif temp=='':
            return
        
        #self.main_map.dimensions
        size   = QtCore.QSize(self.scene.dimensions[0], self.scene.dimensions[1])
        image  = QtGui.QImage(size,QtGui.QImage.Format_ARGB32_Premultiplied)
        painter= QtGui.QPainter(image)
        self.scene.render(painter)
        painter.end()
        image.save(temp)

    def new(self):
        fullsim(self.scene)

    def save(self):
        self.scene.reset_save()

        if self.scene.file_name=="":
            self.saveAs()
        else:
            self.scene.save(self.scene.file_name)    

    def saveAs(self):
        pathto = QFileDialog.getSaveFileName(None, 'Save As',SAVEDIR, 'Json (*.json)')[0]
        if pathto is not None:
            if pathto!="":
                self.scene.save(pathto)
                self.scene.reset_save()

    def quit(self):
        if self.scene.unsaved:
            self.dialog = WarnWidget(parent=self)
            self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.dialog.exec_()

        sys.exit()

    def load(self)->str:
        pathto = QFileDialog.getOpenFileName(None, 'Save As',SAVEDIR, 'Json (*.json)')[0]
        if pathto is not None:
            if pathto!="":
                self.scene.load( pathto)
                self.scene.reset_save()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key()==Qt.Key_Escape:
            self.select_tool("basic")

    def add_tool(self,tool_name:str, tool:Basic_Tool):

        self.ui.add_button(tool_name, tool.buttonIcon(), tool.altText(), tool.tool_layer() )
        def tempfunc():
            return self.select_tool(tool_name)
        
        value = tool.tool_layer().value
        if value==0 or value==1:
            self.ui.buttons[tool_name].clicked.connect(tempfunc)
        elif value==2:
            self.ui.second_buttons[tool_name].clicked.connect(tempfunc)
        else:
            raise NotImplementedError("Not layer {}".format(tool.tool_layer()))

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
