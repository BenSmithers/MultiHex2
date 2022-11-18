from MultiHex2.core.map_entities import GenericTab, IconLib, Entity
from MultiHex2.core.map_entities import Settlement

from PyQt5 import QtWidgets, QtGui

from enum import Enum

from .tables import atmo, temp, pop, tl, bio
from MultiHex2.modules.swon.enums import WorldCategory, WorldTag

#TODO add buttons for adding/removing worlds 

class EnumEntry(QtWidgets.QWidget):
    def __init__(self, entry:Enum, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setObjectName("EnumEntry")

        self.hlayout = QtWidgets.QHBoxLayout(self)
        self.hlayout.setObjectName("hlayout")

        self.label =QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.label.setText(entry.name)
        print(self.label.text())

        undoicon = QtGui.QIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        #  QIcon(QApplication.style().standardIcon(QStyle.SP_DialogCancelButton)
        #QtWidgets.QStyle.SP_DialogCancelButton
        self.button = QtWidgets.QPushButton(self)
        self.button.setIcon(undoicon)
        self.button.setMaximumWidth(32)
        self.hlayout.addWidget(self.button)
        self.hlayout.addWidget(self.label)


        self.button.clicked.connect(self.clicky)

    def clicky(self):
        print("clicky")



class SystemWidget(GenericTab):
    def __init__(self, parent, iconLib:IconLib,config_entity=None):
        GenericTab.__init__(self, parent, iconLib, config_entity)

        self.setObjectName("SystemWidget")

        self.hlayout = QtWidgets.QHBoxLayout(self)
        self.hlayout.setObjectName("hlayout")

        self.tabs=  QtWidgets.QTabWidget(self)
        self.tabs.setObjectName("tabs")
        self.hlayout.addWidget(self.tabs)
        self._tabs_contents = []

        self.configure_with(config_entity)

    def configure_with(self, entity:Settlement):
        """
        Configures the widget according to the given Entity parameters
        """
        self.tabs.clear()
        self._tabs_contents = []
        for ward in entity.wards:
            new_page = WorldWidget(self, self.iconlib, ward)
            self.tabs.addTab(new_page, ward.name)
            self._tabs_contents.append(new_page)

    def apply_to_entity(self, entity:Settlement)->Settlement:
        """
        Gets the 
        """

        entity._wards = [self._tabs_contents[i].apply_to_entity(entity.wards[i]) for i in range(len(entity.wards)) ]

        return(entity)

class WorldWidget(GenericTab):
    def __init__(self, parent, iconLib:IconLib,config_entity=None):
        GenericTab.__init__(self, parent, iconLib, config_entity)

        self.setObjectName("WorldWidget")

        self.formlayout = QtWidgets.QFormLayout(self)
        self.formlayout.setObjectName("formlayout")

        self.name_lbl=QtWidgets.QLabel(self)
        self.name_lbl.setObjectName("name_lbl")
        self.name_lbl.setText("Notes: ")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.name_lbl)
        self.name_entry=QtWidgets.QLineEdit(self)
        self.name_entry.setObjectName("name_entry")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_entry)
        

        # atmo, temp, bio, population (raw), tl 
        self.atm_label = QtWidgets.QLabel(self)
        self.atm_label.setObjectName("atm_label")
        self.atm_label.setText("Atmosphere: ")
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.atm_label)
        self.atm_spin = QtWidgets.QSpinBox(self)
        self.atm_spin.setObjectName("atm_spin")
        self.atm_spin.setMinimum(2)
        self.atm_spin.setMaximum(12)
        self.atm_spin.setValue(7)
        self.formlayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.atm_spin)
        self.atm_word = QtWidgets.QLabel(self)
        self.atm_word.setObjectName("atm_word")
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.atm_word)

        self.pop_label = QtWidgets.QLabel(self)
        self.pop_label.setObjectName("pop_label")
        self.pop_label.setText("Population: ")
        self.formlayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pop_label)
        self.pop_spin = QtWidgets.QSpinBox(self)
        self.pop_spin.setObjectName("pop_spin")
        self.pop_spin.setMinimum(2)
        self.pop_spin.setMaximum(12)
        self.pop_spin.setValue(7)
        self.formlayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.pop_spin)
        self.pop_word = QtWidgets.QLabel(self)
        self.pop_word.setObjectName("pop_word")
        self.formlayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pop_word)

        self.bio_label = QtWidgets.QLabel(self)
        self.bio_label.setObjectName("bio_label")
        self.bio_label.setText("Biosphere: ")
        self.formlayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.bio_label)
        self.bio_spin = QtWidgets.QSpinBox(self)
        self.bio_spin.setObjectName("bio_spin")
        self.bio_spin.setMinimum(2)
        self.bio_spin.setMaximum(12)
        self.bio_spin.setValue(7)
        self.formlayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.bio_spin)
        self.bio_word = QtWidgets.QLabel(self)
        self.bio_word.setObjectName("bio_word")
        self.formlayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.bio_word)

        self.temp_label = QtWidgets.QLabel(self)
        self.temp_label.setObjectName("temp_label")
        self.temp_label.setText("Temperature: ")
        self.formlayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.temp_label)
        self.temp_spin = QtWidgets.QSpinBox(self)
        self.temp_spin.setObjectName("temp_spin")
        self.temp_spin.setMinimum(2)
        self.temp_spin.setMaximum(12)
        self.temp_spin.setValue(7)
        self.formlayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.temp_spin)
        self.temp_word = QtWidgets.QLabel(self)
        self.temp_word.setObjectName("temp_word")
        self.formlayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.temp_word)

        self.tl_label = QtWidgets.QLabel(self)
        self.tl_label.setObjectName("tl_label")
        self.tl_label.setText("Tech Level: ")
        self.formlayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.tl_label)
        self.tl_spin = QtWidgets.QSpinBox(self)
        self.tl_spin.setObjectName("tl_spin")
        self.tl_spin.setMinimum(2)
        self.tl_spin.setMaximum(12)
        self.tl_spin.setValue(7)
        self.formlayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.tl_spin)
        self.tl_word = QtWidgets.QLabel(self)
        self.tl_word.setObjectName("tl_word")
        self.formlayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.tl_word)        

        self.notes_lbl=QtWidgets.QLabel(self)
        self.notes_lbl.setObjectName("notes_lbl")
        self.notes_lbl.setText("Notes: ")
        self.formlayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.notes_lbl)
        self.notes_entry=QtWidgets.QLineEdit(self)
        self.notes_entry.setObjectName("notes_entry")
        self.formlayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.notes_entry)

        self.tagmenu = QtWidgets.QScrollArea(self)
        self.tagmenu.setObjectName("tagmenu")

        self.taggroup = QtWidgets.QGroupBox("World Tags")

        self.tagemenulayout = QtWidgets.QVBoxLayout(self.tagmenu)
        self.tagemenulayout.setObjectName("tagmenulayout")
        
        self.tagcombo = QtWidgets.QComboBox(self)   
        for each in WorldTag:
            self.tagcombo.addItem(each.name)

        self.tagemenulayout.addWidget(self.tagcombo)


        self.tl_spin.valueChanged.connect(self.update_text)
        self.pop_spin.valueChanged.connect(self.update_text)
        self.bio_spin.valueChanged.connect(self.update_text)
        self.atm_spin.valueChanged.connect(self.update_text)
        self.temp_spin.valueChanged.connect(self.update_text)
        
        self._widges = []
        self.configure_with(config_entity)

        

    def configure_with(self, entity: Entity):
        self.tl_spin.setValue(entity.tech_level)
        self.temp_spin.setValue(entity.temperature)
        self.pop_spin.setValue(entity._population_raw)
        self.bio_spin.setValue(entity.biosphere)
        self.atm_spin.setValue(entity.atmosphere)
        self.notes_entry.setText(str(entity.title))

        for tag in entity.tags:
            new_widg = EnumEntry(tag)

            self._widges.append(new_widg)
            self.tagemenulayout.addWidget(new_widg)
        
        if False:
            tag_str = ", ".join([tag.name for tag in entity.tags])
            if tag_str!="":
                tag_str+=", "
            tag_str += ", ".join([tag.name for tag in entity.category])

            if str(entity.title)=="":
                self.notes_entry.setText(tag_str)
            else:
                self.notes_entry.setText(str(entity.title) + ", "+ tag_str)



        self.name_entry.setText(entity.name)

        self.taggroup.setLayout(self.tagemenulayout)
        self.tagmenu.setWidget(self.taggroup)

        self.formlayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.tagmenu)

        self.update_text()

    def update_text(self):
        self.atm_word.setText(atmo.access(self.atm_spin.value()))
        self.pop_word.setText(str(pop.access(self.pop_spin.value())))
        self.temp_word.setText(temp.access(self.temp_spin.value()))
        self.bio_word.setText(bio.access(self.bio_spin.value()))
        self.tl_word.setText(tl.access(self.tl_spin.value()))
    
    def apply_to_entity(self, entity: Entity) -> Entity:
        return entity