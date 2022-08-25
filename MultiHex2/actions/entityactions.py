from .baseactions import MapAction, MetaAction
from MultiHex2.core import Entity

from PyQt5.QtWidgets import QGraphicsScene

class New_Entity_Action(MapAction):
    """
    Creates and entity, opposite deletes an entity
    """
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed = ["eid", "entity", "coords"]
        self.verify(kwargs)
        assert(isinstance(kwargs["entity"], Entity))

        self.eid = kwargs["eid"]
        self.entity = kwargs["entity"]
        self.coords = kwargs["coords"]

    def __call__(self, map: QGraphicsScene):
        
        # do stuff...        
        map.registerEntity(self.entity, self.coords)

        return Delete_Entity_Action(eid=self.eid, entity=self.entity, coords=self.coords)

class Delete_Entity_Action(MapAction):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)
        self.needed =["eid", "entity", "coords"]
        self.verify(kwargs)
        self.eid = kwargs["eid"]
        self.entity=kwargs["entity"]
        self.coords = kwargs["coords"]
    def __call__(self, map: QGraphicsScene):
        
        map.removeEntity(self.eid)

        return New_Entity_Action(eid=self.eid, entity=self.entity, coords=self.coords)



class Edit_Entity_Action(MapAction):
    """
        Swaps an entity on the map with other one
        Used for editing 
    """
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed = ["eID", "old", "new"]
        self.verify(kwargs)
        self.eid = kwargs["eID"]
        self.old = kwargs["old"]
        self.new = kwargs["new"]


    def __call__(self, map:QGraphicsScene):
        map.updateEntity(self.eid, self.new)

        return Edit_Entity_Action(eID=self.eid, old=self.new, new=self.old)
