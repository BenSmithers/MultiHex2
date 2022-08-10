from MultiHex2.core.core import ToolLayer
from MultiHex2.tools.basic_tool import Basic_Tool
from MultiHex2.actions import Add_Remove_Hex
from MultiHex2.widgets.widgets import HexBrushWidget, HexSelectWidget
from MultiHex2.core import hex_to_screen, screen_to_hex, Hex
import os 

from PyQt5 import QtGui
from MultiHex2.actions.baseactions import NullAction

"""
Tools make actions 
"""

art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')

class HexSelect(Basic_Tool):
    
    def __init__(self, parent):
        Basic_Tool.__init__(self, parent)
        self.highlight = False

    def primary_mouse_released(self, event):
        loc = screen_to_hex(event.scenePos())
        this_hex = self.parent.accessHex(loc)

        if this_hex is None:
            self._widget_instance.ui.geo_disp.setText("...")
            self._widget_instance.ui.hid_disp.setText("00-00-00")
            self._widget_instance.ui.textBrowser.setText("...")
        else:
            self._widget_instance.ui.geo_disp.setText(this_hex.geography)
            self._widget_instance.ui.hid_disp.setText(str(loc))
            full_str = ""
            for key in this_hex.params.keys():
                full_str += "{}: {}\n".format(key, this_hex.params[key])
            full_str += "{}: {}\n".format("Is land: ", this_hex.is_land)
                
            self._widget_instance.ui.textBrowser.setText(full_str)                


        return NullAction()

    @classmethod
    def tool_layer(cls):
        return ToolLayer.terrain

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "select_hex.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "select_hex.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "Hex Select Tool"

    @classmethod
    def widget(self):
        return HexSelectWidget

class HexBrush(Basic_Tool):
    """
        A Brush for drawing hexes on the map 
    """

    def __init__(self, parent):
        Basic_Tool.__init__(self, parent)
        self.highlight = True
        self._brushsize = 1
        self._fill = QtGui.QColor(0,0,0)
        self._params = {}
        self._lastID = None
        
    @classmethod
    def tool_layer(cls):
        return ToolLayer.terrain

    def set_fill(self, fill:QtGui.QColor):
        self._fill = fill
        self._lastID= None
    def set_param_preset(self, params:dict):
        self._params = params
        self._lastID=None

    def primary_mouse_held(self, event):
        return self.primary_mouse_released(event)

    def primary_mouse_released(self, event):
        loc = screen_to_hex(event.scenePos())
        if loc==self._lastID:
            return NullAction()
        else:
            self._lastID = loc
            center = hex_to_screen(loc)
            newhex = Hex(center)
            newhex.set_fill(self._fill)
            newhex.set_params(self._params)
            new_action = Add_Remove_Hex(hexID=loc,
                                        hex=newhex)
            return new_action

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "hex_brush.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "hex_brush.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "Hex Brush Tool"

    @classmethod
    def widget(cls):
        return HexBrushWidget

    def setsize(self, value:int):
        self._brushsize = value
        self._lastID=None
    @property
    def size(self)->int:
        return self._brushsize

 