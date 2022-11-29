from MultiHex2.core.map_entities import GenericTab, IconLib, Entity
from MultiHex2.core.map_entities import Settlement

from PyQt5 import QtWidgets, QtGui, QtCore

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


class world_ui(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(649, 1000)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 615, 877))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tag_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.tag_box.setObjectName("tag_box")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tag_box)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.tag_box)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.comboBox = QtWidgets.QComboBox(self.tag_box)
        self.comboBox.setObjectName("comboBox")
        for item in WorldTag:
            self.comboBox.addItem(item.name)
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.tag_list = QtWidgets.QListWidget(self.tag_box)
        self.tag_list.setObjectName("tag_list")
        self.verticalLayout_8.addWidget(self.tag_list)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.tag_delete_button = QtWidgets.QPushButton(self.tag_box)
        self.tag_delete_button.setObjectName("tag_delete_button")
        self.horizontalLayout.addWidget(self.tag_delete_button)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addWidget(self.tag_box)
        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.world_cat_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.world_cat_box.setObjectName("world_cat_box")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.world_cat_box)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.cat_list = QtWidgets.QListWidget(self.world_cat_box)
        self.cat_list.setObjectName("cat_list")
        self.verticalLayout_9.addWidget(self.cat_list)
        self.verticalLayout_4.addWidget(self.world_cat_box)
        self.atm_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.atm_box.setObjectName("atm_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.atm_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.atm_label = QtWidgets.QLabel(self.atm_box)
        self.atm_label.setObjectName("atm_label")
        self.verticalLayout.addWidget(self.atm_label)
        self.atm_spin = QtWidgets.QSpinBox(self.atm_box)
        self.atm_spin.setObjectName("atm_spin")
        self.atm_spin.setMinimum(2)
        self.atm_spin.setMaximum(12)
        self.verticalLayout.addWidget(self.atm_spin)
        self.verticalLayout_4.addWidget(self.atm_box)
        self.bio_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.bio_box.setObjectName("bio_box")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.bio_box)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.bio_lbl = QtWidgets.QLabel(self.bio_box)
        self.bio_lbl.setObjectName("bio_lbl")
        self.verticalLayout_3.addWidget(self.bio_lbl)
        self.bio_spin = QtWidgets.QSpinBox(self.bio_box)
        self.bio_spin.setObjectName("bio_spin")
        self.bio_spin.setMinimum(2)
        self.bio_spin.setMaximum(12)
        self.verticalLayout_3.addWidget(self.bio_spin)
        self.verticalLayout_4.addWidget(self.bio_box)
        self.hydro_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.hydro_box.setObjectName("hydro_box")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.hydro_box)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.hydro_lbl = QtWidgets.QLabel(self.hydro_box)
        self.hydro_lbl.setObjectName("hydro_lbl")
        self.verticalLayout_10.addWidget(self.hydro_lbl)
        self.hydro_spin = QtWidgets.QSpinBox(self.hydro_box)
        self.hydro_spin.setObjectName("hydro_spin")
        self.hydro_spin.setMinimum(2)
        self.hydro_spin.setMaximum(12)
        self.verticalLayout_10.addWidget(self.hydro_spin)
        self.verticalLayout_4.addWidget(self.hydro_box)
        self.pop_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.pop_box.setObjectName("pop_box")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.pop_box)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pop_label = QtWidgets.QLabel(self.pop_box)
        self.pop_label.setObjectName("pop_label")
        self.verticalLayout_7.addWidget(self.pop_label)
        self.pop_spin = QtWidgets.QSpinBox(self.pop_box)
        self.pop_spin.setObjectName("pop_spin")
        self.pop_spin.setMinimum(2)
        self.pop_spin.setMaximum(12)
        self.verticalLayout_7.addWidget(self.pop_spin)
        self.verticalLayout_4.addWidget(self.pop_box)
        self.tl_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.tl_box.setObjectName("tl_box")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tl_box)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tl_label = QtWidgets.QLabel(self.tl_box)
        self.tl_label.setObjectName("tl_label")
        self.verticalLayout_6.addWidget(self.tl_label)
        self.tl_spin = QtWidgets.QSpinBox(self.tl_box)
        self.tl_spin.setObjectName("tl_spin")
        self.tl_spin.setMinimum(2)
        self.tl_spin.setMaximum(12)
        self.verticalLayout_6.addWidget(self.tl_spin)
        self.verticalLayout_4.addWidget(self.tl_box)
        self.temp_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.temp_box.setObjectName("temp_box")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.temp_box)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.temp_lbl = QtWidgets.QLabel(self.temp_box)
        self.temp_lbl.setObjectName("temp_lbl")
        self.verticalLayout_5.addWidget(self.temp_lbl)
        self.temp_spin = QtWidgets.QSpinBox(self.temp_box)
        self.temp_spin.setObjectName("temp_spin")
        self.temp_spin.setMinimum(2)
        self.temp_spin.setMaximum(12)
        self.verticalLayout_5.addWidget(self.temp_spin)
        self.verticalLayout_4.addWidget(self.temp_box)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tag_box.setTitle(_translate("Form", "World Tags"))
        self.pushButton.setText(_translate("Form", "Add Tag"))
        __sortingEnabled = self.tag_list.isSortingEnabled()
        self.tag_list.setSortingEnabled(False)
        self.tag_list.setSortingEnabled(__sortingEnabled)
        self.tag_delete_button.setText(_translate("Form", "Delete Selected"))
        self.world_cat_box.setTitle(_translate("Form", "World Categories"))
        self.atm_box.setTitle(_translate("Form", "Atmosphere"))
        self.atm_label.setText(_translate("Form", "Descriptive Words"))
        self.bio_box.setTitle(_translate("Form", "Biosphere"))
        self.bio_lbl.setText(_translate("Form", "Desc Dords"))
        self.hydro_box.setTitle(_translate("Form", "Hydrology"))
        self.hydro_lbl.setText(_translate("Form", "TextLabel"))
        self.pop_box.setTitle(_translate("Form", "Population"))
        self.pop_label.setText(_translate("Form", "TextLabel"))
        self.tl_box.setTitle(_translate("Form", "Tech Level"))
        self.tl_label.setText(_translate("Form", "TextLabel"))
        self.temp_box.setTitle(_translate("Form", "Temperature"))
        self.temp_lbl.setText(_translate("Form", "Desc aodka"))

class SummaryWidget(GenericTab):
    def __init__(self, parent, iconLib: IconLib, config_entity=None):
        super().__init__(parent, iconLib, config_entity)


class WorldWidget(GenericTab):
    def __init__(self, parent, iconLib:IconLib,config_entity=None):
        GenericTab.__init__(self, parent, iconLib, config_entity)

        self.ui = world_ui()
        self.ui.setupUi(self)

        self.ui.tl_spin.valueChanged.connect(self.update_text)
        self.ui.pop_spin.valueChanged.connect(self.update_text)
        self.ui.bio_spin.valueChanged.connect(self.update_text)
        self.ui.atm_spin.valueChanged.connect(self.update_text)
        self.ui.temp_spin.valueChanged.connect(self.update_text)
        
        self._widges = []
        self.configure_with(config_entity)

        

    def configure_with(self, entity: Entity):
        self.ui.tl_spin.setValue(entity.tech_level)
        self.ui.temp_spin.setValue(entity.temperature)
        self.ui.pop_spin.setValue(entity._population_raw)
        self.ui.bio_spin.setValue(entity.biosphere)
        self.ui.atm_spin.setValue(entity.atmosphere)

        for tag in entity.tags:
            self.ui.tag_list.addItem(tag.name)

        for cat in entity.category:
            self.ui.cat_list.addItem(cat.name)

        self.update_text()

    def update_text(self):
        self.ui.atm_label.setText(atmo.access(self.ui.atm_spin.value()))
        self.ui.pop_label.setText(str(pop.access(self.ui.pop_spin.value())))
        self.ui.temp_lbl.setText(temp.access(self.ui.temp_spin.value()))
        self.ui.bio_lbl.setText(bio.access(self.ui.bio_spin.value()))
        self.ui.tl_label.setText(tl.access(self.ui.tl_spin.value()))
    
    def apply_to_entity(self, entity: Entity) -> Entity:
        return entity