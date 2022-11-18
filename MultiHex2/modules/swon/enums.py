
from enum import Enum


def get_entry_by_name(name:str, what:Enum)->Enum:
    for entry in what:
        if entry.name.lower() == name.lower():
            return entry
    raise ValueError("Could not find {} in {}".format(name, what))

class TradeGood(Enum):
    Basic_Electronics = 1
    Basic_Machine_Parts = 2 
    Basic_Manufactured_Goods = 3
    Basic_Raw_Materials = 4
    Basic_Consumables = 5
    Basic_Ore = 6
    Advanced_Electronics = 7
    Advanced_Machine_Parts = 8
    Advanced_Manufactured_Goods = 9
    Advanced_Weapons = 10
    Advanced_Vehicles = 11
    Biochemicals = 12
    Crystals_and_Gems = 13
    Cybernetics = 14
    Live_Animlas = 15
    Luxury_Consumables = 16
    Luxury_Goods = 17
    Medical_Supplies = 18
    Petrochemicals = 19
    Pharmaceuticals = 20
    Polymers = 21
    Precious_Metals = 22
    Radioactives = 23
    Robots = 24
    Spices = 25
    Textiles = 26
    Uncommon_Ore = 27
    Uncommon_Raw_Materials = 28
    Wood = 29
    Vehicles = 30
    Dangerous_Biochemicals = 31
    Dangerous_Cybernetics = 32
    Dangerous_Drugs = 33
    Dangerous_Luxuries = 34
    Very_Dangerous_Weapons = 35

class WorldCategory(Enum):
    Common=0
    Agricultural=1
    Asteroid=2
    Desert=3
    Fluid_Oceans=4
    Garden=5
    High_Pop=6
    High_Tech=7
    Ice_Capped=8
    Industrial=9
    Low_Pop=10
    Low_Tech=11
    Non_Industrial=12
    Water_World=13
    Non_Agricultural=14
    Poor=15
    Rich=16
    Amber_Zone=17
    Red_Zone=18


class WorldTag(Enum):
    Abandoned_Colony=1
    Alien_Ruins=2
    Altered_Humanity=3
    Area_51=4
    Badlands_World=5
    Bubble_Cities=6
    Civil_War=7
    Cold_War=8
    Colonized_Population=9
    Desert_World=10
    Eugenic_Cult=11
    Exchange_Consulate=12
    Feral_World=13
    Flying_Cities=14
    Forbidden_Tech=15
    Freak_Geology=16
    Freak_Weather=17
    Friendly_Foe=18
    Gold_Rush=19
    Hatred=20
    Heavy_Industry=21
    Heavy_Mining=22
    Hostile_Biosphere=23
    Hostile_Space=24
    Local_Specialty=25
    Local_Tech=26
    Major_Spaceyard=27
    Minimal_Contact=28
    Misandry_Misoginy=29
    Oceanic_World=30
    Out_of_Contact=31
    Outpost_World=32
    Perimeter_Agency=33
    Pilgrimage_Site=34
    Police_State=35
    Preceptor_Archive=36
    Pretech_Cultists=37
    Primitive_Aliens=38
    Psionics_Fear=39
    Psionics_Worship=40
    Psionics_Academy=41
    Quarantined_World=42
    Radioactive_World=43
    Regional_Hegemon=44
    Restrictive_Laws=45
    Rigid_Culture=46
    Seagoing_Cities=47
    Sealed_Menace=48
    Sectarians=49
    Seismic_Activity=50
    Secret_Masters=51
    Theocracy=52
    Tomb_World=53
    Trade_Hub=54
    Tyranny=55
    Unbraked_AI=56
    Warlords=57
    Xenophiles=58
    Xenophobes=59
    Zombies=60