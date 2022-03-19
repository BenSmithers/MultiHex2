# Structure

Plans for how to do the structure?

I want the Map Objects and the PyQt5 objects to be interlinked 

when we use scene.add

Clicking on a map returns the map items (or itemIDs?) under it


The QGraphicsScene stands as the map and clicker interface. It'll have an ActionManager and tools. 
    Tools make actions and send them to the action manager
    The ActionManager makes changes happen on the map 


Ultimately, my plan is to set things up with **modules** loaded in from the main menu. Modules will provide...
 - a set of tools
 - a world generator (config widget, runny thing)
 - a tileset 

These will be centrally located, probably in a folder named `modules`. Not sure *exactly* how I'm going to implement the modules yet, but I'm hoping they can be little folders where we any new code is imported. A module will be selectable from a configuration menu off of the main menu. 

There will be the "core" module for overland maps. I'm thinking there will be a Stars W/O Number module. 

## Tools

Tools make package and return actions 

Tools each have classmethods to return the QPixMap for their icon, an alt-text for when the button is hovered over, and a widget to configure the tool. 
Tools are added at the MainWindow level, there a button is made and configured, and the Scene is told to make the tool. 
The buttons, when clicked, tell the scene to set that as the active tool. 
A widget is made and set underneath the button grid, then configured with the scene. 

## Hexes 
    Hexes are registered with scenes. The scene draws the hex, and records the itemID. 
    
### HexGrid

We'll be using a cubic coordinate system where each Hex has three indicies `i`, `j`, and `k`.  

