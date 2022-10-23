"""
Define the World class 
"""
from random import choice
import numpy as np

from .tables import bio, pop, tl, atmo, temp
from MultiHex2.core import Settlement

WORLD_TAGS = ["Abandoned Colony",
    "Alien Ruins",
    "Altered Humanity",
    "Area 51",
    "Badlands World",
    "Bubble Cities",
    "Civil War",
    "Cold War",
    "Colonized Population",
    "Desert World",
    "Eugenic Cult",
    "Exchange Consulate",
    "Feral World",
    "Flying Cities",
    "Forbidden Tech",
    "Freak Geology",
    "Freak Weather",
    "Friendly Foe",
    "Gold Rush",
    "Hatred",
    "Heavy Industry",
    "Heavy Mining",
    "Hostile Biosphere",
    "Hostile Space",
    "Local Specialty",
    "Local Tech",
    "Major Spaceyard",
    "Minimal Contact",
    "Misandry/Misoginy",
    "Oceanic World",
    "Out of Contact",
    "Outpost World",
    "Perimeter Agency",
    "Pilgrimage Site",
    "Police State",
    "Preceptor Archive",
    "Pretech Cultists",
    "Primitive Aliens",
    "Psionics Fear",
    "Psionics Worship",
    "Psionics Academy",
    "Quarantined World",
    "Radioactive World",
    "Regional Hegemon",
    "Restrictive Laws",
    "Rigid Culture",
    "Seagoing Cities",
    "Sealed Menace",
    "Sectarians",
    "Seismic Activity",
    "Secret Masters",
    "Theocracy",
    "Tomb World",
    "Trade Hub",
    "Tyranny",
    "Unbraked AI",
    "Warlords",
    "Xenophiles",
    "Xenophobes",
    "Zombies"]

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

        self._fuel=False
    
        if "seed" in kwargs.keys():
            np.random.seed(kwargs["seed"])

        self._tags = []

        for entry in world_tag:
            if not isinstance(entry, int):
                raise TypeError("Cannot index with type {}, try an {}".format(type(entry, int)))
            self._tags.append(WORLD_TAGS[entry])

        if len(world_tag)==0:
            self._tags=[ choice(WORLD_TAGS) for i in range(2) ]
        
        self._atmosphere = roll(rng) if atmosphere==-1 else atmosphere
        self._temperature = roll(rng) if temperature==-1 else temperature
        self._biosphere = roll(rng) if biosphere==-1 else biosphere
        self._population_raw = roll(rng) if population==-1 else population
        self._tech_level = roll(rng) if tl==-1 else tl

        self._population = pop.access(self._population_raw)*np.random.randint(1,10)

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

        size = d100(rng)
        extra = d100(rng)

        if size<61:
            self._bio = 4
            if extra<22:
                self._atm = 4
                self._tmp = 12
                self._title="geomorteus"
            elif extra<40:
                self._atm = 4
                self._tmp = 9
                self._title="geoinactive"
            elif extra<66:
                self._atm = 4
                self._tmp = 10
                self._title = "dwarf"
            elif extra<91:
                self._atm = 2
                self._tmp = 12
                self._title="reducing"
            elif extra<96:
                self._atm = 4
                self._tmp = 12
                self._title = "chthonian"
            else:
                self._atm = 2
                self._tmp = 12
                self._title = "demon"
        elif size<71:
            # temp 4-10, 6-8 temperate
            # atm 5-10 probably
            if extra<21:
                self._tmp = 10
                self._atm = 7
                self._title="desert"
            if extra<41:
                self._tmp=4
                self._atm = 10
                self._title="adaptable"
            elif extra<51:
                self._temp = 7
                self._atm = 9
                self._title="marginal"
            elif extra<59:
                self._tmp=7
                self._atm=7
                self._bio=7
                self._title="terrestrial"
            elif extra<79:
                self._tmp=7
                self._tmp=7
                self._title="pelagic"
            else:
                self._tmp=4
                self._atm = 7
                self._title="glaciated"

        else:
            self._fuel=True
            self._tmp = 2
            if self._pop>5:
                self._pop = 5

            if extra<21:
                self._title="ice giant"
            elif extra<86:
                self._title="gas giant"
            elif extra<96:
                self._title="super giant"
            elif extra<97:
                self._title="gas ultar giant"
            else:
                self._title="beta Giant"
                self._tmp = 12

                                         