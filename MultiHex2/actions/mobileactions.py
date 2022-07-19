from MultiHex2.actions.baseactions import NullAction, MetaAction, MapAction
from MultiHex2.clock import Time, minutes_in_day

from PyQt5.QtWidgets import QGraphicsScene


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
        self.verify()
        self._dest_hid = kwargs["dest_hid"]
        self._mobile_eid = kwargs["mobile_eid"]


    def __call__(self, map: QGraphicsScene) -> 'MapAction':
        current_hid = map.get_eid_loc(self._mobile_eid)

        this_entity = map.accessEid(self._mobile_eid)
        speed = this_entity.speed # hexes/day 

        one_day = minutes_in_day
        tph = int(one_day/speed)

        route = map.get_route_a_star(current_hid, self._dest_hid)

        map.moveEntity(self._mobile_eid, route[1])

        if len(route)==2:
            return NullAction()
        else:
            return MobileMoveAction(recurring=Time(minute=tph), dest_hid=self._dest_hid, mobile_eid=self._mobile_eid)
        

