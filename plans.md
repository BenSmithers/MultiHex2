# Structure

Plans for how to do the structure?

I want the Map Objects and the PyQt5 objects to be interlinked 

when we use scene.add

Clicking on a map returns the map items (or itemIDs?) under it


The QGraphicsScene stands as the map and clicker interface. It'll have an ActionManager and tools. 
    Tools make actions and send them to the action manager
    The ActionManager makes changes happen on the map 

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

