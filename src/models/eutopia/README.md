farm_eutopia
============

Possible worlds farm simulation.

There are two ways to run the model. For a quick test, run
```
$ python eutopia.py
```
It will timestep the model for a bit and then print final economic results.
If you have scipy+matplotlib installed, it will also plot these results.

To build a bigger application, construct a `Eutopia` instance,
give it a place to log, and repeatedly call `next()` on it.
For example:
```{py}
import eutopia
log = []
simulation = eutopia.Eutopia(log)
for timestep in simulation:
    print(log)
```
For Eutopia, each `next()` call is a timestep.

* `simulation.py` is some framework code meant to manage distinct runs of the simulation, e.g. to compare tax scenarios.
* `activity.py` and `eutopia.py` are the simulation proper
* `pygdal.py`   is the beginnings of a library to wrap gdal into a more pythonic form; Eutopia uses it internally.

You should see a symlink (if you're on OS X or Linux; dunno about Windows)
```Elora_esque.shp.zip -> Elora_esque.shp.zip.real``` here.
The ".real" file is copyrighted and you need to obtain it from a team member.
Once you have it, you should be able to just put it in this folder.
See src/README.md for the reasoning behind this design.
