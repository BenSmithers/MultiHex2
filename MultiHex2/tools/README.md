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

Tools, in general, should **not** make direct edits to the map. They can access the map, see what's there, but never actually permute anything.
If a tool is to modify the map, it should pack that up in an **Action** and then pass that Action up to the parent... like, 
```
    parent.do_now(my_action)
```
That way it enters the undo/redo deque and can be undone! And... redone! 

## Hex Tools

I think there's only one. It makes hexes 

## Region Tool

It makes regions, adds/removes hexes from regions 

## Entity Tool

This one is a little tricky. 
There's a parent tool to handle the editing/selecting of entities. 
Then there are child ones for placing specific kinds of entities. 
So, each one is capable of editing entities. 

## Map Use Tool

Also... a little... tricky. This right now just shows you the local time on a hex and allows skipping to sunsets/sunrises and next events. Woo.

# Widgets 

Each of the tools has a widget associated with it. 
These widgets are used to configure the behavior of the tools. 