# About #
This is a framework to modify things! 

-----

# Requirements #
* Python 2.x

# Installation #
1. Clone this repository: `git clone --recursive https://github.com/majdal/modex.git`. Notice the `--recursive` flag: it is used to clone the repositories under `simpacks`, which makes the lightbulb mode work with garlicsim. 

> If you're on Ubuntu, use install the following packages `sudo apt-get install build-essential python-dev`
> If you're on OSX, make sure that you have Xcode installed, and up to date, including commandline tools
> If you're on Windows, `pip` sometimes doesn't install Twisted correctly. Installing it separately might solve the problem. 

2. Install dependencies: `pip install -r requirements.txt`

> We installed Twisted seperately, but you might not have to!


# Running #
To run the server, run `python run.py` in the terminal. A new browser window should open automatically, pointing to `http://127.0.0.1:8080`. 
