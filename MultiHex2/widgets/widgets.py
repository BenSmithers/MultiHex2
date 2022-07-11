
"""
Widgets should all have a "configure" function to connect them to the Scene/Map 

These will setup all the functions that allow the widget to adjust the scene's current tool. 
When a widget is instantiated, only that widet's tool can be selected. 
"""
import os
import json


from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QColorDialog

from MultiHex2.generation.name_gen import create_name
from MultiHex2.tools.widgetgui.hextoolgui import Ui_Form as HexToolWidgetGui
from MultiHex2.tools.widgetgui.regionui import Ui_Form as RegionToolWidgetGui
from MultiHex2.tools.widgetgui.pathui import Ui_Form as PathToolWidgetGui
from MultiHex2.guis.hex_select_gui import hex_select_gui
from MultiHex2.actions.regionactions import MetaRegionUpdate
from MultiHex2.widgets.basic_widget import ToolWidget


class PathWidget(ToolWidget):
    def __init__(self, parent, tool, tileset, text_source):
        super().__init__(parent, tool, tileset, text_source)
        self.ui = PathToolWidgetGui()
        self.ui.setupUi(self)

        self.ui.add_to_end.clicked.connect(self.add_to_end)
        self.ui.add_to_start.clicked.connect(self.add_to_start)
        self.ui.name_shuffle.clicked.connect(self.shuffle_name)


    def shuffle_name(self):
        pass

    def add_to_start(self):
        self.tool.set_state(3)


    def add_to_end(self):
        self.tool.set_state(4)

class RiverWidget(PathWidget):
    def __init__(self, parent, tool, tileset, text_source):
        super().__init__(parent, tool, tileset, text_source)

        #self.ui.river_add_button = QtWidgets.QPushButton(self)
        #self.ui.river_add_button.setObjectName("river_add_button")
        #self.ui.river_add_button.setText("Create River!")
        #self.ui.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.ui.river_add_button)
        #self.ui.river_add_button.clicked.connect(self.new_river_auto)

    def new_river_auto(self):
        new_code = 1

        while new_code!=0:
            new_code = 0 # _pour_river(self.tool.parent)
            print("Ended with code {}".format(new_code))


class RegionWidget(ToolWidget):
    def __init__(self, parent, tool,tileset, text_source):
        ToolWidget.__init__(self, parent, tool,tileset, text_source)
        self.ui = RegionToolWidgetGui()
        self.ui.setupUi(self)

        self.ui.color_choice_button.clicked.connect(self.choose_color)
        self.ui.delete_button.clicked.connect(self.delete_region)
        self.ui.apply_button.clicked.connect(self.apply)
        self.ui.new_name_button.clicked.connect(self.random_name)

    def random_name(self):

        if self._tool.tool_layer().value==2:
            what = "county"
        elif self._tool.get_selected_region() is not None:
            what = self._tool.get_selected_region().geography
        else:
            what = ""
        new_name = create_name(what, filename=self.text_source)
        self.ui.name_edit.setText(new_name)

    def choose_color(self):
        
        self.new_color = QColorDialog.getColor(initial = self.new_color, parent=self)

        self.ui.color_choice_button.setStyleSheet("background-color:rgb({},{},{})".format(self.new_color.red(), self.new_color.green(), self.new_color.blue()))

    def delete_region(self):
        pass

    def apply(self):
        new_name = self.ui.name_edit.text()
        rid = self._tool.selected
        action = MetaRegionUpdate(name=new_name, fill=self.new_color, rid=rid, layer=self._tool.tool_layer())
        # this kinda bypasses the typical tool-action functionality, but it's fine...

        self._tool.parent.do_now(action)
        

class HexSelectWidget(ToolWidget):
    def __init__(self, parent, tool,tileset,text_source):
        super().__init__(parent, tool,tileset,text_source)
        self.ui = hex_select_gui()
        self.ui.setupUi(self)
        


class HexBrushWidget(ToolWidget):
    def __init__(self, parent, tool,tileset,text_source):
        ToolWidget.__init__(self, parent, tool,tileset,text_source)
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

