
from MultiHex2.core.coordinates import HexID
from MultiHex2.core.core import Path

class Road(Path):
    def __init__(self, *positions):
        super().__init__(*positions)

        self._quality = 1.0
    
    @property
    def quality(self):
        return self._quality

    @property
    def vertices(self)->'list[HexID]':
        return super().vertices