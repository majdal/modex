# Nodex Version

This is modex using Flask+NodeJS which replaces the earlier Twisted/Autobahn/WAMP setup.
This works by running two simultaneous servers, Flask and Node. Flask replaces the earlier server.py, and Flask
runs the model simulation. What NodeJS does, is runs the client side model visualizer, and it allows us to abstract
the WebSocket implementation. 

So, NodeJS listens on two ports, 8080 and 9080. Going to localhost:8080/ runs the client side farm simulation. 
When the client adds interventions (currently a Eutopia concept), they are sent over WebSockets to NodeJS, which then
sends them as POST requests to port 5000, which is the Flask server. The Flask server updates the interventions as needed.

When the model is running, data is pushed by being sent as a POST request to localhost:9080//, which then sends them as WebSocket
data to the client's running game.

# Model Explorer

We are an interdisciplinary project of the [Social Innovation Group](http://sig.uwaterloo.ca) at the University of Waterloo. We are building a simulation of the southern Ontario farm system in its social, economic, and ecological aspects, and simultaneously building out tools to explore large-scale semi-chaotic simulations.

<!-- TODO: insert a screencap of the working model here, with place names labelled and graphs plotted -->


We're attacking the problem of simulating [complexity](https://en.wikipedia.org/wiki/Complex_systems) because we are on the cusp of having enough computational power to do it well for the first time in history. We intend to build powerful and intuitive [visualization](FIXME), [interaction](FIXME) and [statistical](FIXME) methods that let a user without too much training engage with multi-valent cross-domain models. That is, we are building a system that has [agents](https://en.wikipedia.org/wiki/Agent-based_model) interacting with both [geography](http://www.esri.com/what-is-gis/) and  [physics](https://en.wikipedia.org/wiki/Differential_equation), with statistically valid insights to what the future holds for humanity. Our watchwords are "ambitious" and "elegant".

See our [blog](http://socialinnovationsimulation.com/), our [people](FIXME), and our [wiki](https://github.com/majdal/modex/blob/master/wiki/Home.md), and our [live demo](FIXME).


## Getting Started ##
1. Clone this repository: `git clone https://github.com/majdal/modex.git`.
2. To install dependencies, see [the developer's guide](src/README.md).
3. To run the application, run `python run.py` in a terminal. A new browser window should open automatically, pointing to `http://127.0.0.1:8080`.
