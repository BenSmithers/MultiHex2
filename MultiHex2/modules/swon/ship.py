from MultiHex2.core.map_entities import Mobile

class Ship(Mobile):
    def __init__(self, name: str):
        super().__init__(name)

        self._speed = 1./6 # 1 hex every 6 days :()
        self._flies = True

        