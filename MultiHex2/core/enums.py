"""
Define MultiHex enums
"""


from enum import Enum

class ToolLayer(Enum):
    null = 0
    terrain = 1
    civilization = 2
    mapuse = 4


class OverlandRouteType(Enum):
    """
        settings for the routing. Will default to land type. 
        These can be combined bit-wise... just in case?  
    """
    land = 1        # 100
    boat = 2        # 010 
    amphibian = 3   # 110
    aerial = 4      # 001