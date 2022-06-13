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

# Clock system plans

 - clicking on a day button in the calendar opens a prompt with the time until then and a list of events on that day. It gives an option to skip to that day
 - buttons on calendar will be color-coded 
    + red is today
    + gray is nothing
    + green is a holiday or day of note 
    + yellow is a meaningful event (like a mobile moving)
