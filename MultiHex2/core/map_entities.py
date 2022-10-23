"""
Here, we define various map Entities and their associated Widgets 

The basic principle is that we have multiple primitive properties defined in here, and map objects will inherit 
from multiple to get whichever properties they need. 

We also define the widgets used to configure those primitive properties in here
"""
from PyQt5 import QtWidgets, QtGui, QtCore

from MultiHex2.core.enums import OverlandRouteType
from MultiHex2.core.coordinates import DRAWSIZE, HexID

from glob import glob
import os
from math import sqrt
from copy import deepcopy

ARTDIR = os.path.join( os.path.dirname(__file__),'..', 'assets', )

class IconLib:
    """
        A library for pre-loading all the icons we'll be using. This is used by the clicker tool for drawing the entities 

        Modules can provide a folder of icons which can overwrite (and add to) the default set of icons
    """
    def __init__(self, module_folder=""):
        self._pictures = glob(os.path.join(ARTDIR, "map_icons", "*.svg"))
        self._module_folder = module_folder
        
        self.reload()

    def set_module(self, module_folder):
        if not os.path.exists(module_folder):
            raise IOError("Module folder does not exist: {}".format(module_folder))
        self._module_folder = module_folder
        self.reload()

    def reload(self):
        self._pixmaps = {}        
        for each in self._pictures:
            name = os.path.split(each)[1].split(".")[0]

            self._pixmaps[name] = QtGui.QPixmap(each)

        if self._module_folder!="":
            module_overwrite = glob(os.path.join(self._module_folder, "*"))
            for each in module_overwrite:
                name = os.path.split(each)[1].split(".")[0]
                print("added {}".format(name))
                self._pixmaps[name] = QtGui.QPixmap(each)

    def all_names(self):
        return list(self._pixmaps.keys())

    def __iter__(self):
        return self._pixmaps.__iter__()

    def access(self, name:str, width=-1)->QtGui.QPixmap:
        if name not in self._pixmaps:
            raise ValueError("Requested {} pixmap, don't see it! Have {}".format(name, self._pixmaps.keys()))

        if width==-1:
            return self._pixmaps[name].scaledToWidth(DRAWSIZE*1.5)
        else:
            return self._pixmaps[name].scaledToWidth(width)



class Entity:
    """
    Defines static entity that can be placed on a Hex
    """
    def __init__(self, name:str, location = None ):
        """
        @param name     - String. name of this entity
        @param location - HexID. Where this entity is placed. (optional. Entites can be off the map)
        """

        if not type(name)==str:
            raise TypeError("Arg 'name' must be {}, received {}".format(str, type(name)))
        self.name        = name
        self.description = ""
        self.icon        = "location"

    @staticmethod
    def widget(self):
        return [EntityWidget]

    @classmethod
    def type_name_converter(cls, type_name:str)->'Entity':
        if type_name=="Entity":
            return Entity
        elif type_name=="Government":
            return Government
        elif type_name=="Settlement":
            return Settlement
        else:
            return ValueError("Not sure how to convert type name {}".format(type_name))

    def pack(self)->dict:
        this_dict = {}
        this_dict["name"] = self.name
        this_dict["description"] = self.description
        this_dict["icon"] = self.icon
        this_dict["type"] = "Entity"
        return this_dict

    @classmethod
    def unpack(cls, this_dict)->'Entity':
        new_one = cls(this_dict['name'])
        new_one.icon = this_dict["icon"]
        new_one.description = this_dict["description"]
        return new_one


class GenericTab(QtWidgets.QWidget):
    def __init__(self, parent, iconLib:IconLib, config_entity=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.iconlib = iconLib
        if not isinstance(config_entity, Entity):
            raise TypeError("Expected {}, got {}".format(Entity, type(config_entity)))

    def apply_to_entity(self, entity:Entity)->Entity:
        """
        Gets the 
        """
        return(entity)

    def configure_with(self, entity:Entity):
        """
        Configures the widget according to the given Entity parameters
        """
        return


class EntityWidget(GenericTab):
    def __init__(self,  parent, iconLib:IconLib, config_entity=None):
        GenericTab.__init__(self,parent,iconLib, config_entity)
        self.setObjectName("EntityWidget")

        self.iconlib = iconLib

        if isinstance(self, MobileWidget):
            self.ARTDIR = os.path.join(ARTDIR, 'mobiles')
        else:
            self.ARTDIR = os.path.join(ARTDIR, 'map_icons')

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        # build the name label depending on the mode this is being built in
        font = QtGui.QFont()
        font.setPointSize(24)
        self.entity_name = QtWidgets.QLineEdit(self)
        self.entity_name.setObjectName("entity_name")
        self.entity_name.setFont(font)
        self.entity_name.setText("temp")

        self.verticalLayout.addWidget(self.entity_name)
        self.central_panes = QtWidgets.QHBoxLayout()
        self.left_pane = QtWidgets.QFormLayout()
        line = 0
        if isinstance(self, MobileWidget):
            self.speed_lbl = QtWidgets.QLabel(self)
            self.speed_lbl.setObjectName("speed_lbl")
            self.speed_lbl.setText("Speed:")
            self.left_pane.setWidget(line, QtWidgets.QFormLayout.LabelRole, self.speed_lbl) #FieldRole SpanningRole
            self.speed_edit = QtWidgets.QDoubleSpinBox(self)
            self.speed_edit.setObjectName("speed_edit")
            self.speed_edit.setMinimum(0)
            self.speed_edit.setSingleStep(0.1)
            self.speed_edit.setDecimals(1)
            self.speed_edit.setMaximum(100.)
            self.left_pane.setWidget(line, QtWidgets.QFormLayout.FieldRole, self.speed_edit)
            line+=1

        self.description_lbl = QtWidgets.QLabel(self)
        self.description_lbl.setObjectName("description_lbl")
        self.description_lbl.setText("Description: \n")
        
        self.left_pane.setWidget(line, QtWidgets.QFormLayout.LabelRole, self.description_lbl)
        line+=1
        self.description_edit = QtWidgets.QTextEdit(self)
        self.description_edit.setObjectName("description_edit")
        self.description_edit.setMinimumWidth(350)
        self.description_edit.setMinimumHeight(400)

        self.left_pane.setWidget(line, QtWidgets.QFormLayout.SpanningRole, self.description_edit)
        self.right_pane = QtWidgets.QVBoxLayout()
        self.icon_combo = QtWidgets.QComboBox(self)
        self.icon_combo.setObjectName("icon_combo")

        self.pictures = glob(os.path.join(self.ARTDIR, "*.svg"))


        for name in self.iconlib.all_names():
            self.icon_combo.addItem( QtGui.QIcon(self.iconlib.access(name)), name )

        self.picture_box = QtWidgets.QLabel(self)
        self.picture_box.setObjectName("picture_box")
        # self.picture_box.setPixmap(QtGui.QPixmap(os.path.join(self.ARTDIR,self.pictures[self.icon_combo.currentIndex()])).scaledToHeight(300))
        self.picture_box.setPixmap( self.iconlib.access( self.icon_combo.currentText(), 400 ))

        self.right_pane.addWidget(self.picture_box)
        self.right_pane.addWidget(self.icon_combo)
        # Picture spot

        self.central_panes.addItem(self.left_pane)
        self.central_panes.addItem(self.right_pane)
        self.verticalLayout.addItem(self.central_panes)

        self.icon_combo.currentIndexChanged.connect(self.combo_change)

        if config_entity is not None:
            self.configure_with(config_entity)

        #self.left_pane.setWidget(line, QtWidgets.QFormLayout.LabelRole, self.speed_lbl) #FieldRole SpanningRole

    def combo_change(self):
        self.picture_box.setPixmap( self.iconlib.access( self.icon_combo.currentText(), 400 ) )


        #self.picture_box.setPixmap(self. .scaledToWidth(400) )

    def apply_to_entity(self, entity):
        """
        Takes an entity and applies the GUIs current configuration to it

        returns the modified entity 
        """
        GenericTab.apply_to_entity(self, entity)

        entity.name = self.entity_name.text()
        entity.description = self.description_edit.toPlainText()
        entity.icon = self.icon_combo.currentText()
        return(entity)



    def configure_with(self, entity):
        """
        Gets the configuration of the entity provided, and uses that to configure the gui

        returns void
        """
        GenericTab.configure_with(self, entity)

        self.entity_name.setText(entity.name)
        self.description_edit.setText(entity.description)
        which = self.icon_combo.findText( entity.icon )
        if which==-1:
            print("Could not find icon of name: {}".format(entity.icon))
        else:
            self.icon_combo.setCurrentIndex(which)

class GovernmentWidget(GenericTab):
    def __init__(self, parent, iconLib:IconLib, config_entity=None):
        GenericTab.__init__(self, parent, iconLib, config_entity)
        self.setObjectName("GovernmentWidget")

        self.formlayout = QtWidgets.QFormLayout(self)

        self.orderlbl = QtWidgets.QLabel(self)
        self.orderlbl.setObjectName("orderlbl")
        self.orderlbl.setText("Order: ")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.orderlbl)
        self.orderbar = QtWidgets.QSlider(self)
        self.orderbar.setOrientation(QtCore.Qt.Horizontal)
        self.orderbar.setObjectName("orderbar")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.orderbar)

        self.warlbl = QtWidgets.QLabel(self)
        self.warlbl.setObjectName("warlbl")
        self.warlbl.setText("War: ")
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.warlbl)
        self.warbar = QtWidgets.QSlider(self)
        self.warbar.setOrientation(QtCore.Qt.Horizontal)
        self.warbar.setObjectName("warbar")
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.warbar)

        self.spiritlbl = QtWidgets.QLabel(self)
        self.spiritlbl.setObjectName("spiritlbl")
        self.spiritlbl.setText("Spirit: ")
        self.formlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.spiritlbl)
        self.spiritbar = QtWidgets.QSlider(self)
        self.spiritbar.setOrientation(QtCore.Qt.Horizontal)
        self.spiritbar.setObjectName("spiritbar")
        self.formlayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spiritbar)

        self.configure_with(config_entity)

    def apply_to_entity(self, entity):
        GenericTab.apply_to_entity(self, entity)
        if not isinstance(entity, Government):
            raise TypeError("Expected {}, got {}".format(Government, type(entity)))

        entity.set_war(self.warbar.value()/100.)
        entity.set_spirit(self.spiritbar.value()/100.)
        entity.set_order(self.orderbar.value()/100.)
        return(entity)

    def configure_with(self, entity):
        GenericTab.configure_with(self, entity)
        if not isinstance(entity, Government):
            raise TypeError("Expected {}, got {}".format(Government, type(entity)))

        self.warbar.setValue(entity.war*100)
        self.spiritbar.setValue(entity.spirit*100)
        self.orderbar.setValue(entity.order*100)

class Government():
    """
    A Generic implementation of 'government.' Intended to not be used on its own, but as a parent class to other objects. 
    """
    def __init__(self, order = 0.0, war = 0.0, spirit = 0.0):

        self._order = order
        self._war   = war
        self._spirit= spirit

    @property 
    def order(self):
        copy = self._order
        return(copy)
    @property 
    def war(self):
        copy = self._war
        return(copy)
    @property
    def spirit(self):
        copy = self._spirit
        return(copy)

    def set_order(self, new):
        if not ( isinstance(new,int) or isinstance(new,float)):
            raise TypeError("Invalid type {} for order, expected {}".format(type(new), float ))
        self._order =  min( 1.0, max( 0.0, new))
    def set_war(self, new):
        if not ( isinstance(new,int) or isinstance(new,float)):
            raise TypeError("Invalid type {} for war, expected {}".format(type(new), float ))
        self._war =  min( 1.0, max( 0.0, new))
    def set_spirit(self,new):
        if not ( isinstance(new,int) or isinstance(new,float)):
            raise TypeError("Invalid type {} for spirit, expected {}".format(type(new), float ))
        self._spirit =  min( 1.0, max( 0.0, new))

    @staticmethod
    def widget(cls):
        return [GovernmentWidget]

    def pack(self)->dict:
        return {
            "order":self._order,
            "war":self._war,
            "spirit":self._spirit,
            "type": "Entity"
        }

    @classmethod 
    def unpack(cls, what)->'Government':
        return cls(what["order"], what["war"], what["spirit"])


class SettlementWidget(GenericTab):
    def __init__(self, parent, iconLib:IconLib, config_entity):
        GenericTab.__init__(self, parent, iconLib, config_entity)
        self.iconlib = iconLib
        self.setObjectName("SettlementWidget")

        self.formlayout = QtWidgets.QFormLayout(self)

        self.nameedit = QtWidgets.QLineEdit(self)
        self.nameedit.setObjectName("nameedit")
        self.nameedit.setText("City Name")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.nameedit)

        self.gridLayout = QtWidgets.QGridLayout()
        self.totalPoplbl = QtWidgets.QLabel(self)
        self.totalPoplbl.setObjectName("totalPoplbl")
        self.totalPoplbl.setText("Total Population")
        self.gridLayout.addWidget(self.totalPoplbl, 0,0)
        self.totalWealthlbl = QtWidgets.QLabel(self)
        self.totalWealthlbl.setObjectName("totalWealthlbl")
        self.totalWealthlbl.setText("Total Wealth")
        self.gridLayout.addWidget(self.totalWealthlbl, 0,1)
        self.formlayout.setLayout(1, QtWidgets.QFormLayout.SpanningRole, self.gridLayout)

        self.populationlbl = QtWidgets.QLabel(self)
        self.populationlbl.setObjectName("populationlbl")
        self.populationlbl.setText("Population: ")
        self.formlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.populationlbl)
        self.populationedit = QtWidgets.QSpinBox(self)
        self.populationedit.setMaximum(1000000)
        self.populationedit.setMinimum(0)
        self.populationedit.setObjectName("populationedit")
        self.formlayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.populationedit)

        self.wealthlbl = QtWidgets.QLabel(self)
        self.wealthlbl.setObjectName("wealthlbl")
        self.wealthlbl.setText("Wealth: ")
        self.formlayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.wealthlbl)
        self.wealthedit = QtWidgets.QSpinBox(self)
        self.wealthedit.setMaximum(1000000)
        self.wealthedit.setMinimum(0)
        self.wealthedit.setObjectName("wealthedit")
        self.formlayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.wealthedit)

        self.ward_grid_layout = QtWidgets.QGridLayout()
        self.ward_label = QtWidgets.QLabel()
        self.ward_label.setObjectName("ward_label")
        self.ward_label.setText("Wards: ")
        self.ward_grid_layout.addWidget(self.ward_label, 0, 0)

        self.wardCombo = QtWidgets.QComboBox()
        self.wardCombo.setObjectName("wardCombo")
        self.ward_grid_layout.addWidget(self.wardCombo, 0, 1)
        self.ward_button = QtWidgets.QPushButton()
        self.ward_button.setObjectName("ward_button")
        self.ward_button.setText("Add New Ward")
        self.ward_button.clicked.connect(self.new_ward)
        self.ward_grid_layout.addWidget(self.ward_button,0,2)
        self.wardCombo.addItem("City Center")
        self.wardCombo.currentIndexChanged.connect(self.prep_ward_widget)

        self.ward_widget = None
        self._entity = None
        self._previous_index = -1

        self.configure_with(config_entity)

    def new_ward(self):
        new_ward = Settlement("New Ward", is_ward=True)
        self._entity.add_ward(new_ward)
        self.wardCombo.insertItem(self.wardCombo.count()-1, new_ward.name)
        self.wardCombo.setCurrentIndex(self.wardCombo.count()-2)

    def _clear_widget(self):
        if self.ward_widget is not None:
            self.formlayout.removeWidget(self.ward_widget)
            self.ward_widget.deleteLater()
            self.ward_widget = None

    def prep_ward_widget(self):
        index = self.wardCombo.currentIndex()

        if self._previous_index!=-1:
            if self.ward_widget is not None:
                self.ward_widget.apply_to_entity( self._entity.wards[self._previous_index])
                self.wardCombo.setItemText(self._previous_index, self.ward_widget.nameedit.text())

                # update the population and wealth
                self.populationedit.setValue(self._entity.partial_population)
                self.wealthedit.setValue(self._entity.partial_wealth)

        self._previous_index = index
        self._clear_widget()

        if index!=self.wardCombo.count()-1:
            # prep ward widget?
            self.ward_widget = SettlementWidget(self, self.iconlib, self._entity.wards[index])
            self.formlayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.ward_widget)

        self.totalWealthlbl.setText("Total Wealth:    {}".format(self._entity.wealth))
        self.totalPoplbl.setText("Total Population    {}".format(self._entity.wealth))

    def apply_to_entity(self, entity):
        GenericTab.apply_to_entity(self, entity)
        if not isinstance(entity, Settlement):
            raise TypeError("Expected {}, got {}".format(Settlement, type(entity)))

        entity.name = self.nameedit.text()
        entity.set_population(self.populationedit.value(), 0)
        entity.set_wealth(self.wealthedit.value(), 0)

        return(entity)

    def configure_with(self, entity):
        GenericTab.configure_with(self, entity)
        if not isinstance(entity, Settlement):
            raise TypeError("Expected {}, got {}".format(Settlement, type(entity)))
        self._entity = entity
        self.nameedit.setText(entity.name)
        self.wealthedit.setValue(entity.partial_wealth) 
        self.populationedit.setValue(entity.partial_population)

        if not entity._is_ward:
            self.formlayout.setLayout(4, QtWidgets.QFormLayout.SpanningRole, self.ward_grid_layout)
            for ward in entity.wards:
                self.wardCombo.insertItem(self.wardCombo.count()-1, ward.name)
        
        self.totalWealthlbl.setText("Total Wealth:    {}".format(self._entity.wealth))
        self.totalPoplbl.setText("Total Population    {}".format(self._entity.wealth))

class Settlement(Entity, Government):
    """
    Generic implementation for settlements of people. Can be applied for space stations, planets, towns, or anything really. Maintains a total population and its demographics. 

    Settlements can be divided into `wards` to represent sub-sections of the 
    """
    def __init__(self, name, location=None, is_ward=False):
        Entity.__init__(self, name, location)
        Government.__init__(self)

        self.icon = "town"

        # these values are assigned to the city-center 
        self._population = 1
        self._wealth = 1

        self._wards = [ ]
        self._is_ward = is_ward

        # this only describes the population directly contained by the _population attribute
        self._demographics = { 'racial': { 'human': 1.00 } }

    def pack(self)->dict:
        """
            We get the pack-dicts for Entity, government, and then combine them 
        """
        e_dict = Entity.pack(self)
        g_dict = Government.pack(self)

        for key in g_dict.keys():
            e_dict[key] = g_dict[key]

        e_dict["population"] = self._population
        e_dict["wealth"] = self._wealth
        e_dict["is_ward"] = self._is_ward
        e_dict["demographics"] = self._demographics
        e_dict["wards"] = [ward.pack() for ward in self.wards]
        e_dict["type"] = "Settlement"
        return e_dict
    
    @classmethod
    def unpack(cls, this_dict) -> 'Settlement':
        """
            Multiple inheritance weirdness! Here, it'll call `unpack` on Entity, unpacking those elements but making a Settlement object 
        """
        this_obj = super().unpack(this_dict)
        this_obj._war = this_dict["war"]
        this_obj._spirit = this_dict["spirit"]
        this_obj._order = this_dict["order"]
        this_obj._population = this_dict["population"]
        this_obj._wealth = this_dict["wealth"]
        this_obj._is_ward = this_dict["is_ward"]
        this_obj._demographics = this_dict["demographics"]
        this_obj._wards = [Settlement.unpack(entry) for entry in this_dict["wards"]]

        return this_obj

    @property
    def wards(self)->'list[Settlement]':
        return self._wards

    @property
    def tension(self):

        if len(self.wards)==0:
            return(0)
        else:
            # get averages! 
            avg_ord = (self.partial_population/self.population)*self.order/(1+len(self.wards))
            avg_war = (self.partial_population/self.population)*self.war/(1+len(self.wards))
            avg_spi = (self.partial_population/self.population)*self.spirit/(1+len(self.wards))

            for ward in self.wards:
                avg_ord += (ward.population/self.population)*ward.order/(1+len(self.wards))
                avg_war += (ward.population/self.population)*ward.war/(1+len(self.wards))
                avg_spi += (ward.population/self.population)*ward.spirit/(1+len(self.wards))

            wip = (self.partial_population/self.population)*( ( avg_ord - self.order)**2 + (avg_war - self.war)**2 + (avg_spi - self.spirit)**2)
            for ward in self.wards:
                wip += (ward.population/self.population)*((avg_ord - ward.order)**2 + (avg_war - ward.war)**2 + (avg_spi - ward.spirit)**2)

            wip = sqrt(wip)
            return( wip )


    @property
    def demographics(self):
        """
        Returns a copy of this object's demographics! 
        """
        copy = deepcopy( self._demographics )
        return( copy )

    def set_demographics(self, new_demo):
        if not self._valid_demo_structure( new_demo ):
            raise TypeError("Improperly formatted demographics object!")
        
        self._demographics = new_demo
        self._norm_demographics()

    @staticmethod
    def widget(self):
        return Entity.widget(self)+Government.widget(self)+[SettlementWidget]

    def get_demographics_as_str(self):
        """
        Returns an entry in the demographics object formated in the ward-dialog style. Must specify a ward and the demographic
        """
  
        out = ""
        for key in self._demographics:
            out += "+{}\n".format(key)
            for subkey in self._demographics[key]:
                out+= "{}:{:.4f}\n".format(subkey, self._demographics[key][subkey])
        return(out)


    @property
    def partial_wealth(self):
        """
        returns just the wealth belonging to the 'city center'. Does not include any ward wealth
        """
        return(self._wealth)

    @property
    def partial_population(self):
        """
        returns just the wealth belonging to the city center
        """
        return(self._population)

    def set_wealth(self,new_wealth, which_ward=None):
        diff = new_wealth - self.wealth

        self.add_wealth( diff, which_ward )

    def add_wealth( self, amount, which_ward = None):
        """
        Adds an amount of wealth to the settlement. If no ward is specified, it spreads the wealth according to populations 
        """
        if which_ward is None:
            self._wealth += int(amount*float(self._population)/self.population)
            for ward in self.wards:
                ward.add_wealth( int(amount*float(ward.population)/self.population))
        else:
            if not isinstance( which_ward, int):
                raise TypeError("Expected type {} for ward, got {}".format(int, type(which_ward)))

            if which_ward == 0:
                self._wealth += amount
            else:
                lowered = which_ward - 1
                self.wards[lowered].add_wealth( amount )

    @property
    def wealth(self):
        """
        returns all the wealth of all the wards combined 
        """
        total_wealth = self._wealth
        for ward in self.wards:
            total_wealth+= ward._wealth
        return(total_wealth)

    def add_ward( self, new_ward ):
        """
        Adds a ward to this settlement's list, such that it is now a part of this Settlement. 
        """

        if not isinstance(new_ward, Settlement):
            raise TypeError("Arg `new_ward` is type {}, expected {}".format(type(new_ward), Settlement))

        new_ward._is_ward = True
        self._wards.append( new_ward )

    def _valid_demo_structure( self, demo ):
        """
        Verifies that the passed demographics object is of the proper structure.

        We're expecting a dictionary containing dictionaries.
        """

        if type(demo)!=dict:
            return(False)
        else:
            for key in demo:
                if type( demo[key]) != dict :
                    return(False) 
        
        # ensure the demographics thing is normalized 
        for key in demo:
            total = 0.0
            for subkey in demo[key]:
                total += demo[key][subkey]

            if abs(total-1.0)>0.001:
                return(False)

        return(True)

    def _norm_demographics( self ):
        """
        Normalize the demographics dictionary! 
        """
        for key in self._demographics:
            total = 0.
            for subkey in self._demographics[key]:
                total += self._demographics[key][subkey]

            for subkey in self._demographics[key]:
                self._demographics[key][subkey] /= total
        
    def add_population(self, to_add, which_ward=None, demographics = None):
        """
        Adds population to the Settlement. If no ward is specified, it divides added population evently between the wards.  

        To specify wards are enumerated starting at 1. The 0-Ward is the city-center. 
        """
        if (demographics is not None) and (not self._valid_demo_structure( demographics )):
            raise ValueError("Arg 'demographics' is not structured properly.")
        else:
            if demographics is not None:
                # populate the dictionaries such that the keys are symmetric  
                for key in demographics:
                    if key not in self._demographics:
                        self._demographics[key] = {}
                    for subkey in demographics[key]:
                        if subkey not in self._demographics[key]:
                            self._demographics[key][subkey] = 0.0
                for key in self._demographics:
                    if key not in demographics:
                        demographics[key] = {}
                    for subkey in self._demographics[key]:
                        if subkey not in demographics[key]:
                            demographics[key][subkey] = 0.0

        # update the demographics of the main part of town 
        if demographics is not None:
            # update the demographics
            for key in self._demographics:
                for subkey in self._demographics[key]:
                    self._demographics[key][subkey] = (self._demographics[key][subkey]*self._population + demographics[key][subkey]*to_add)/( self._population + to_add )
                    if self._demographics[key][subkey] < 0:
                        self._demographics[key][subkey] = 0.0 

        if which_ward is None:
            if len(self.wards)==0:                
                self._population += to_add
                assert( self._population >= 0 )

            else:
                # keep track of number added to avoid rounding errors. Just put any extras in the main ward
                added = 0 
                pre_population = self.population

                added            += int(to_add*float(self._population)/pre_population)
                self._population += int(to_add*float(self._population)/pre_population)

                for ward in self.wards:
                    added   +=           int(to_add*float(ward.population)/pre_population)
                    ward.add_population( int(to_add*float(ward.population)/pre_population), demographics=demographics )
                    
                if added!=to_add:
                    self._population += ( to_add - added )
        else:
            if which_ward<0:
                raise ValueError("Invalid ward no. {}".format(which_ward))
            elif which_ward==0:
                self._population += to_add
            else:
                which_ward -= 1
                if which_ward>=(len(self.wards)):
                    raise ValueError("No ward of number {}".format(which_ward))
                else:
                    self.wards[which_ward].add_population( to_add, demographics = demographics )
        
        self._norm_demographics()

    def set_population(self, population, which_ward=None ):
        """
        Sets the population of the settlement to the given amount 
        """
        assert( isinstance( population, int))
        assert( population >= 0 )
        
        to_add = population - self.population
        self.add_population( to_add, which_ward=which_ward )

    @property
    def population(self):
        pop = self._population
        for ward in self.wards:
            pop += ward.population
        return( pop )
        
    @property
    def size( self ):
        """
        Returns a string representing the effective size of the Settlement 
        """
        return("")

    def __str__(self):
        """
        Returns a string describing the settlement. Used implicitly with Python's print function
        """
        output = ""
        if self._is_ward:
            output += "    "

        output  += "{}: A {} of total poulation {}. ".format( self.name, self.size, self.population )
        if (not self._is_ward) and len(self.wards)!=0:
            output += "City Center Demographics...\n"
        else:
            output += "Demographics are...\n"
        for key in self._demographics:
            if self._is_ward:
                output += "    "
            output += "{}:\n".format( key[0].upper()+key[1:] )
            for subkey in self._demographics[key]:
                if self._is_ward:
                    output += "    "
                output += "    {:.2f}% {}\n".format( 100*self._demographics[key][subkey], subkey[0].upper()+subkey[1:])
        if len(self.wards)>0:
            output += "Contains Wards...\n"
            for ward in self.wards:
                output+= ward.__str__()

        return( output )
             

class Mobile( Entity ):
    """
    Defines a mobile map Entity. Fundamentally the same as an Entity, but its location can be moved. 
    Also carries with it a speed (hexes/day), and how it can move (walks/swims/flies)
    """
    def __init__(self, name:str):
        Entity.__init__(self, name)
        
        self._speed = 1. #hexes/day 
        self._walks = True
        self._swims = False
        self._flies = False
        self.icon = "walker"

    def pack(self) -> dict:
        this_dict = super().pack()
        this_dict["type"]="mobile"
        this_dict["walks"]=self._walks
        this_dict["swims"]=self._swims
        this_dict["flies"]=self._flies
        this_dict["speed"]=self._speed
        return this_dict

    @classmethod
    def unpack(cls, this_dict) -> 'Mobile':
        obj = super().unpack(this_dict)
        obj._speed = this_dict["speed"]
        obj._walks = this_dict["walks"]
        obj._swims = this_dict["swims"]
        obj._flies = this_dict["flies"]

        return obj

    @property
    def walks(self):
        return self._walks
    
    @property
    def swims(self):
        return self._swims

    @property
    def flies(self):
        return self._flies

    def get_route_type(self):
        if self._flies:
            return OverlandRouteType.aerial
        print("making {}".format(OverlandRouteType(int(self._walks) + 2*int(self._swims))))
        return OverlandRouteType(int(self._walks) + 2*int(self._swims))

    @property 
    def speed(self):
        return(self._speed)

    def set_speed(self, new_speed):
        if not (isinstance(new_speed,float) or isinstance(new_speed,int)):
            raise TypeError("Expected {}, got {}".format(float, type(new_speed)))
        if new_speed <= 0.:
            raise ValueError("Need positive speed, got {}".format(new_speed))

        self._speed = new_speed


class MobileWidget(EntityWidget):
    def __init__(self,parent, iconLib:IconLib, config_entity=None):
        EntityWidget.__init__(self,parent, iconLib, config_entity)
    
        self.configure_with(config_entity)
