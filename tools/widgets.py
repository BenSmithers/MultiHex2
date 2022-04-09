
"""
Widgets should all have a "configure" function to connect them to the Scene/Map 

These will setup all the functions that allow the widget to adjust the scene's current tool. 
When a widget is instantiated, only that widet's tool can be selected. 
"""
import os
import json

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QColorDialog

from MultiHex2.tools.widgetgui.hextoolgui import Ui_Form as HexToolWidgetGui
from MultiHex2.tools.widgetgui.regionui import Ui_Form as RegionToolWidgetGui
from MultiHex2.guis.hex_select_gui import hex_select_gui
# from MultiHex2.tools.clicker_tool import Clicker

class ToolWidget(QtWidgets.QWidget):
    def __init__(self, parent, tool, tileset):
        QtWidgets.QWidget.__init__(self, parent)
        self._tool = tool

        self._tool.link_to_widget(self)
        self.tileset = tileset
        self.setMaximumWidth(250)
        self.setMinimumWidth(250)

class RegionWidget(ToolWidget):
    def __init__(self, parent, tool,tileset):
        ToolWidget.__init__(self, parent, tool,tileset)
        self.ui = RegionToolWidgetGui()
        self.ui.setupUi(self)

        self.ui.color_choice_button.clicked.connect(self.choose_color)
        self.ui.delete_button.clicked.connect(self.delete_region)
        self.ui.apply_button.clicked.connect(self.delete_region)

    def choose_color(self):
        old_one = QtGui.QColor(0,0,0)
        new_color = QColorDialog.getColor(initial = old_one, parent=self.parent)

    def delete_region(self):
        pass

    def apply(self):
        pass
        

class HexSelectWidget(ToolWidget):
    def __init__(self, parent, tool,tileset):
        super().__init__(parent, tool,tileset)
        self.ui = hex_select_gui()
        self.ui.setupUi(self)
        


class HexBrushWidget(ToolWidget):
    def __init__(self, parent, tool,tileset):
        ToolWidget.__init__(self, parent, tool,tileset)
        self.ui = HexToolWidgetGui()
        self.ui.setupUi(self)

        self.ui.tilesetbutton.clicked.connect(self.load_tileset)
        self.ui.leftbutton.clicked.connect(self.decrease_size)
        self.ui.rightbutton.clicked.connect(self.increase_size)

        self._data = {}

        self._apply_tileset(self.tileset)
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
        self.ui.combobox.clear()
        f = open(pathto,'r')
        self._data = json.load(f)
        f.close()
        for key in self._data:
            self.ui.combobox.addItem(key)

        self.hex_supertype_clicked()

