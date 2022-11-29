"""
Define the World class 
"""
from random import choice
import numpy as np

from .tables import bio, pop, tl, atmo, temp
from MultiHex2.core import Settlement
from MultiHex2.modules.swon.enums import WorldTag, WorldCategory, TradeGood
from MultiHex2.modules.swon.trade_goods import ALL_GOODS

WorldTag._value2member_map_.keys()


def roll(rng=None, mod=0):
    if rng is None:
        return np.random.randint(1,7)+np.random.randint(1,7)+mod
    else:
        return rng.randint(1,7) + rng.randint(1,7) + mod


def d100(rng=None):
    if rng is None:
        return np.random.randint(1,101)
    else:
        return rng.randint(1,101)

class World(Settlement):
        
    def __init__(self,name,rng=None,
                atmosphere=-1, temperature=-1,biosphere=-1,
                population=-1, tl=-1,*world_tag, **kwargs) -> None:
        if not isinstance(world_tag,(list,tuple)):
            raise TypeError("World Tags should be type {}, not {}".format(list, type(world_tag)))
        super().__init__(name, None, True)

        self.name = name

        self._fuel=False
        self.title = ""
    
        if "seed" in kwargs.keys():
            np.random.seed(kwargs["seed"])

        self._tags = []

        for entry in world_tag:
            if not isinstance(entry, WorldTag):
                raise TypeError("Cannot index with type {}, try an {}".format(type(entry, int)))
            self._tags.append(entry)

        if len(world_tag)==0:
            self._tags=[ choice(list(WorldTag)) for i in range(2) ]
        
        self._atmosphere = roll(rng) if atmosphere==-1 else atmosphere
        self._temperature = roll(rng) if temperature==-1 else temperature
        self._biosphere = roll(rng) if biosphere==-1 else biosphere
        self._population_raw = roll(rng) if population==-1 else population
        self._tech_level = roll(rng) if tl==-1 else tl
        self._hydro = roll(rng) 
        if self._atmosphere==4:
            self._hydro-=4
        if self._temperature==12:
            self._hydro-=4
        elif self._temperature>9:
            self._hydro-=2
        
        if self._hydro<2:
            self._hydro = 2

        self._population = int(pop.access(self._population_raw))*np.random.randint(1,10)
        self._category =[WorldCategory.Common,]

        self.update_category()

    def list_available_goods(self)->'set[TradeGood]':
        """
        Returns a set of available goods. We use a set here so that each entry is unique
        """
        avail = []

        for category in self._category:
            # take all the trade goods, and filter out only the ones that are available for this category 
            avail += list(filter(lambda entry: ALL_GOODS[entry].is_available(category), TradeGood ))

        avail = set(avail)

        return avail

    def get_purchase_price(self, tg:TradeGood):
        """
            Returns the purchase price of the given trade good on this world 
            Returns -1 if the good is not available here 
        """
        entry = ALL_GOODS[tg]

        if any(entry.is_available(wc) for wc in self._category ):
            return min([entry.get_purchase_price(wc) for wc in self._category])
        return -1 

    def get_sale_price(self, tg:TradeGood):
        entry = ALL_GOODS[tg]

        return max([entry.get_sale_price(wc) for wc in self._category])

    def update_category(self):
        self._category = []
        if self._atmosphere==4:
            self._category.append(WorldCategory.Asteroid)
        if self._atmosphere==6:
            if self._temperature>3 and self._temperature<10:
                if self._population_raw>4 and self._population_raw<8:
                    self._category.append(WorldCategory.Agricultural)

        if self._hydro==2 and self._atmosphere!=4:
            self._category.append(WorldCategory.Desert)
        
        if self._atmosphere==9 and self._hydro>2:
            self._category.append(WorldCategory.Fluid_Oceans)

        if self._atmosphere>=6 and self._atmosphere<=8:
            if self._hydro==7 or self._hydro==6:
                if self._temperature>=6 and self._temperature<9:
                    self._category.append(WorldCategory.Garden)
        
        if self._population_raw>9:
            self._category.append(WorldCategory.High_Pop)

        if self._tech_level==11 or self._tech_level==12:
            self._category.append(WorldCategory.High_Tech)

        if self._hydro<2 and self._temperature<4:
            self._category.append(WorldCategory.Ice_Capped)

        if self._population_raw==11:
            if self._atmosphere<11 and self._atmosphere!=2:
                self._category.append(WorldCategory.Industrial)
        
        if self._population_raw<4:
            self._category.append(WorldCategory.Low_Pop)

        if self._tech_level<6 or self._tech_level==9 or self._tech_level==10:
            self._category.append(WorldCategory.Low_Tech)

        if self._population_raw>=6 and self._population_raw<12:
            if self._hydro<5:
                if self._atmosphere<5 or self._atmosphere>10:
                    self._category.append(WorldCategory.Non_Agricultural)

            if self.temperature>=6 and self.temperature<9:
                if self._atmosphere>5 and self._atmosphere<9:
                    self._category.append(WorldCategory.Rich)
        else:
            self._category.append(WorldCategory.Non_Industrial)
        
        if self._hydro<5:
            if self._atmosphere<6 or self._atmosphere>8:
                self._category.append(WorldCategory.Poor)

        if self._hydro==12:
            self._category.append(WorldCategory.Water_World)
        
        if len(self._category)==0:
            self._category=[WorldCategory.Common]
    
    @property
    def category(self)->'list[WorldCategory]':
        return self._category

    @property 
    def atmosphere(self):
        return self._atmosphere

    @property
    def temperature(self):
        return self._temperature

    @property
    def biosphere(self):
        return self._biosphere
    
    @property
    def tech_level(self):
        return self._tech_level

    @property
    def tags(self):
        return self._tags

    @property
    def atmosphere_str(self)->str:
        return "The atmophere is " + atmo.access(self._atmosphere)

    @property
    def temperature_str(self)->str:
        return "The planet is " + temp.access(self._temperature)
    
    @property
    def population_str(self)->str:
        return "It has a population of approximately {}".format(self._population)
    
    @property
    def tech_level_str(self)->str:
        return "The planet is {}".format(tl.access(self._tech_level))

    @property
    def biosphere_str(self)->str:
        return "The biosphere is " + bio.access(self._biosphere)

    def description(self)->str:
        """
        Returns a string describing this world! 
        """
        return ", ".join([self.atmosphere_str, self.temperature_str, self.population, self.tech_level_str, self.biosphere_str])

class UnhabWorld(World):
    def __init__(self, name, rng=None) -> None:
        World.__init__(self, name, rng, population=2, tl=2)

        self._pop = 2
        self._tl = 2
        self._tags = []

        size = d100(rng)
        extra = d100(rng)

        if size<61:
            self._bio = 4
            if extra<22:
                self._atmosphere = 4
                self._temperature = 12
                self.title="geomorteus"
            elif extra<40:
                self._atmosphere = 4
                self._temperature = 9
                self.title="geoinactive"
            elif extra<66:
                self._atmosphere = 4
                self._temperature = 10
                self.title = "dwarf"
            elif extra<91:
                self._atmosphere = 2
                self._temperature = 12
                self.title="reducing"
            elif extra<96:
                self._atmosphere = 4
                self._temperature = 12
                self.title = "chthonian"
            else:
                self._atmosphere = 2
                self._temperature = 12
                self.title = "demon"
        elif size<71:
            # temp 4-10, 6-8 temperate
            # atm 5-10 probably
            if extra<21:
                self._temperature = 10
                self._atmosphere = 7
                self.title="desert"
            if extra<41:
                self._temperature=4
                self._atmosphere = 10
                self.title="adaptable"
            elif extra<51:
                self._temp = 7
                self._atmosphere = 9
                self.title="marginal"
            elif extra<59:
                self._temperature=7
                self._atmosphere=7
                self._bio=7
                self.title="terrestrial"
            elif extra<79:
                self._temperature=7
                self._temperature=7
                self.title="pelagic"
            else:
                self._temperature=4
                self._atmosphere = 7
                self.title="glaciated"

        else:
            self._fuel=True
            self._temperature = 3
            if self._pop>5:
                self._pop = 5

            if extra<21:
                self.title="ice giant"
                self._temperature = 2
            elif extra<86:
                self.title="gas giant"
            elif extra<96:
                self.title="super giant"
            elif extra<97:
                self.title="gas ultar giant"
            else:
                self.title="beta Giant"
                self._temperature = 12

        self.update_category()