from MultiHex2.tools.basic_tool import Basic_Tool
from MultiHex2.actions import Add_Remove_Hex
from MultiHex2.tools.widgets import HexBrushWidget
from MultiHex2.core import hex_to_screen, screen_to_hex, Hex
import os 

from PyQt5 import QtGui
from actions.baseactions import NullAction

from tools.basic_tool import ToolLayer

"""
Tools make actions 
"""

art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')

class HexSelect(Basic_Tool):
    
    def __init__(self, parent):
        Basic_Tool.__init__(self, parent)
        self.tool_layer = ToolLayer.terrain
        self.highlight = False

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

 