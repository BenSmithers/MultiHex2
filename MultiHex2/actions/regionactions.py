from MultiHex2.actions.baseactions import MapAction, MetaAction

from PyQt5.QtWidgets import QGraphicsScene

from copy import copy

class MetaRegionUpdate(MapAction):
    """
    Changes information like the name and fill type of a region 
    """
    def __init__(self, recurring=None, **kwargs):
        MapAction.__init__(self, recurring=None, **kwargs)
        self.needed=["name","fill", "rid", "layer"]

        self.verify(kwargs)

        self.new_name = kwargs["name"]
        self.fill = kwargs["fill"]
        self.rID = kwargs["rid"]
        self.layer = kwargs["layer"]

    def __call__(self, map: QGraphicsScene) -> 'MetaRegionUpdate':
        region = map.accessRegion(self.rID, self.layer)
        old_fill = region.fill
        old_name = region.name
        
        region.set_name(self.new_name)
        region.set_fill(self.fill)
        # redraw it! 
        map.drawRegion(self.rID, self.layer)
        return MetaRegionUpdate(name=old_name, fill=old_fill, rid=self.rID, layer=self.layer)



class New_Region_Action(MapAction):
    """
    This action registers a region in the Hexmap
    Requires knowledge of next available rid! 
    """
    def __init__(self, **kwargs):
        MapAction.__init__(self, recurring=None, **kwargs)
        self.needed=["region", "rid", "layer"]
        self.verify(kwargs)
        self.region=kwargs["region"]
        self.rID=kwargs["rid"]
        self.layer=kwargs["layer"]


    def __call__(self, map:QGraphicsScene):
        this_rid = map.addRegion( self.region, self.layer )
        assert(this_rid == self.rID)
        return Delete_Region_Action(rID=self.rID, region=self.region, layer=self.layer)

class Delete_Region_Action(MapAction):
    """
    This action deletes a region from a Hexmap
    """
    def __init__(self, **kwargs):
        MapAction.__init__(self, recurring=None, **kwargs)
        self.needed=["rID", "layer"]
        self.verify(kwargs)
        self.layer=kwargs["layer"]
        self.rID=kwargs["rID"]

    def __call__(self, map:QGraphicsScene):
        old_region = map.accessRegion(self.rID, self.layer)
        map.deleteRegion(self.rID)

        return New_Region_Action(region=old_region, rid=self.rID, layer=self.layer)


class Region_Add_Remove(MapAction):
    """
        This action is to add and remove hexes from regions on the map. 
    """
    def __init__(self, **kwargs):
        MapAction.__init__(self, recurring=None, **kwargs)
        self.needed = ["rID", 'hexID', 'layer']
        self.verify(kwargs)
        self.rID = kwargs["rID"]
        self.hexID = kwargs["hexID"]
        self.layer = kwargs["layer"]
        
        self.old_rid = None


    def __call__(self, map:QGraphicsScene):
        if self.rID is None: # removing this hex from a region

            self.old_rid = map.accessHexRegion(self.hexID, self.layer)
            old_region = copy(map.accessRegion(self.rID, self.layer))

            map.regionRemoveHex( self.hexID, self.layer )

            # this might have deleted the region, check if its still part of the catalog
            if map.accessRegion(self.old_rid, self.layer) is None:
                # if it did, the inverse is to make a new region with the old rid
                return New_Region_Action(rID=self.old_rid, region=old_region, layer=self.layer)
            else:
                # if it didn't delete the region, then we just add the hex back in
                return Region_Add_Remove(rID=self.old_rid, hexID=self.hexID, layer=self.layer)
        else:
            # there's a chance this action is the inverse of one that deleted the region we're adding back to

            if map.accessRegion(self.rID, self.layer) is None:
                raise ValueError("Cannot add to region {}, which doesn't exist".format(self.rID))
            else:
                map.regionAddHex(self.rID , self.hexID , self.layer) 
            
            return Region_Add_Remove(rID=None, hexID=self.hexID, layer=self.layer)

class Merge_Regions_Action(MapAction):
    def __init__(self, **kwargs):
        MapAction.__init__(self, recurring=None, **kwargs)
        self.needed=["rID2","rID2"]
        self.verify(kwargs)
        self.rid1 = kwargs["rID1"]
        self.rid2 = kwargs["rID2"]
        self.layer = kwargs["layer"]

        self._drawtype=True
    
    def __call__(self, map:QGraphicsScene):
        """
        Merging these is easy, the inverse is a little hard. 

        We have to delete the combined region (Region 1), then create the sub-regions (1 and 2)
        We need to also be sure to make the sub-regions in order of increasing region number 
        """
        map.mergeRegions(self.rid1, self.rid2, layer=self.layer)

        region1 = map.accessRegion(self.rid1, layer=self.layer)
        region2 = map.accessRegion(self.rid2, layer=self.layer)

        inverse = MetaAction(Delete_Region_Action(rID=self.rid1, layer=self.layer))
        add1 = New_Region_Action(rID=self.rid1, region=region1, layer=self.layer)
        add2 = New_Region_Action(rID=self.rid2, region=region2, layer=self.layer)
        """
         the order matters! 
         if these are in the wrong order we may go 
                    do      undo         redo
         rid1+rid2 --> rid1 --> rid2+rid1 --> rid2 
        """
        if self.rid1>self.rid2:
            inverse.add_to(add2)
            inverse.add_to(add1)
        else:
            inverse.add_to(add1)
            inverse.add_to(add2)
        return(inverse)


