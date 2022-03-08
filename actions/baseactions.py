from enum import Enum 
from collections import deque
from multiprocessing.sharedctypes import Value
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

        self.needed = []
        self.verify(kwargs)
    
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

class MapAction(MapEvent):
    """
    These are MapEvents that actually effect the map. We call these when they come up. 

    We have a drawtype entry to specify whether or not this Action has an associated redraw command 
    """
    def __init__(self, recurring=None, **kwargs):
        MapEvent.__init__(self,recurring=None, **kwargs)

    
    def __call__(self, map:QGraphicsScene):
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

class ActionManager:
    """
    This keeps track of upcoming events (and actions) and the time.
    It allows you to add new events and 

    This is made before on launch before the map is loaded, so it doesn't do anything until the map is loaded. 
    """
    def __init__(self):
        self._queue = []

        #self.database_dir = get_base_dir()
        self.database_filename = "event_database.csv"

        # we keep a list of Actions' inverses we've done, so we can always go back through
        self.n_history_max = 50 
        self.redo_history = deque()
        self.undo_history = deque()

        self._making_meta = False
        self._meta_inverses = []

        self._meta_event_holder = None

    def add_to_meta(self, action:MapAction):
        """
        For these special meta actions, we do the things as they are sent. Once we do something non-meta related (or call the finish meta function), 
        we bundle these up in a single MetaAction that can be reversed as one. 

        This is important for doing sweeping brush strokes! 
        """
        self._making_meta = True
        if not isinstance(action, NullAction):
            inverse = action(self)
            self._meta_inverses.append(inverse)


    def finish_meta(self):
        """
        Use the inverses we've collected to make a new MetaEvent, then manually pop that on our undo queue

        return the draw thingy from the meta action 
        """
        if len(self._meta_inverses)==0:
            return
        this_meta = MetaAction(*self._meta_inverses[::-1])
            
        self.undo_history.appendleft(this_meta)
        while len(self.undo_history)>self.n_history_max:
            self.undo_history.pop()

            if len(self.redo_history)!=0:
                self.redo_history=deque()

        self._meta_inverses=[]
        self._making_meta = False

    def do_now(self, event: MapAction, ignore_history = False):
        """
        Tells the action manager to do an action
            - ignore history, bypass the undo/redo functionality. Useful with MetaActions. We can do those actions as we build up the MetaAction
                    then pass the MetaAction through here again and use it with the undo/redo
            - action skip, adds this to the undo/redo queues without actually doing anything. Used with the above! 
        """
        if isinstance(event, NullAction):
            return

        if self._making_meta:
            self.finish_meta()


        inverse = event(self)
        if not ignore_history:
            self.undo_history.appendleft(inverse)
            while len(self.undo_history)>self.n_history_max:
                self.undo_history.pop()
            
            if len(self.redo_history)!=0:
                self.redo_history = deque()

        return inverse
    
    def _generic_do(self, list1, list2):
        """
        This handles the undo and redo functions

        When you do something in a deque, you call the 0th entry, invert the action, and append it at the start of other deque.
        This is done to give undo/redo functionality.
        """

        if len(list1)==0:
            return []
        
        #does the action, stores inverse 
        inverse = list1[0](self)
        
        """ might re-add this. 
        # check if we'll need to redraw anything 
        draw = None
        if list1[0].drawtype:
            draw = [list1[0].draw(),]
        if isinstance(list1[0], MetaAction):

            draw = [entry.draw() for entry in filter(lambda ex:ex.drawtype, list1[0].actions)]
        """

        list2.appendleft(inverse)
        while len(list2)>self.n_history_max:
            list2.pop()
        
        list1.popleft()


    def undo(self):
        if self._making_meta:
            self.finish_meta()
        
        return self._generic_do(self.undo_history, self.redo_history)
    def redo(self):
        return self._generic_do(self.redo_history, self.undo_history)



    def add_event(self, event, time):
        if not isinstance(event, MapEvent):
            raise TypeError("Can only register {} type events, not {}".format(MapEvent, type(event)))
        if not isinstance(time, Time):
            raise TypeError("Expected {} for time, not {}.".format(Time, type(time)))

        if len(self.queue)==0:
            self._queue.append( [time, event] )
        else:
            if time<self.queue[0][0]:
                self._queue.insert(0, [time,event])
            elif time > self.queue[-1][0]:
                self._queue.append([time,event])

            else:
                loc = 0
                while time > self.queue[loc][0]:
                    loc+=1

                self._queue.insert(loc, [time,event])

    def skip_to_next_event(self):
        if len(self.queue)==0:
            return

        data = self.queue[0]

        # If this is an action, do it. Otherwise it's an event, nothing is done. 
        if isinstance(data[1], MapAction):
            data[1].do()
            if data[1].recurring is not None:
                self.add_event(data[1], data[0]+data[1].recurring)

        self.clock.skip_to(data[0])
        self.queue.pop(0)

    def skip_by_time(self, time):
        self.skip_to_time(self.clock.time + time)

    def skip_to_time(self, time):
        if len(self.queue)!=0:
            while time<self.queue[0][0]:
                # moves time up to the next event, does the action (if there is one), and pops the event from the queue
                self.skip_to_next_event()

                if len(self.queue)==0:
                    break

        self.clock.skip_to(time)


    @property
    def queue(self):
        return(self._queue)

