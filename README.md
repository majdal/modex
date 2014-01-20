## Requirements ##
* Python 2.x
* Twisted
* GDAL
* An HTML5-supporting browser (so, any recent Firefox, Chrome, Opera, or even IE)
* Datasets (not all are open; for some you need to be part of [OGDE]() to legally obtain them)

## Getting Started ##
1. Clone this repository: `git clone --recursive https://github.com/majdal/modex.git`. Notice the `--recursive` flag: it is used to clone the repositories under `simpacks`, which makes the lightbulb mode work with garlicsim. 
2. To install dependencies, see [the developer's guide](src/README.md)
3. To run the application, run `python run.py` in a terminal. A new browser window should open automatically, pointing to `http://127.0.0.1:8080`.
