# Core 

This section here contains the main core data types. 

## Coordinates 

Contains HexID stuff and functions for converting between Hex and Screen coordinates. 

## Core (Core - Core)

Has the Hex object, the Region object. Note: the Hex object here has the functions for calculating costs/heuristics used by the pathing algorithm.

Contains catalogs that keep track of IDs and objects. 

## Map Entities

All the entity structure. Has the entity objects themselves (Entity, Settlement, Government) and the associated widgets. 

### Entity Widgets. 

These widgets have two modes. The edit mode and the new entity mode. 

In the new entity mode, it contains and configures a widget once accepted. 

In the other mode it prepares a MetaAction (see the action section) by combining actions that'll apply the relevant parameters from the widget it opens. 