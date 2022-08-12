from MultiHex2.actions.baseactions import NullAction, MetaAction, MapAction, MapEvent
from MultiHex2.clock import Time, Clock

from PyQt5.QtWidgets import QWidget

from collections import deque
import os
import numpy as np

class ActionManager:
    """
    This keeps track of upcoming events (and actions) and the time.
    It allows you to add new events and 

    This is made before on launch before the map is loaded, so it doesn't do anything until the map is loaded. 
    """
    def __init__(self):
        self._queue = []

        self.database_dir = os.path.join(os.path.dirname(__file__), "..","resources")
        self.database_filename = "example_events.csv"

        self._event_widget = None

        self._unsaved = False

        # we keep a list of Actions' inverses we've done, so we can always go back through
        self.n_history_max = 50 
        self.redo_history = deque()
        self.undo_history = deque()

        self._making_meta = False
        self._meta_inverses = []

        self._meta_event_holder = None

        self._clock = Time()

        self._latitude = 0.0
        self._longitude = 0.0

    def update_times(self):
        self._event_widget.update()

    @property
    def clock(self):
        return self._clock

    def queue(self):
        return self._queue

    def configure_event_widget(self, widg:QWidget):
        self._event_widget = widg

    def configure_with_clock(self, this_clock:Clock):
        """
        Configures this action manager with a clock object, loads in all the events/holidays from a datafile 
        """
        self._clock = this_clock
        time = this_clock.time

        fullpath = os.path.join(self.database_dir, self.database_filename)
        data = np.loadtxt(fullpath, dtype=str, comments="#", delimiter=",")
        for row in data:
            # we do the "-1" on most of these to convert between common terminology and internal clockwork
            # ie, language counts months and days from "1"
            # code counts them from "0"
            if row[-1] == "annual":
                recurring = Time(year=int(row[4]))
                start_time = Time(minute=int(row[0]), hour=int(row[1]), day=int(row[2])-1, month=int(row[3])-1, year=time.year)
                if start_time<time:
                    start_time = start_time + Time(year=1)
            elif row[-1]=="monthly":
                recurring = Time(month=int(row[3]))
                start_time = Time(minute=int(row[0]), hour=int(row[1]), day=int(row[2])-1, month=time.month, year=time.year)
                if start_time< time:
                    start_time = start_time + Time(month=1)
            elif row[-1]=="daily":
                recurring = Time(day=int(row[2]))
                start_time = Time(minute=int(row[0]), hour=int(row[1]), day=time.day, month=time.month, year=time.year)
                if start_time< time:
                    start_time = start_time + Time(day=1)
            elif row[-1]=="hourly":
                recurring = Time(hour=int(row[1]))
                start_time = Time(minute=int(row[0]), hour=time.hour, day=time.day, month=time.month, year=time.year)
                if start_time< time:
                    start_time = start_time + Time(hour=1)
            else:
                # not recurring 
                start_time = Time(minute=int(row[0]), hour=int(row[1]), day=int(row[2]), month=int(row[3]), year=int(row[4]))
                recurring = None
            event = MapEvent(recurring=recurring)
            event.brief_desc=row[5]
            self.add_event(event, time=start_time)

    def config_with(self, latitude:float, longitude:float)->None:
        self._latitude = latitude
        self._longitude = longitude

        self._event_widget.set_lat_lon(self._latitude, self._longitude)

    @property
    def unsaved(self):
        return self._unsaved

    def reset_save(self):
        self._unsaved=False

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

        self._unsaved=True

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
        
        self._unsaved=True

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

    def remove_from_event_queue(self, where:int):
        """
        finds an event stored at id "id", removes it from the queue 
        """

        i = 0
        while self._queue[i][1].id!=where:
            print("{} vs {}".format(id(self._queue[i][1]), where))
            i+=1 
            if i==len(self._queue):
                print("failed to remove from queue")
                return
        
        self._queue.pop(i)


    def add_event(self, event:MapEvent, time:Time):
        """
        This function enqueues an Event at a certain time. We simply scan across until we find the right time to put our event 

        TODO : why aren't we enqueuing tuples 
        """
        if not isinstance(event, MapEvent):
            raise TypeError("Can only register {} type events, not {}".format(MapEvent, type(event)))
        if not isinstance(time, Time):
            raise TypeError("Expected {} for time, not {}.".format(Time, type(time)))

        if len(self.queue)==0:
            self._queue.append( [time, event] )
        else:
            if time > self.queue[-1][0]:
                self._queue.append([time,event])
            else:
                loc = 0
                while time > self._queue[loc][0]:
                    loc +=1 
                    
                self._queue.insert(loc,[time,event] )
        
        self._parent_window.ui.events.update()
        return event.id


    def skip_to_next_event(self):
        if len(self.queue)==0:
            return

        data = self.queue[0]

        # some actions will only be done until some criteria is met. Then it returns a "NullAction" when 
        re_queue = True

        # If this is an action, do it. Otherwise it's an event, nothing is done. 
        if isinstance(data[1], MapAction):
            self._unsaved=True
            new_action = data[1](self)
            if isinstance(new_action, NullAction):
                re_queue = False
            else:
                if new_action.recurring is not None:
                    self.add_event(new_action, data[0]+new_action.recurring)
        else:
            if data[1].recurring is not None:
                if re_queue:
                    self.add_event(data[1], data[0]+data[1].recurring)

        self.clock.skip_to(data[0])
        self._parent_window.ui.clock.set_time(self.clock.time)
        self.queue.pop(0)

    def skip_by_time(self, time):
        self.skip_to_time(self.clock.time + time)

    def skip_to_time(self, time):
        if len(self.queue)!=0:
            while time>self.queue[0][0]:
                # moves time up to the next event, does the action (if there is one), and pops the event from the queue
                self.skip_to_next_event()

                if len(self.queue)==0:
                    break

        self.clock.skip_to(time)
        self._parent_window.ui.clock.set_time(time)

    def skip_to_suntime(self):
        time = self.clock.get_next_suntime(self._latitude, self._longitude)

        self.skip_to_time(time)

    @property
    def queue(self):
        return(self._queue)

