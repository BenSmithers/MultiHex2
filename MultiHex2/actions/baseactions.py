from enum import Enum

from MultiHex2.clock import Time

from PyQt5.QtWidgets import QGraphicsScene

class actionDrawTypes(Enum):
    null = 0
    hex = 1
    region = 2
    entity = 3
    path = 4
    meta = 5


class MapEvent:
    def __init__(self, recurring=None, **kwargs):
        """
        An event used by the Action Manager. 

        recurring - a Time object. Represents how frequently the event happens. 'None' for one-time events. When this kind of event is triggered, a new one is auto-queued 
        kwargs - arguments specific to this kind of event. Varies 
        """

        if recurring is not None:
            if not isinstance(recurring, Time):
                raise TypeError("If recurring, arg must be {}, not {}".format(Time, type(recurring)))
        self.recurring = recurring

        self.brief_desc = "" # will be used on the event list
        self.long_desc = ""

        # whether or not the event should appear in the Event List
        self._show = True

        self._interupt = False

        self.needed = []

        self.verify(kwargs)

    @property
    def id(self):
        """
        Return some identifier we can apply to these events. Optional, really 

        Base is -1 since most IDs in MultiHex start at zero
        """
        return -1
    
    def verify(self,kwargs):
        """
        This function verifies we received all the arguments
        """
        for entry in self.needed:
            if entry not in kwargs:
                raise ValueError("Missing entry {} in kwargs".format(entry))

    @property
    def show(self):
        return(self._show)

    def __call__(self,map:QGraphicsScene):
        raise NotImplementedError("Must override base implementation in {}".format(self.__class__))

class MapAction(MapEvent):
    """
    These are MapEvents that actually effect the map. We call these when they come up. 

    We have a drawtype entry to specify whether or not this Action has an associated redraw command 
    """
    def __init__(self, recurring=None, **kwargs):
        MapEvent.__init__(self,recurring=recurring, **kwargs)

    
    def __call__(self, map:QGraphicsScene)->'MapAction':
        """
        This function is accessed through the `action(map)` syntax

        This then does the action defined by this object, and returns the inverse of the action.
        """
        raise NotImplementedError("Must override base implementation in {}".format(self.__class__))


class NullAction(MapAction):
    """
    An action used to do nothing 
    """
    def __init__(self, **kwargs):
        MapAction.__init__(self, recurring=None, **kwargs)
    def __call__(self, map:QGraphicsScene):
        return NullAction()

class MetaAction(MapAction):
    """
    A combination of actions treated as one. 

    This would be useful when working with large brushes 
    """
    def __init__(self, *args,**kwargs):
        MapAction.__init__(self, **kwargs)
        for arg in args:
            if not isinstance(arg, MapAction):
                raise TypeError("Cannot make MetaAction with object of type {}".format(type(arg)))
        if len(args)==0:
            raise ValueError("Cannot make a meta action of no actions {}".format(len(args)))
        
        self._actions = [arg for arg in args]

    def add_to(self, action:MapAction):
        if action is None:
            return
        
        if not isinstance(action, NullAction):
            if isinstance(action, MetaAction):
                self._actions += action._actions
            else:
                self._actions.append(action)

    @property
    def actions(self):
        return self._actions

    def __call__(self, map:QGraphicsScene):
        """
        The actions are already done, so just make the inverses and return them in inverse-order 
        """
        inverses = [action(map) for action in self.actions][::-1]
        return MetaAction(*inverses)
