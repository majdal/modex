# Model Explorer Developer's Guide

## Layout

Each folder should have a README that describes its content in more detail, but as an overview:

* ```assets/``` -- static content, like data
  * ```assets/libs/``` -- external javascript libraries
  * ```assets/images```-- sprites, textures, icons, etc
* ```src/frontend```   -- internal html, javascript, and css 
* ```src/backend```    -- model explorer and the twisted server that feeds it to the frontend
* ```src/models```     -- (_tentative_) different model instances to be hosted by the model explorer
* ```src/scripts```    -- batch scripts, like geoprocessing hacks, one-off webcrawlers, and database cleaners

## Dependencies

We depend on several libraries, tools, and sources. The frontend libraries are all in javascript and are either referenced by hyperlink or included under ```assets/```, but the backend libraries require some work on your end. To get this project running, you need to install these dependencies:

* [Python 2.x](FIXME)
* [Twisted](FIXME)
* [GDAL](FIXME)
* An HTML5-supporting browser (so, any recent Firefox, Chrome, Opera, or even IE)
* [GIS Datasets](../assets/maps/README.md) (not all are open; for some you need to be part of [OGDE](www.lio.mnr.gov.on.ca/) to legally obtain them).

* A spreadsheet. Excel, [LibreOffice Calc](http://www.libreoffice.org/download). You need to be able to work with and debug tabular data. You should be able to do reliable preprocessing of it (sums, averages, subsets) and plotting. (if you are comfortable doing this in matlab, R, or scipy, then by all means stick with what you know).
* A GIS. You can get [ArcGIS](http://esri.com) [from the school](https://uwaterloo.ca/information-systems-technology/services/software-students/microsoft-office-students) at a discount, or you can install [QGIS](http://qgis.org/) which is frankly perhaps better

1. Prepare your system
  - If you're on Ubuntu, use install the following packages `sudo apt-get install build-essential python-dev`
    - if you're on another Linux, you're on your own, but feel free to pressure us to support you: it makes the code better
  - If you're on OSX, see [here](https://github.com/majdal/modex/wiki/Step-by-step-installation-instructions-for-Mac-users)
  - If you're on Windows, see [here]https://github.com/majdal/modex/wiki/Step-by-step-installation-instructions-for-Windows-users)
2. Optionally, set up a [virtualenv](http://www.virtualenv.org/) (this is not quite so optional on Windows and OS X)
2. Install the package dependencies: `pip install -r requirements.txt`
  - if you read requirements.txt you might find that you already have several dependencies installed or that you can install them from your package manager.

## Hacking

To get started, open a command prompt and run 'run.py' (which is living a directory up from here, in the project root):
```
[user@laptop modex]$ ./run.py
2014-01-19 22:57:35-0500 [-] Log opened.
2014-01-19 22:57:35-0500 [-] Starting server in /home/kousu/School/WICI/sig/repos/modex
2014-01-19 22:57:35-0500 [-] putting /home/kousu/School/WICI/sig/repos/modex/src/frontend at root
2014-01-19 22:57:35-0500 [-] putting /home/kousu/School/WICI/sig/repos/modex/assets at assets
2014-01-19 22:57:35-0500 [-] Site starting on 8080
2014-01-19 22:57:35-0500 [-] Starting factory <twisted.web.server.Site instance at 0x14cf680>
2014-01-19 22:57:35-0500 [-] Now open http://127.0.0.1:8080 in your browser
```

which should open a browser window pointed at the twisted web application server we're using.
Because of the complicated web-based nature of this project you must always be running the server
while developing, and you need to have a network connection available for at least for the basemaps, and perhaps other sources.

Next, depending on your interest, see [frontend](frontend) or [backend](backend).
Some changes, namely API changes, which are going to be especially common in the early stage,
require working on both sides simultaneously. To do that work, keep both subfolders open and liberally restart the server: press Ctrl-C, wait for it to terminate, and then rerun 'run.py'.

### Gotchas

You can use qgis to fiddle with geodata: subset it, reorder it, remove or add columns, do precomputation, convert formats...
but it's tricky. Some gotchas with qgis:
* SQL joins are hidden under 'properties' of a layer
* to edit a layer it MUST be in ESRI Shapefile format and you need to find the "Toggle Editing" button (which shows up in the rightclick menu on the layer, once its in that format)
