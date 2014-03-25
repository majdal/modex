# Model Explorer Developer's Guide

Welcome to Modex! Please excuse the construction dust.

If your copy of modex isn't working, make sure your [dependencies](#dependencies) are up to date. 

## Team Guidelines


### Git and Branching

We are using [git](http://www.git-scm.com/book) for version control, under a modified [_gitflow_](http://nvie.com/posts/a-successful-git-branching-model/) pattern.

The biggest modifcation is that we're using git centrally because it's simpler for git newbies--which is most of us--to work with. Thus, the canonical copy of the codebase--which everyone on the team has push access to--is "https://github.com/majdal/modex/". Follow [github's instruction's](FIXME) on setting up your machine to be able to talk to your github account via `ssh` and then, to get a fresh copy of the code, do 
```
git clone git@github.com:majdal/modex
```
or your git client's equivalent. This will connect to github and pull the `master` branch down, and additionally record that you are connecting over ssh--which is what will allow you to push back up. Talk to [@majdal](https://github.com/majdal) at this point to be granted push access. You will be able to test this by
```
echo "Hello, GitHub!" > hello.txt
git add hello.txt
git commit
git push
```
and then looking at [the front page](https://github.com/majdal/modex/) to see if your commit took.

The main thing to know about _gitflow_ is that **every commit to `master` is considered a release**. Our mainline, bleeding-edge, daily code happens in the `develop` branch. Once your account can push and pull (and you've `git rm`'d that testing file, switch to `develop`:
```
git branch develop
git branch --set-upstream-to=origin/develop develop
git checkout develop
```

You can double check what is going on with
```
git branch -a #see active local AND remote branches
```
and by looking in the hidden `.git/config` file.


With every change you make, it's a good idea to test before writing your commit message, and as a rule you **must** test before pushing (but if you do break the build by accident we won't bite your head off: that's what doing our work on `develop` instead of `master` is for). The goal of this design is so that a newbie or interested, remote, researcher can `git clone` and end up with something useful.

![Gitflow](http://nvie.com/img/2009/12/Screen-shot-2009-12-24-at-11.32.03.png )

_Gitflow_ is made a magnitude smooher by installing the gitflow plugin from [here](https://github.com/nvie/gitflow) (Linux/OS X/other), or using [SourceTree](http://www.sourcetreeapp.com/) (Windows/OS X) which has gitflow beautifully integrated. 

As usual with version control systems, large and/or notable changes are built in on-the-side "feature" branches. To make a new branch that won't hurt anything else by accident, do
```
git checkout -b feature1
```
where "feature1" is the name for branch: something short and descriptive of what you're doing in it. Branches show up on the [branches tab](https://github.com/majdal/modex/branches)

The other modification we have to `gitflow` is that, because the public face of our codebase right now is https://github.com/majdal/modex/tree/**master**/wiki, edits to files in `wiki/` happen on `master` unless there's a good reason for them to be done in a branch first. _This is kludgy and subject to change as we get more experience_.


### Documentation

Our heterogeneity makes coordination difficult. This makes it extra important to document where we're at.
Whenever you discover a tricks, gotcha, or reference, record it and make it available to the team.
Putting discoveries into this `wiki/` (which is really just a series of .md files in the source repo) makes them easily linkable, fixable, and public to the world.

Again, for this one case, make sure to make these changes _on `master`_, not `develop`. They are still linkable if you commit on the wrong branch, but they are not findable by the average passer-by. The easiest way at this point to ensure documentation is public is to make your doc edits with GitHub's web-based Edit button. If you have a large amount of changes to make, just like working out of the cloud, (or are reorganizing things/adding pictures/generally doing someting complicated), just be mindful of what branch you're on when you run `git commit`.


### Issue Tracker

We currently are coordinating through an [Asana](http://asana.com) group. Our issue tracker is over there, not here.

### Keeping Copyrighted Data Out

While it is joyous that the Open Data movement is getting underway, not everything is freely available yet.
Several of our datasets are not. It would be disastrous (not the end of the world, but pretty close) if we
accidentally uploaded a copyrighted dataset to github--forcing us to [delete the repositories to wipe any
trace of the bad commit](https://help.github.com/articles/remove-sensitive-data) and recreate them from an older check in.

The convention for dealing with this problem in this project **is as follows**

1. Given a dataset `x.ext` that you want to use
2. Rename it: `mv x.ext x.ext.real`
3. Create a symlink in its place: `ln -s x.ext.real x.ext`
4. Hide `x.ext.real` from git, so it doesn't accidentally get committed: `echo x.ext.real >> .gitignore`
   * **if x.ext.real gets expanded to any child files, add those to .gitignore as well**
5. Distribute `x.ext.real` in some private way to those authorized (thumbdrive, Google Drive, carrier pigeon...)
This way, it should be very difficult to accidentally upload copyrighted data.



## Folder Layout

Each folder should have a README that describes its content in more detail, but as an overview:

* ```assets/``` -- static content, like data
  * ```assets/libs/``` -- external javascript libraries
  * ```assets/images```-- sprites, textures, icons, etc
* ```src/frontend```   -- internal html, javascript, and css 
* ```src/backend```    -- model explorer and the twisted server that feeds it to the frontend
* ```src/models```     -- (_tentative_) different model instances to be hosted by the model explorer
* ```src/scripts```    -- batch scripts, like geoprocessing hacks, one-off webcrawlers, and database cleaners
* ```tests/```         -- unit, integration, acceptance, etc tests
* ```scratch/```       -- demo, testing, and API-learning code goes here. If a demo is at all complicated it should get its own subfolder and include all js libraries it needs locally. Once it cycles through a few iterations its lessons should be merged in ```src/```, but the demo should (within reason) stay put for future reference. 
* ```mockups/```       -- drawings and vision documents

## Dependencies

We depend on several libraries, tools, and sources. The frontend libraries are all in javascript and are either referenced by hyperlink or included under ```assets/```, while the backend libraries require some work on your end. To get hacking on this project, you need to install these dependencies:

* An HTML5-supporting browser (so, any recent Firefox, Chrome, Opera, or even IE)
* [Python 2.x](FIXME)
  * on Linux or OS X you almost certainly already have this; if not, Google how to install it
  * on Windows, go to [download it](http://python.org/download)
* [GDAL](FIXME)
* [GIS Datasets](../assets/maps/README.md) (not all are open; for some you need to be part of [OGDE](www.lio.mnr.gov.on.ca/) to legally obtain them).



You also need several python-specific requirements. They are listed in ```requirements.txt```. **You must put some effort in to decide how you want to install these**. You can either _**install into your system python**_ directory or setup a **_```virtualenv```_** to isolate the packages.

If you want to use ```virtualenv``` first make sure it is installed properly (something like this -- sorry, very much linux specific at the moment; should work on Mac too, but leave a comment if it doesn't)
```
$ sudo pip2 install virtualenv  #make sure virtualenv is install if it isn't already
$ sudo pip2 install virtualenvwrapper #get the scripts that should have come with virtualenv
$ # setup 'workon' to make virtualenvs less tedious
$ cat >> ~/.bashrc <<EOF
export WORKON_HOME=~/.virtualenvs
source /usr/bin/virtualenvwrapper.sh
EOF
$ source ~/.bashrc              #temporarily pull in that change; it will become permanent next login
$ mkdir $WORKON_HOME            #setup a place to put virtualenvs
```

And then construct the environment:
```
$ cd ~/modex           #go to wherever you checked out the repository; it's it's not ~/modex, substitute the correct path
$ mkvirtualenv -p `which python2` modex  #construct the environment; note that we specify python2 here because modex is python2-specific 
$ workon modexenv      #get the missing script that virtualenv should come with
(modexenv)$ which python #you should see the name of the env to the left now, indicating that paths are jailed
/home/yourusername/.virtualenvs/modexenv/bin/python
(modexenv)$ pip install -r requirements.txt
```

Now whenever you want to start working on the project, you must remember the invocation
```
$ cd ~/modex
$ workon modexenv
(modexenv) $
```

**_Virtualenvs_** are an elegant solution to dependency hell, and they allow us to specify with ```requirements.txt``` exactly what code we're desinging against, but they are tedious and take up extra space. Many of the dependencies **_can be isntalled directly into your system_** python ```site-packages/``` folder. Twisted is a great candidate for this: it's extremely stable so there is no need to isolate its version from the mainstream version, and it's large: about 50MB. If you wish to follow this path, then first try installing things with your package manager, and only after you have exhausted that try ```pip```. 

 You can install these dependencies using ```pip``` (which, depending on your system, you might need to run as ```pip2``` since we're developing against Python 2 or):
`pip install -r requirements.txt`

If you don't know if you have a package manager, if you're on linux check if you have ```apt-get``` (aka synaptic), ```pacman```, ```yum```, ```emerge``` or search your distribution's documentation; if you're on OS X see if you have installed [fink](http://fink.thetis.ig42.org/), [port](https://www.macports.org/), or [brew](http://brew.sh/). Then _tediously go through ```requirements.txt``` line by line_ and search in your package manager (and you might need to Google to find the correct package names for your system),

Finally, once that is done, run
```
$ cd ~/modex
$ sudo pip2 install -r requirements.txt
```
to get any leftovers. **You also need to run this when requirements.txt changes**.

Arranging your install this way is more immediately tedious, but it saves you from having to ```workon modexenv``` every day, and saves space on your disk. Do be aware that when you do system updates the updates have a small chance of conflicting with the pip-installed packages, and that if that happens remember you did it yourself.

The choice of which method: virtual or system, is up to you. You will probably have an easier time going with virtualenvs on Windows on OS X, and an easier time with your system package manager on Linux/BSD.


You will probably also want **_these tools_** to make dealing with code easier:

* Some web developer tools (see [frontend/README.md](frontend/) for suggestions)
* [IPython](http://ipython.org), which gives a python command shell _with tab-completion_, and Mathematica-style [notebooks](http://nbviewer.ipython.org).
* [nodejs](http://nodejs.org) - several of our deps have their unit tests written against Node, because it's easier than trying to script a browser. -_tab completion for javascript_
* [topojson](https://github.com/mbostock/topojson/wiki/Installation) comes in handy (make sure to remember `-g` when installing!)


* A spreadsheet. Excel, [LibreOffice Calc](http://www.libreoffice.org/download). You need to be able to work with and debug tabular data. You should be able to do reliable preprocessing of it (sums, averages, subsets) and plotting. (if you are comfortable doing this in matlab, R, or scipy, then by all means stick with what you know).
* A GIS. You can get [ArcGIS](http://esri.com) [from the school](https://uwaterloo.ca/information-systems-technology/services/software-students/microsoft-office-students) at a discount, or you can install [QGIS](http://qgis.org/) which is frankly perhaps better


For a brain dump of everything you might need to know about getting set up on OS X, see [here](../wiki/TechGuides/Step-by-step-installation-instructions-for-Mac-users.md). Similarly, see [here](../wiki/TechGuides/Step-by-step-installation-instructions-for-Windows-users.md) for Windows.


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
