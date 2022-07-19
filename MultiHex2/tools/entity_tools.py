"""
In this file we define the tools used to make and edit entities

We also define the widget/gui that is used to do that.
"""
from MultiHex2.tools.basic_tool import Basic_Tool
from MultiHex2.core import HexID, screen_to_hex, Entity
from MultiHex2.actions.baseactions import MetaAction, NullAction
from MultiHex2.actions.entityactions import *
from MultiHex2.core.map_entities import Settlement
from MultiHex2.tools.basic_tool import ToolLayer

import os
from copy import copy

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsSceneEvent



art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')


class EntityDialogGUI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600,400)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")

        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Entity Editor"))

class EntityDialog(QtWidgets.QDialog):
    """
    This widget is opened up when we're 
        - making a new entity, or
        - editing an existing entity 

    It adds tabs to itself according to what kind of entity is worked with. 
    When this is "accepted" it packages up and stores an action, which can be accepted later
    """
    def __init__(self,parent, config_object:Entity):
        super(EntityDialog, self).__init__(parent)
        self.ui = EntityDialogGUI()
        self.ui.setupUi(self)
        self.parent = parent

        self.ui.buttonBox.accepted.connect(self.accept)
        self.accepted = False

        if not isinstance(config_object, Entity):
            raise TypeError("Cannot configure {} object!".format(type(config_object)))
  
        
        self._configuring = config_object
        self._action = NullAction()
        self._tabs = []
        
        # this returns a list of widgets, each of which gets its own tab! 
        widget_list = config_object.widget(config_object)
        for entry in widget_list:
            newtab = QtWidgets.QWidget(self)
            
            layout = QtWidgets.QVBoxLayout(newtab)
            this_widg = entry(newtab, config_object)
            newtab.setObjectName( this_widg.objectName() )
            layout.addWidget(this_widg)
            newtab.setLayout(layout)

            self._tabs.append(this_widg)
            self.ui.tabWidget.addTab(newtab, this_widg.objectName())
        
    @property
    def action(self):
        return self._action

    def accept(self):
        self.accepted=True
        for i_tab in range(len(self._tabs)):
            self._tabs[i_tab].apply_to_entity(self._configuring)

        super().accept()


class EntitySelector(Basic_Tool):
    """
        Generic tool for placing and selecting entitites. When it's in state zero, double-clicking on an entity will allow for editing the entity. 
        When it's in its one-state, it allows for placing its kinda entity. 

        We'll have one of these for 
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._creation_type = Entity

    @classmethod
    def tool_layer(cls):
        return ToolLayer.civilization

    def primary_mouse_released(self, event:QGraphicsSceneEvent):
        if self.state==1: # placing state
            loc = event.scenePos()
            coords = screen_to_hex(loc)
            new_entity = self._creation_type("New Entity")

            self.dialog = EntityDialog(parent=None,config_object=new_entity)
            self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.dialog.exec_()
            
            self.set_state(0)
            if self.dialog.accepted:
                eID = self.parent.nextFreeEID()
                
                return New_Entity_Action(eid=eID, entity=new_entity,coords=coords)

        return NullAction()

    def secondary_mouse_released(self, event:QGraphicsSceneEvent):
        if self.state==0:
            loc = event.scenePos()
            coords = screen_to_hex(loc)
            eids_here = self.parent.eIDs_at_hex(coords)

        return NullAction()

    def double_click_event(self, event:QGraphicsSceneEvent):
        """
        When we double click, if there's only one entity we immediately open up a config window. 
        This is used to configure a duplicate of the entity there. 

        Then we return an Action that swaps the configured duplicate with the old entity. 
        """
        if self.state==0:
            loc = event.scenePos()
            coords = screen_to_hex(loc)

            eids_here = self.parent.eIDs_at_hex(coords)
            if len(eids_here)==1:
                this_ent = self.parent.accessEid(eids_here[0])

                backup = copy(this_ent)
                self.dialog = EntityDialog(parent=None, config_object=backup)
                self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                self.dialog.exec_()

                if self.dialog.accepted:
                    return Edit_Entity_Action(eID=eids_here[0], old=this_ent, new=backup)

        return NullAction()

    @property
    def entityShadow(cls):
        raise NotImplementedError("User derived class.")

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
        self._creation_type = Entity
        self.auto_state=1
        self.highlight_icon = "location"
        self.set_state(1)

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
        self._creation_type = Settlement
        self.auto_state=1
        self.set_state(1)
        self.highlight_icon="town"

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "new_settle.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "new_settle.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "Create new settlement"

class MobileSelector(Basic_Tool):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.auto_state = 1
        self._selected = -1 # none 

    def primary_mouse_released(self, event):
        """
            If try selecting a mobile here
        """
        return NullAction()

    def secondary_mouse_released(self, event):
        """
            If nothing selected, do nothing. 
            If something is selected, queue a route for it     
        """
        if self._selected == -1:
            return NullAction()
        else:
            # route! 
            pass 

        return NullAction()

    @classmethod
    def tool_layer(cls):
        return ToolLayer.mapuse
    @classmethod
    def altText(cls):
        return "Mobile Selector Tool"

class NewMobile(MobileSelector):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.auto_state = 2

    