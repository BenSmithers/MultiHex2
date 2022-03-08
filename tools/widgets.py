
"""
Widgets should all have a "configure" function to connect them to the Scene/Map 

These will setup all the functions that allow the widget to adjust the scene's current tool. 
When a widget is instantiated, only that widet's tool can be selected. 
"""
import os
import json

from PyQt5 import QtWidgets, QtGui, QtCore
from MultiHex2.tools.widgetgui.hextoolgui import Ui_Form as HexToolWidgetGui
from MultiHex2.tools.widgetgui.regionui import Ui_Form as RegionToolWidgetGui
# from MultiHex2.tools.clicker_tool import Clicker

class ToolWidget(QtWidgets.QWidget):
    def __init__(self, parent, tool):
        QtWidgets.QWidget.__init__(self, parent)
        self._tool = tool

class RegionWidget(ToolWidget):
    def __init__(self, parent, tool):
        ToolWidget.__init__(self, parent, tool)
        self.ui = RegionToolWidgetGui()
        self.ui.setupUi(self)
        self.setMaximumWidth(250)
        

class HexBrushWidget(ToolWidget):
    def __init__(self, parent, tool):
        ToolWidget.__init__(self, parent, tool)
        self.ui = HexToolWidgetGui()
        self.ui.setupUi(self)

        self.setMaximumWidth(250)

        self.ui.tilesetbutton.clicked.connect(self.load_tileset)
        self.ui.leftbutton.clicked.connect(self.decrease_size)
        self.ui.rightbutton.clicked.connect(self.increase_size)

        self._data = {}
        self._apply_tileset("/home/ben/software/MultiHex2/resources/main.json")
        self.ui.hex_sub_list.clicked[QtCore.QModelIndex].connect( self.hex_subtype_clicked )
        self.ui.combobox.currentIndexChanged.connect(self.hex_supertype_clicked)

    def hex_supertype_clicked(self):
        self.ui.hex_list_entry.clear()
        this_sub = self.ui.combobox.currentText()

        for entry in self._data[this_sub]:
            this = QtGui.QStandardItem(entry)
            color =  self._data[this_sub][entry]["color"]
            this.setBackground( QtGui.QColor(color[0], color[1], color[2] ))
            self.ui.hex_list_entry.appendRow(this)

    def hex_subtype_clicked(self, index=None):
        sub_type = index.data()
        this_type = self.ui.combobox.currentText()
        color =  self._data[this_type][sub_type]["color"]
        self._tool.set_fill(QtGui.QColor(color[0], color[1], color[2] ))
        self._tool.set_param_preset(self._data[this_type][sub_type]["params"])

    def increase_size(self):
        if self._tool.size<6:
            self._tool.setsize(self._tool.size + 1)
        self.ui.sizelbl.setText("{}".format(self._tool.size))
    def decrease_size(self):
        if self._tool.size >1:
            self._tool.setsize(self._tool.size-1)
        self.ui.sizelbl.setText("{}".format(self._tool.size))
    def load_tileset(self):
        pathto = QtWidgets.QFileDialog.getOpenFileName(None, 'Open TileSet', os.path.join(os.path.dirname(__file__),'..','resources'), 'Json (*.json)')[0]
        if pathto=="" or pathto is None:
            return
        self._apply_tileset(pathto)

    def _apply_tileset(self,pathto:str):
        f = open(pathto,'r')
        self._data = json.load(f)
        f.close()
        for key in self._data:
            self.ui.combobox.addItem(key)

        self.hex_supertype_clicked()

