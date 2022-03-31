from MultiHex2.tools.basic_tool import Basic_Tool, ToolLayer
from MultiHex2.tools.widgets import RegionWidget
from MultiHex2.core import Region, screen_to_hex, Hex, HexID
from actions.baseactions import NullAction
from MultiHex2.actions.regionactions import Merge_Regions_Action, Region_Add_Remove, New_Region_Action

import os 

from PyQt5 import QtGui, QtWidgets

from core.coordinates import hex_to_screen


art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')


class RegionAdd(Basic_Tool):
    """
    Used to add/remove from a region. 
    Left click add, right click remove. If it's in state zero, tries to select the region under the cursor. 
    """
    def __init__(self, parent):
        Basic_Tool.__init__(self, parent)
        self.highlight = True
        self._selected_rid = -1

    @classmethod
    def tool_layer(cls):
        return ToolLayer.terrain

    def deselect(self):
        self._selected_rid = -1
        return super().deselect()

    def select(self, rid:int):
        """
        Select a region
        """
        self._selected_rid = rid

    def secondary_mouse_held(self, event):
        return self.secondary_mouse_released(event)

    def primary_mouse_held(self, event):
        return self.primary_mouse_released(event)
    

    def primary_mouse_released(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        loc =  screen_to_hex( event.scenePos() )
        this_rid = self.parent.accessHexRegion(loc) # region under hex, none if no region
        if self._selected_rid == -1:
            # make new region
            if this_rid is None:
                hex_here = Hex(hex_to_screen(loc))
                action = New_Region_Action(region=Region(hex_here), rid=self.parent.get_next_rid())
                self._selected_rid = action.rID
                return action
            else:
                # choose the region under the cursor 
                self._selected_rid = this_rid
                return NullAction()

        else:
            # add to the selected region or add    
            if this_rid is None:
                # add to that region
                # ["rID", 'hexID']
                return Region_Add_Remove(rID = self._selected_rid, hexID=loc)
            else:
                self._selected_rid = this_rid
                return NullAction()

    @classmethod
    def widget(self):
        return RegionWidget

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "biome_brush.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "biome_brush.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "Hex Brush Tool"

