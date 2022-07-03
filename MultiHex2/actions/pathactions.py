from .baseactions import MapAction, MetaAction, NullAction
from MultiHex2.core.core import Path, Road
from MultiHex2.core.coordinates import HexID
from MultiHex2.tools.basic_tool import ToolLayer

from PyQt5.QtWidgets import QGraphicsScene



class Add_Delete_Path(MapAction):
    """
        A Generic class for creating and deleting paths 
        Need to specify which layer and return action are used 
    """
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed = ["pid", "road"]
        self.verify(kwargs)

        self._layer = ToolLayer.null
        self._retaction = NullAction

        self.pid = kwargs["pid"]
        self.road = kwargs["road"]

    def __call__(self, map: QGraphicsScene) -> 'MapAction':
        if self._layer == ToolLayer.null or self._retaction==NullAction:
            raise NotImplementedError("Use a derived class with specified layer and return action")

        if self.pid in map.get_path_cat(self._layer):
            old_road = map.get_path_cat(self._layer)[self.pid]
            map.remove_road(self.pid,self._layer)
        else:
            old_road = None

        if self.road is not None:
            map.register_path(self.road,self._layer)

        return self._retaction(road=old_road, pid=self.pid)

class Add_To_Path(MapAction):
    """
    Generic class for adding to the start or the end of a path. 
    """
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed = ["pid", "hexID"]
        self.pid = kwargs["pid"]
        self.hexID = kwargs["hexID"]
        self._layer = ToolLayer.null
        self._retaction = NullAction
        self._end = True

    def __call__(self, map:QGraphicsScene)->MapAction:

        map.get_path_cat(self._layer).add_to(self.pid, self.hexID, self._end)
        map.draw_road(self.pid,self._layer)

        return self._retaction(pid=self.pid)

class Pop_From_Path(MapAction):
    """
    And a generic class for popping entries from the start or end of a path
    """
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed = ["pid"]
        self.pid = kwargs["pid"]
        self._layer = ToolLayer.null
        self._retaction = NullAction
        self._createaction = NullAction
        self._end = True

    def __call__(self, map: QGraphicsScene) -> 'MapAction':
        # if road is length one, then the opposite of this will be a "new road action"
        this_road =  map.get_path_cat(self._layer)[self.pid]

        if len(this_road)==1:
            # delete road action!
            map.remove_road(self.pid,self._layer)
            map.draw_road(self.pid,self._layer)
            return self._createaction(pid = self.pid, road = this_road)
        else:
            end_hexID = map.get_path_cat(self._layer).pop_from(self.pid, self._end)
            map.draw_road(self.pid,self._layer)
            return self._retaction(pid=self.pid, hexID=end_hexID)

"""
Now the various children of the above with the layers and return actions specified 
"""

class Add_Delete_Road(Add_Delete_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)
        self._layer = ToolLayer.civilization
        self._retaction = Add_Delete_Road

class Add_Delete_River(Add_Delete_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)
        self._layer = ToolLayer.terrain
        self._retaction = Add_Delete_River


class Pop_From_Road_End(Pop_From_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self._layer = ToolLayer.civilization
        self._retaction = Add_To_Road_End
        self._createaction = Add_Delete_Road
        self._end = True

class Pop_From_Road_Start(Pop_From_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self._layer = ToolLayer.civilization
        self._retaction = Add_To_Road_Start
        self._createaction = Add_Delete_Road
        self._end = False

class Add_To_Road_End(Add_To_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self._layer = ToolLayer.civilization
        self._retaction = Pop_From_Road_End

class Add_To_Road_Start(Add_To_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)
        self._layer = ToolLayer.civilization
        self._retaction = Pop_From_Road_Start
        self._end = False


class Pop_From_River_End(Pop_From_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self._layer = ToolLayer.terrain
        self._retaction = Add_To_River_End
        self._createaction = Add_Delete_River
        self._end = True

class Pop_From_River_Start(Pop_From_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self._layer = ToolLayer.terrain
        self._retaction = Add_To_River_Start
        self._createaction = Add_Delete_River
        self._end = False

class Add_To_River_End(Add_To_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self._layer = ToolLayer.terrain
        self._retaction = Pop_From_River_End

class Add_To_River_Start(Add_To_Path):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)
        self._layer = ToolLayer.terrain
        self._retaction = Pop_From_River_Start
        self._end = False
