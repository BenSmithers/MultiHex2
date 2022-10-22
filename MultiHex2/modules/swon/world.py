"""
Define the World class 
"""
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

def roll(mod=0):
    return np.random.randint(1,7)+np.random.randint(1,7)+mod

class World(Settlement):
        
    def __init__(self,name,
                atmosphere=-1, temperature=-1,biosphere=-1,
                population=-1, tl=-1,*world_tag, **kwargs) -> None:
        if not isinstance(world_tag,(list,tuple)):
            raise TypeError("World Tags should be type {}, not {}".format(list, type(world_tag)))
        super().__init__(name, None, True)
    
        if "seed" in kwargs.keys():
            np.random.seed(kwargs["seed"])

        self._tags = []

        for entry in world_tag:
            if not isinstance(entry, int):
                raise TypeError("Cannot index with type {}, try an {}".format(type(entry, int)))
            self._tags.append(WORLD_TAGS[entry])
        
        self._atmosphere = roll() if atmosphere==-1 else atmosphere
        self._temperature = roll() if temperature==-1 else temperature
        self._biosphere = roll() if biosphere==-1 else biosphere
        self._population_raw = roll() if population==-1 else population
        self._tech_level = roll() if tl==-1 else tl

        self._population = pop.access(self._population_raw)*np.random.randint(1,10)

    @property
    def atmosphere(self)->str:
        return "The atmophere is " + atmo.access(self._atmosphere)

    @property
    def temperature(self)->str:
        return "The planet is " + temp.access(self._temperature)
    
    @property
    def population_str(self)->str:
        return "It has a population of approximately {}".format(self._population)
    
    @property
    def tech_level(self)->str:
        return "The planet is {}".format(tl.access(self._tech_level))

    @property
    def biosphere(self)->str:
        return "The biosphere is " + bio.access(self._biosphere)

    def description(self)->str:
        """
        Returns a string describing this world! 
        """
        return ", ".join([self.atmosphere, self.temperature, self.population, self.tech_level, self.biosphere])