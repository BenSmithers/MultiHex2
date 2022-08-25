# MultiHex

<p align="center">
  <img src="https://github.com/BenSmithers/MultiHex2/blob/main/MultiHex2/assets/multihex_logo.png" alt="MultiHex Logo" width="500" height="500">
</p>

A Hex-Map maker, editor, and interface by Ben Smithers. This is an open-source MultiHex tool for (eventually) all your hex-map needs. It will always be open-source and always be freely available on github. It's under active development and there are no official stable releases at the moment. The `main` branch is kept stable (with a few known bugs).

It's a refactor of my earlier project [MultiHex](https://github.com/BenSmithers/MultiHex).
I'm moving over as much of the code as I can, but lots will still have to be remade. 

# Installation 

You should be able to run this from here by setting the environmental variable
```
export PYTHONPATH=$PYTHONPATH:/path/to/here
```
Or, alternatively, just run
```
python -m pip install . 
```
which should then move install these files somewhere python knows about.

# Prerequesites
Only Python3 is supported. For python module requirements, try running 
```
python -m pip install -r requirements.txt
```
which installs 
- PyQt5 (not 4!)
- NumPy

The world generator for the main module also requires the [plate-tectonics](https://github.com/Mindwerks/plate-tectonics) package. 
Eventually I'll update this to be an optional dependency.

# Plans 

## Variable draw size

Maps should save the draw size and the hex coordinates. We should stop saving the exact screen coordinates. 

## New Module types

To encourage some of these other changes, I should write up another map module type (this'll also help debug what's already written).

Stars w/o Number would be a good jumping off point.

## World Gen 
Upgrade the gui/widgets for world generation. Modules/generators should require a widget that can configure the world generation. 
Might also require a little refactor? 

### Faster! 
The current world gen (for overland at least) is way too slow. It'd be better if it could make bigger, faster, maps. 
Might just end up doing a single all-hex pass with basic perlin noise sampling. 
Idea: same continent sampling simulation (best if we can avoid the smoothing phase) followed up by the noise application for temperature and rainfall. Wind may be sample-able from a basic function added onto some perlin/simplex noise. 
```
  TODO: write function
```

## More Mobile 
### Generation 
Right now these are just lik enetities with nothing else added. Need more options for mobiles.
Maybe set up some presets? 
Like... click on "New Mobile" and it gives you a dialog. This effects its behavior

## AI?
Maybe the mobiles could have some kind of AI too. Every, say, week (or on other triggered events) an AI decides what it'll do. 

## Map Routing 
Variable routing options that are module dependent. 
Should also be able to have mobiles "Teleport" without routing between places. How do we do this? 

## Clock system plans

 - clicking on a day button in the calendar opens a prompt with the time until then and a list of events on that day. It gives an option to skip to that day
 - buttons on calendar will be color-coded 
    + red is today
    + gray is nothing
    + green is a holiday or day of note 
    + yellow is a meaningful event (like a mobile moving)

## Procedural Descriptions

For a given point, MHX should write flavor text. 
These should also be influenced by the procedural weather. 

## Procedural Weather

Clouds should occasionally spawn over water. 
Then, the clouds should follow wind and evolve. 