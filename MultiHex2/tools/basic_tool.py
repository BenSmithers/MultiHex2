import os
from enum import Enum

from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsScene, QWidget
from PyQt5.QtCore import QPointF
from MultiHex2.core.coordinates import hex_to_screen, screen_to_hex

from MultiHex2.widgets.basic_widget import ToolWidget
from MultiHex2.core.core import Hex, ToolLayer
from MultiHex2.tools.clicker_tool import Clicker
from MultiHex2.actions.baseactions import NullAction

art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')

class Basic_Tool:
    
    """
    Prototype a basic tool. We use this for consistent typing and templated functions. 
    
    So, you know, like why anyone else would use class inheritance 
    """
    def __init__(self, parent:Clicker):
        if not (isinstance(parent, Clicker) or (parent is None)):
            raise TypeError("Parent should be of type {}, not {}".format(Clicker, type(parent)))
        self._parent = parent
        self._state = 0
        self.highlight = False # highlight space under the cursor 

        self.auto_state = 0 # automatically set to this state when selected
        self.highlight_icon = ""

        self._widget_instance = None
        self._polygon = Hex(QPointF(0,0))

    @property 
    def parent(self)->Clicker:
        return self._parent

    def get_highlight_color(self):
        """
        See below, but now it's the highlight color! 
        """
        return QtGui.QColor(110,228,230)

    def get_polygon(self):
        """
        The clicker control can ask the tools for a polygon to use as the preview when highlighting
        
        This highlighted polygon is updated whenever the mouse is moved (and is by default a Hex)
        Other tools (like the path brush) implment other shapes! 
        """
        return self._polygon

    @property
    def widget_instance(self):
        return self._widget_instance

    def deselect(self):
        self._state = 0

    @classmethod
    def tool_layer(cls):
        return ToolLayer.null

    @classmethod
    def buttonIcon(cls):
        return QtGui.QPixmap(os.path.join(art_dir, "temp.svg")).scaledToWidth(64)


    @classmethod
    def altText(cls):
        return "Prototype tool template text"

    def link_to_widget(self, widg:ToolWidget):
        """
        Connects an instance of this tool to an instance of the widget that configures it. 
        """
        self._widget_instance = widg

    @classmethod
    def widget(self):
        """
        returns the widget Class that can configure this tool 
        """
        return ToolWidget

    @property 
    def state(self)->int:
        return self._state

    def set_state(self, state:int)->None:
        self._state = state

    def primary_mouse_depressed(self,event):
        """
        Called when the right mouse button is depressed 

        @param event 
        """
        return NullAction()
    def primary_mouse_released(self, event):
        """
        This is called when the right mouse button is released from a localized click. 

        @param event - location of release
        """
        return NullAction()
    def primary_mouse_held(self,event ):
        """
        Called continuously while the right mouse button is moved and depressed 

        @param event - current mouse location
        @param setp  - vector pointing from last called location to @place
        """
        return NullAction()
    def secondary_mouse_held(self, event):
        """
        Called continuously while the right mouse button is moved and depressed 
        """
        return NullAction()
    def double_click_event(self, event):
        return NullAction()
    def secondary_mouse_released(self, event ):
        """
        Left click released event, used to select something

        @param event - Qt event object. has where the mouse is
        """
        return NullAction()
    def mouse_moved(self, event):
        """
        Called continuously while the mouse is in the widget

        @param place - where the mouse is 
        """
        if self.highlight:
            loc = hex_to_screen(screen_to_hex(event.scenePos()))
            self._polygon = Hex(loc)

        return NullAction()
    def drop(self):
        """
        Called when this tool is being replaced. Cleans up anything it has drawn and should get rid of (like, selection circles). This is needed when closing one of the guis 
        """
        pass

    def get_context_options(self,event):
        """
        Function called by the clicker control requesting a list of context menu options, from the active tool, at the cursor. 
        The tool returns a list containing a string for each viable option
        """
        return([])
    def __str__(self):
        return("BasicTool of type {}".format(type(self)))
