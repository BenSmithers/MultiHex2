# Action Basics

Actions are rather simple things (in theory)! 
You construct them with a series of keyword arguments. 
When an action is called (done by an ActionManager), it changes something on the map. 
Then, it builds an inverse action that undoes whatever it just changed and returns it. 

These actions should be pretty high-level. You generally won't do anything but trade an old for a new, or make calls to the map itself 

# Action Manager

This code manages all the actions. It keeps a queue for events/actions that will happen at some given time.
It also maintains undo/redo queues for immediate actions.
When you tell the action manager to do something, it calls it, then puts the inverse of that action on the undo queue. 
If the user calls Ctrl+Z, it takes the first entry off the undo queue, calls it, and puts the inverse of _that_ onto the top of the redo queue. 
The redo queue, and Ctrl+R (should this be Y?), works similarly. 

# Action Types

## Hex Actions 

Draw Hex, inverse is remove hex 

Tweak hex, self-inverse 

## Region Actions

MetaRegionUpdate - changes some of the properties of a region like its name and fill color

New Region Action - makes a new region, inverse of delete

Delte Region Action - self-explanatory 

Region_Add_Remove - adds/removes hexes from a region on the map 

MergeRegionAction - merges two regions on the map. Inverse is the creation of the two regions that made this one 


## Entity Actions

New, Delete, edit