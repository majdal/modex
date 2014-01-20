# Model Explorer

We are an interdisciplinary project of the [Social Innovation Group](http://sig.uwaterloo.ca) at the University of Waterloo. We are building a simulation of the southern Ontario farm system in its social, economic, and ecological aspects, and simultaneously building out tools to explore large-scale semi-chaotic simulations.

<!-- TODO: insert a screencap of the working model here, with place names labelled and graphs plotted -->


We're attacking the problem of simulating [complex](https://en.wikipedia.org/wiki/Complex_systems) because we are on the cusp of having enough computational power to do it well for the first time in history. We intend to build powerful and intuitive [visualization](FIXME), [interaction](FIXME) and [statistical](FIXME) methods that let a user without too much training engage with multi-valent cross-domain models. That is, we are building a system that has [agents](https://en.wikipedia.org/wiki/Agent-based_model), interacting with [geography](http://www.esri.com/what-is-gis/)) and  [physics](https://en.wikipedia.org/wiki/Differential_equation) that gives statistically valid guidelines to what the future holds for humanity. Our watchwords are "ambitious" and "elegant".

See our [blog](http://socialinnovationsimulation.com/), <!-- our [people](...), --> and our [wiki](https://github.com/majdal/modex/wiki).


## Getting Started ##
1. Clone this repository: `git clone --recursive https://github.com/majdal/modex.git`. Notice the `--recursive` flag: it is used to clone the repositories under `simpacks`, which makes the lightbulb mode work with garlicsim. 
2. To install dependencies, see [the developer's guide](src/README.md)
3. To run the application, run `python run.py` in a terminal. A new browser window should open automatically, pointing to `http://127.0.0.1:8080`.
