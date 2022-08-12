from MultiHex2.actions.baseactions import NullAction, MetaAction, MapAction
from MultiHex2.clock import Time, minutes_in_day

from PyQt5.QtWidgets import QGraphicsScene
from MultiHex2.tools.clicker_tool import Clicker

from MultiHex2.core.core import hex_scale

# TODO change the mobile speed for a "time to cross hex"

class MobileMoveAction(MapAction):
    """
    Stores a entity ID for whichever mobile is moving. 
        The recurring TIME argument specifies how often a step is made
        each time this comes up, we recalculate the route, step to the next spot, and add in the next step

    TODO have this action *optionally* support being directly provided with a route! 
        THEN also allow it to be given a follow-up action to make a multi-step route? 
    """
    def __init__(self, recurring:Time, **kwargs):
        super().__init__(recurring, **kwargs)

        self._show = True
        self.needed=["dest_hid", "mobile_eid"]
        self.verify(kwargs)
        self._dest_hid = kwargs["dest_hid"]
        self._mobile_eid = kwargs["mobile_eid"]

    @property
    def id(self):
        return self._mobile_eid

    def __call__(self, map: Clicker) -> 'MapAction':
        current_hid = map.get_eid_loc(self._mobile_eid)

        this_entity = map.accessEid(self._mobile_eid)
        speed = this_entity.speed # hexes/day 

        geo = map.accessHex(current_hid).geography
        if geo in hex_scale:
            scale = hex_scale[geo]
        else:
            scale = 1.0

        one_day = minutes_in_day
        tph = int(scale*one_day/speed)

        route = map.get_route_a_star(current_hid, self._dest_hid, False)
        
        #map.register_route(self._mobile_eid, route)

        map.moveEntity(self._mobile_eid, route[1])
        if len(route)<=2:    
            map.remove_route(self._mobile_eid)        
            return NullAction()
        else:
            map.draw_route(self._mobile_eid, route[1:])
            acty = MobileMoveAction(recurring=Time(minute=tph), dest_hid=self._dest_hid, mobile_eid=self._mobile_eid)
            acty.brief_desc = self.brief_desc
            print("brief desc = {}".format(acty.brief_desc))
            return acty
        

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

    @property
    def id(self):
        return self._mobile_eid

    def __call__(self, map: Clicker) -> 'MapAction':
        if self._dest_hid is None:
            map.remove_route(self._mobile_eid)
            # OH! Accessthe map, scan through until we find the right queued event, get its destination (if any) and return that. 
            # if there is none, then we just return the NullAction (nothing was done)
            return NullAction() # TODO figure out what the heck an inverse to this would be? This cancels a queued move, so we'd need to get the information for where it _was_ going
        else:
            entity_selected = map.accessEid(self._mobile_eid)
            entity_loc = map.access_entity_hex(self._mobile_eid)

            route = map.get_route_a_star(entity_loc, self._dest_hid, False)
            
            geo = map.accessHex(entity_loc).geography
            if geo in hex_scale:
                scale = hex_scale[geo]
            else:
                scale = 1.0

            speed = entity_selected.speed # hexes/day 

            one_day = minutes_in_day
            tph = int(scale*one_day/speed)
            step =  Time(minute=tph)
            when = map.clock.time + step
            
            # we queue an event, we don't do anything now!
            acty = MobileMoveAction(recurring=step, dest_hid = self._dest_hid, mobile_eid=self._mobile_eid)
            acty.brief_desc = self.brief_desc
            route_id = map.add_event(acty, when)
            map.register_route(self._mobile_eid, route_id)
            map.draw_route(self._mobile_eid, route)

            # a thing to move it back!
            acty = QueueMove(dest_hid=None, mobile_eid=self._mobile_eid)
            acty.brief_desc = self.brief_desc
            print("brief desc = {}".format(acty.brief_desc))
            return acty

