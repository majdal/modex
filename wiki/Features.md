Features
========

This is our official Model Explorer feature spec. It is expected to evolve with time. 
See [UseCases](UseCases.md) for the motivation behind all of these
(or, if you can't find it there, challenge the feature in a comment here or write up a case study there)


1. Running a single instance of a model and "watching" it (see NetLogo for great examples of this)
interacting with it as it runs
1. Able to host **any** (computational) model in **any** programming language, except that the model might need to be modified to output data in a particular way
1. Running many copies of a model in parallel and saving the results all to a single database
1. Automated statistics generation
1. Handy, composable, data widgets, which update as new data comes:
  * the ability for end-users to compose new visualizations in-browser
  * these widgets need to be pretty
  1. Maps
    * vector data
    * raster data
    * bits on the map should be clickable and sensible related information from the other data streams should pop up
  1. Bar charts
    1. Bar charts with confidence and/or credible intervals
  1. Line graphs
    1. Line graphs with confidence and/or credible intervals
  1. Histograms
  1. Scatterplots
  1. 
1. Data-binds
1. Forking of models
1. A small but effective suite of forkable example models with working visualizations
1. (_World Wide_) Web-based Collaboration

Unknowns:
 how do we support model validation?
