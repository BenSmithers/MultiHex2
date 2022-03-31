import os
from enum import Enum

from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsScene, QWidget

from MultiHex2.tools.widgets import ToolWidget
from MultiHex2.actions import NullAction

art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')

class ToolLayer(Enum):
    null = 0
    terrain = 1
    civilization = 2
    mapuse = 4

class Basic_Tool:
    
    """
    Prototype a basic tool. We use this for consistent typing and templated functions. 
    
    So, you know, like why anyone else would use class inheritance 
    """
    def __init__(self, parent=None):
        if not (isinstance(parent, QGraphicsScene) or (parent is None)):
            raise TypeError("Parent should be of type {}, not {}".format(QGraphicsScene, type(parent)))
        self.parent = parent
        self._state = 0
        self.highlight = False # highlight space under the cursor 

        self.auto_state = 0 # automatically set to this state when selected
        self.highlight_icon = ""

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

    @classmethod
    def widget(self):
        """
        returns the widget that can configure this tool 
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
