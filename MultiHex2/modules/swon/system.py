from MultiHex2.core import Settlement
from MultiHex2.modules.swon import World


class System(Settlement):
    """
    Systems are collections of worlds 
    """
    def __init__(self, name, *worlds):
        is_ward = False
        super().__init__(name, None, is_ward)

        self._wards = list(worlds)

    def add_ward(self, new_ward:World):
        """
        Adds a world to the system 
        """
        return super().add_ward(new_ward)

