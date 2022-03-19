from MultiHex2.tools.basic_tool import Basic_Tool
from MultiHex2.core import HexID, screen_to_hex, Entity
import os

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsSceneEvent
from actions.baseactions import MetaAction, NullAction

from tools.basic_tool import ToolLayer


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
    def __init__(self,parent, config_object:Entity, new_mode:bool):
        super(EntityDialog, self).__init__(parent)
        self.ui = EntityDialogGUI()
        self.ui.setupUi(self)
        self.parent = parent

        self.ui.buttonBox.accepted.connect(self.accept)

        if not isinstance(config_object, Entity):
            raise TypeError("Cannot configure {} object!".format(type(config_object)))
        
        # yeah the syntax here is really ugly, but this function is a static method so it can also be called on 
        #  an un-instantiated class 
        
        # this returns a list of widgets, each of which gets its own tab! 

        self._configuring = config_object
        self._action = NullAction()
        self._tabs = []

        self.new_mode = new_mode

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
        all_act = []
        for i_tab in range(len(self._tabs)):
            all_act.append( self._tabs[i_tab].get_apply_action(self._configuring) )
            if self.new_mode:
                self._tabs[i_tab].apply_to(self._configuring)

        self._action = MetaAction(*all_act)


        super().accept()


class EntitySelector(Basic_Tool):
    """
        Generic tool for placing and selecting entitites. When it's in state zero, double-clicking on an entity will allow for editing the entity. 
        When it's in its one-state, it allows for placing its kinda entity. 

        We'll have one of these for 
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def primary_mouse_released(self, event:QGraphicsSceneEvent):
        if self.state==1: # placing state
            loc = event.scenePos()
            coords = screen_to_hex(loc)

            # use the dialog to make a new event! 

    def secondary_mouse_released(self, event:QGraphicsSceneEvent):
        if self.state==0:
            loc = event.scenePos()
            coords = screen_to_hex(loc)
            eids_here = self.parent.eIDs_at_hex(coords)

    def double_click_event(self, event:QGraphicsSceneEvent):
        if self.state==0:
            loc = event.scenePos()
            coords = screen_to_hex(loc)

            eids_here = self.parent.eIDs_at_hex(coords)
            if len(eids_here)==1:
                this_ent = self.parent.accessEid(eids_here[0])
                self.dialog = EntityDialog(self.parent, this_ent)
                self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                self.dialog.exec_()

                # get the action 
                return self.dialog.action


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