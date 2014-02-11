#!/usr/bin/python2
"""emulate this bash script, in a cross-platform and working-directory-agnostic way:
```bash
 src/backend/server.py &
 firefox http://localhost:8080/
```
"""

# TODO: this script is untested on Windows
# TODO: silence messages from the webrowser (they are very distracting)

import sys
from os.path import dirname, abspath, join as pathjoin

# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Utilities for dealing with processes.
"""

import os

def which(name, flags=os.X_OK):  #this function is from twisted 8.2's twisted.python.procutils, imported so that this script doesn't depend on twisted itself
    """Search PATH for executable files with the given name.
    
    On newer versions of MS-Windows, the PATHEXT environment variable will be
    set to the list of file extensions for files considered executable. This
    will normally include things like ".EXE". This fuction will also find files
    with the given name ending with any of these extensions.

    On MS-Windows the only flag that has any meaning is os.F_OK. Any other
    flags will be ignored.
    
    @type name: C{str}
    @param name: The name for which to search.
    
    @type flags: C{int}
    @param flags: Arguments to L{os.access}.
    
    @rtype: C{list}
    @param: A list of the full paths to files found, in the
    order in which they were found.
    """
    result = []
    exts = filter(None, os.environ.get('PATHEXT', '').split(os.pathsep))
    path = os.environ.get('PATH', None)
    if path is None:
        return []
    for p in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, flags):
            result.append(p)
        for e in exts:
            pext = p + e
            if os.access(pext, flags):
                result.append(pext)
    return result


import threading, webbrowser, time
import subprocess

#'working directory': not the system working directory, but the directory this program is in (so that we can be run from anywhere and$
PROJECT_ROOT = dirname(abspath(__file__)) #run.py should always sit in the project root

def browse():
  time.sleep(2) #give time for the server to spin up
  webbrowser.open('http://127.0.0.1:8080')  #the URL here is hardcoded and needs to match what server.py spins up on

if __name__ == '__main__':
  # attempt, in a reasonably cross-platform way, to find the python2 interpreter
  # this depends on twisted which means this script itself depends on python2, which is sort of irritating
  #PYTHON = which("python2")
  #if not PYTHON:
  #  PYTHON = which("python")
  #PYTHON = PYTHON[0] #just take the first result as the final result, because whatever
  PYTHON = 'python'  #at the moment, 'python2' vs 'python3' seems to be the more cross-compatible method this way
  
  browser = threading.Thread(target=browse) 
  browser.start()  #open a browser to the webapp's page (nonblocking)
                   # this is glitchy: depending on the mixture of close buttons and ctrl-cs sent
  
  # even though the script we're emulating runs the server in the background
  # it is cleaner to run everything else in the background and run the server on the mainthread
  # because call() hooks SIGINT (or your local system's favourite shutdown signal)
  # and politely but firmly kills the server no matter how run.py ends
  subprocess.call([PYTHON, pathjoin(PROJECT_ROOT, "src", "backend", "server.py"), "debug"])
