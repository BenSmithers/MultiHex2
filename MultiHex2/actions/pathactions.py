from .baseactions import MapAction, MetaAction, NullAction
from MultiHex2.core.core import Path, Road
from MultiHex2.core.coordinates import HexID

from PyQt5.QtWidgets import QGraphicsScene

class Add_Delete_Road(MapAction):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed = ["pid", "road"]
        self.verify(kwargs)

        self.pid = kwargs["pid"]
        self.road = kwargs["road"]

    def __call__(self, map: QGraphicsScene) -> 'MapAction':
        if self.pid in map.roadCatalog:
            print("Making new road")
            old_road = map.roadCatalog[self.pid]
            map.remove_road(self.pid)
        else:
            old_road = None

        if isinstance(self.road, Road):
            map.register_road(self.road)

        return Add_Delete_Road(road=old_road, pid=self.pid)

class Add_To_Road_End(MapAction):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed = ["pid", "hexID"]
        self.pid = kwargs["pid"]
        self.hexID = kwargs["hexID"]

    def __call__(self, map:QGraphicsScene)->MapAction:

        map.roadCatalog.add_to(self.pid, self.hexID, True)
        map.draw_road(self.pid)

        return Pop_From_Road_End(pid=self.pid)

class Add_To_Road_Start(Add_To_Road_End):
    def __call__(self, map: QGraphicsScene) -> MapAction:
        map.roadCatalog.add_to(self.pid, self.hexID, False)
        map.draw_road(self.pid)

        return Pop_From_Road_Start(pid=self.pid)

class Pop_From_Road_End(MapAction):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed = ["pid"]
        self.pid = kwargs["pid"]

    def __call__(self, map: QGraphicsScene) -> 'MapAction':
        # if road is length one, then the opposite of this will be a "new road action"
        this_road =  map.roadCatalog[self.pid]

        if len(this_road)==1:
            # delete road action!
            map.remove_road(self.pid)
            map.draw_road(self.pid)
            return Add_Delete_Road(pid = self.pid, road = this_road)
        else:
            end_hexID = map.roadCatalog.pop_from(self.pid, True)
            map.draw_road(self.pid)
            return Add_To_Road_End(pid=self.pid, hexID=end_hexID)

class Pop_From_Road_Start(Pop_From_Road_End):
    def __call__(self, map: QGraphicsScene) -> 'MapAction':
        this_road =  map.roadCatalog[self.pid]
        if len(this_road)==1:
            # delete road action!
            map.remove_road(self.pid)
            map.draw_road(self.pid)
            return Add_Delete_Road(pid = self.pid, road = this_road)
        else:
            end_hexID = map.roadCatalog.pop_from(self.pid, False)
            map.draw_road(self.pid)
            return Add_To_Road_Start(pid=self.pid, hexID=end_hexID)