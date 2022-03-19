from distutils.dep_util import newer
from core.map_entities import Government
from .baseactions import MapAction, MetaAction
from MultiHex2.core import Entity

from PyQt5.QtWidgets import QGraphicsScene

class New_Entity_Action(MapAction):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed = ["eid", "entity"]
        assert(isinstance(kwargs["entity"], Entity))

        self.eid = kwargs["eid"]
        self.entity = kwargs["entity"]

    def __call__(self, map: QGraphicsScene):
        
        # do stuff...

        return Delete_Entity_Action(eid=self.eid, entity=self.entity)

class Delete_Entity_Action(MapAction):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.needed =["eid", "entity"]
        self.eid = kwargs["eid"]
        self.entity=kwargs["entity"]

    def __call__(self, map: QGraphicsScene):
        
        
        # do stuff...

        return New_Entity_Action(eid=self.eid, entity=self.entity)



class Edit_Entity_Action(MapAction):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.verify(kwargs)


class Edit_Settlement_Action(MapAction):
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)

        self.verify(kwargs)

class Edit_Government_Action(MapAction):
    def __init__(self, recurring=None, **kwargs):
        """
        Construct with a pointer to the government we're editing 
        """
        super().__init__(recurring, **kwargs)
        self.needed=["gov"]

        self.verify(kwargs)

        assert(isinstance(kwargs["gov"], Government))
        self._gov = kwargs["gov"]
        
        self._optional = ["order", "war","spirit"]
