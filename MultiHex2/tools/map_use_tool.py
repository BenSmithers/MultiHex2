from math import pi
import os

from MultiHex2.core.enums import ToolLayer
from MultiHex2.tools import Basic_Tool
from MultiHex2.core.coordinates import screen_to_hex, hex_to_screen
from MultiHex2.actions import NullAction

from PyQt5 import QtGui

art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')

class MapUse(Basic_Tool):
    """
        Define the tool that can be used to move mobiles around, look at them, edit them, etc... 
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.dimensions = self.parent.dimensions

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "temp.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "temp.svg")).scaled(48,48)

    @classmethod
    def tool_layer(cls):
        return ToolLayer.mapuse

    def primary_mouse_released(self, event):
        locid =  screen_to_hex( event.scenePos() )
        pos = hex_to_screen(locid)

        longitude = 2*pi*pos.x()/self.dimensions[0]
        
        
        latitude = -(pi*pos.y()/self.dimensions[1]) + 0.5*pi

        self.parent.config_with(latitude,longitude)

        self.parent.update_times()

        # check for mobile here, 

        return NullAction()