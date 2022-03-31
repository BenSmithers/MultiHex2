# Clicker Tool

This should really be adapted/renamed. This is the **core** object.
This is the main QGraphicsScene+ActionManager that keeps track of the tools and catalogs.
As such it does all the drawing and keeps track of all the objects. 
It intercepts mouse and keyboard events, passes them to its active tool, and then does the action that is returned. 
See the actions section for more info on that! 

## Drawing
The Clicker tool does the drawing, we need to be careful to layer these things right 

So...
 - Hexes at z-value 0
 - Rivers at z-val 10
 - Entities at z-val 20
 - Regions at z-value 100


# Tools

Each tool has a few entries. It specifies an icon that's used in the button to select it.
It references a Widget that's used to define it (see the next major section).

## Hex Tools

I think there's only one. It makes hexes 

## Region Tool

It makes regions, adds/removes hexes from regions 

## Entity Tool

This one is a little tricky. 
There's a parent tool to handle the editing/selecting of entities. 
Then there are child ones for placing specific kinds of entities. 
So, each one is capable of editing entities. 

# Widgets 

Each of the tools has a widget associated with it. 
These widgets are used to configure the behavior of the tools. 