# MultiHex

<p align="center">
  <img src="https://github.com/BenSmithers/MultiHex2/blob/main/assets/multihex_logo.png" alt="MultiHex Logo" width="500" height="500">
</p>

A Hex-Map maker, editor, and interface by Ben Smithers. This is an open-source MultiHex tool for (eventually) all your hex-map needs. It will always be open-source and always be freely available on github. It's under active development and there are no official stable releases at the moment. The `main` branch is kept stable (with a few known bugs).

It's a refactor of my earlier project [MultiHex](https://github.com/BenSmithers/MultiHex).
I'm moving over as much of the code as I can, but lots will still have to be remade. 

# Prerequesites

- PyQt5 (not 4!)
- NumPy
- Python 3 (2 isn't and never will be supported)

# Clock system plans

 - clicking on a day button in the calendar opens a prompt with the time until then and a list of events on that day. It gives an option to skip to that day
 - buttons on calendar will be color-coded 
    + red is today
    + gray is nothing
    + green is a holiday or day of note 
    + yellow is a meaningful event (like a mobile moving)