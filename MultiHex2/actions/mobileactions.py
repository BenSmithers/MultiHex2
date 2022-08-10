from MultiHex2.actions.baseactions import NullAction, MetaAction, MapAction
from MultiHex2.clock import Time, minutes_in_day

from PyQt5.QtWidgets import QGraphicsScene
from MultiHex2.tools.clicker_tool import Clicker


# TODO change the mobile speed for a "time to cross hex"

class MobileMoveAction(MapAction):
    """
    Stores a entity ID for whichever mobile is moving. 
        The recurring TIME argument specifies how often a step is made
        each time this comes up, we recalculate the route, step to the next spot, and add in the next step
    """
    def __init__(self, recurring:Time, **kwargs):
        super().__init__(recurring, **kwargs)

        self._show = True
        self.needed=["dest_hid", "mobile_eid"]
        self.verify(kwargs)
        self._dest_hid = kwargs["dest_hid"]
        self._mobile_eid = kwargs["mobile_eid"]


    def __call__(self, map: Clicker) -> 'MapAction':
        current_hid = map.get_eid_loc(self._mobile_eid)

        this_entity = map.accessEid(self._mobile_eid)
        speed = this_entity.speed # hexes/day 

        one_day = minutes_in_day
        tph = int(one_day/speed)

        route = map.get_route_a_star(current_hid, self._dest_hid, False)


        map.moveEntity(self._mobile_eid, route[1])

        if len(route)==2:
            return NullAction()
        else:
            return MobileMoveAction(recurring=Time(minute=tph), dest_hid=self._dest_hid, mobile_eid=self._mobile_eid)
        

class QueueMove(MapAction):
    """
    enqueue a route. 
    Undo-ing this will remove it 
    """
    def __init__(self, recurring=None, **kwargs):
        super().__init__(recurring, **kwargs)
        self._show = True

        self.needed = ["dest_hid", "mobile_eid"]
        self.verify(kwargs)
        self._dest_hid = kwargs["dest_hid"]
        self._mobile_eid = kwargs["mobile_eid"]

    def __call__(self, map: Clicker) -> 'MapAction':
        if self._dest_hid is None:
            map.remove_route(self._mobile_eid)
            map.draw_route(self._mobile_eid)
            return QueueMove(dest_hid=self._dest_hid, mobile_eid=self._mobile_eid)
        else:
            entity_selected = map.accessEid(self._mobile_eid)
            entity_loc = map.access_entity_hex(self._mobile_eid)

            route = map.get_route_a_star(entity_loc, self._dest_hid, False)
            map.draw_route(self._mobile_eid, route)

            speed = entity_selected.speed # hexes/day 
            one_day = minutes_in_day
            tph = int(one_day/speed)
            step =  Time(minute=tph)
            when = map.clock.time + step
            
            print("Queueing to {}".format(when))
            # we queue an event, we don't do anything now!
            route_id = map.add_event(MobileMoveAction(recurring=step, dest_hid = self._dest_hid, mobile_eid=self._mobile_eid), when)
            map.register_route(entity_selected, route_id)

            return QueueMove(dest_hid=None, mobile_eid=self._mobile_eid)

