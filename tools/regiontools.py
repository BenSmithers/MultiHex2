from MultiHex2.tools.basic_tool import Basic_Tool, ToolLayer
from MultiHex2.tools.widgets import RegionWidget
from MultiHex2.core import Region, screen_to_hex, Hex, HexID
from MultiHex2.core.core import County
from actions.baseactions import NullAction
from MultiHex2.generation.name_gen import create_name
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

        self.regionType = Region
        self._need_to_update_widget = False

    def get_selected_region(self):
        if self._selected_rid!=-1:
            return self.parent.accessRegion(self._selected_rid, self.tool_layer())
        else:
            return None

    @property
    def selected(self):
        return self._selected_rid

    @classmethod
    def tool_layer(cls):
        return ToolLayer.terrain

    def deselect(self):
        self._selected_rid = -1
        self._need_to_update_widget = True
        return super().deselect()

    def update_gui(self):
        # update widget 
        if self._selected_rid != -1:
            this_region = self.get_selected_region()
            self.widget_instance.ui.name_edit.setText(this_region.name)
            color = this_region.fill
            self.widget_instance.new_color = color
            self.widget_instance.ui.color_choice_button.setStyleSheet("background-color:rgb({},{},{})".format(color.red(), color.green(), color.blue()))
        else:
            self.widget_instance.ui.name_edit.setText("")
            self.widget_instance.ui.color_choice_button.setStyleSheet("")

        self._need_to_update_widget = False

    def select(self, rid:int):
        """
        Select a region
        """
        self._selected_rid = rid
        self._need_to_update_widget = True

    def mouse_moved(self, event):
        if self._need_to_update_widget:
            self.update_gui()
        return NullAction()

    def secondary_mouse_held(self, event):
        return self.secondary_mouse_released(event)

    def primary_mouse_held(self, event):
        return self.primary_mouse_released(event)
    
    def secondary_mouse_released(self, event):
        """
        Removes hex from region
        """
        loc =  screen_to_hex( event.scenePos() )
        this_rid = self.parent.accessHexRegion(loc, self.tool_layer()) 

        if this_rid is None:
            return NullAction()
        else:
            self.select(this_rid)
            return Region_Add_Remove(rID = None, hexID=loc, layer=self.tool_layer())
        

    def primary_mouse_released(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        loc =  screen_to_hex( event.scenePos() )
        this_rid = self.parent.accessHexRegion(loc, self.tool_layer()) # region under hex, none if no region
        if self._selected_rid == -1:
            # make new region
            if this_rid is None:
                hex_here = Hex(hex_to_screen(loc))

                actual_hex = self.parent.accessHex(loc)
                new_region = self.regionType(hex_here)
                new_region.set_geography(actual_hex.geography)
                if self.tool_layer()==ToolLayer.civilization:
                    new_region.set_name(create_name("county", filename=self.widget_instance.text_source))
                else:
                    new_region.set_name(create_name(new_region.geography, filename=self.widget_instance.text_source))
                action = New_Region_Action(region=new_region, rid=self.parent.get_next_rid(self.tool_layer()), layer=self.tool_layer())
                self.select(action.rID)
                #self._selected_rid = action.rID
                return action
            else:
                # choose the region under the cursor 
                self.select(this_rid)
                #self._selected_rid = this_rid
                return NullAction()

        else:
            # add to the selected region or add    
            if this_rid is None:
                # add to that region
                # ["rID", 'hexID']
                return Region_Add_Remove(rID = self._selected_rid, hexID=loc, layer=self.tool_layer())
            else:
                self.select(this_rid)
                #self._selected_rid = this_rid
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
        return "Biome Draw Tool"


class CivAdd(RegionAdd):
    def __init__(self, parent):
        super().__init__(parent)
        self.regionType = County

    @classmethod
    def tool_layer(cls):
        return ToolLayer.civilization

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "county.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "county.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "County Draw Tool"