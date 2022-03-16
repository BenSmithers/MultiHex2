from MultiHex2.tools.basic_tool import Basic_Tool

import os

from PyQt5 import QtGui
from actions.baseactions import NullAction

from tools.basic_tool import ToolLayer


art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')

class EntitySelector(Basic_Tool):
    """
        Generic tool for placing and selecting entitites. When it's in state zero, double-clicking on an entity will allow for editing the entity. 
        When it's in its one-state, it allows for placing its kinda entity. 

        We'll have one of these for 
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "select_location.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "select_location.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "Entity selector tool"

class AddEntityTool(EntitySelector):
    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "new_location.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "new_location.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "Create new location"

class AddSettlement(EntitySelector):
    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "new_settle.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "new_settle.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "Create new settlement"