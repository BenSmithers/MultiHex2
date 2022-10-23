from MultiHex2.tools.entity_tools import AddSettlement

from .system import System
from .world import World


class AddSystem(AddSettlement):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._creation_type = System
        self.auto_state=1
        self.set_state(1)

        self.highlight_icon="star_red"