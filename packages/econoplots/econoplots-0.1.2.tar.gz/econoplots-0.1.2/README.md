# Description
This project helps create Matplotlib plots in the style of *The Economist*. Only some plot styles are supported (line plots are the only style that works right now) and there are some stylistic differences from *The Economist* for the sake of convenience/laziness. 

# Users Guide
- Install fonts (see below) before using any functions.
- The main function you will use is `converter.convert2Econo()`, which takes a Matplotlib `Axes` and returns and `Axes` that is formatted nicely.
    - First generate a Matplotlib `Axes` in any way you like, then pass it into `convert2Econo()`-- then presto you have an Econoplot!

# How to install fonts
- Copy .ttf file here: "~\\.local\share\fonts"
- Delete the matplotlib cache here (it will automatically be recreated): "~\\.cache\matplotlib"
