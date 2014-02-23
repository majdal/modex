# vecrip.py
# copy down OSM's vectiles-buildings archive
# depends on python-requests

import sys
import os
import requests
from requests.exceptions import InvalidURL
import random
archive = "vectiles-buildings"
template = "http://{server}.tile.openstreetmap.us/{archive}/{z}/{x}/{y}.json"

# OSM's standard is zoom/x/y
#...why are OSM's vector tiles in z/x/y
# and their raster tiles in z/y/x? are they?

class DownloadError(Exception): pass

def get(z,x,y):
  "downloads data to z/x/y.json, relative to the current working directory"

  url = template.format(server = random.choice(["a","b","c"]),
                              archive = archive,
                              z = z, x = x, y = y)
  print(url)
  tile = requests.get(url)
  if tile.status_code != 200:
    raise InvalidURL("Couldn't download",z,x,y, tile.status_code)
  print(tile)
  os.makedirs(os.path.join(str(z),str(x)), exist_ok=True)
  with open(os.path.join(*[str(e) for e in [z,x,y]])+".json","w") as j:
    j.write(tile.text)

def rip(root, depth=20):
  "root is a folder to be created for storage"
  #"extent is a list [(x0,y0),(xl,yl)] which gives the rectangle of tiles to download"
  #"extent only makes sense with reference to a particular zoom level..."
  if os.path.exists(root):
    raise ValueError("'%s' already exists; delete or move it before trying again" % root)
  os.mkdir(root)
  os.chdir(root)

  for z in [15]: #range(depth): #it seems that OSM only has vector tiles at zoom level 15
    print("zoom level", z)
    x = 0
    while True: #we don't know how many tiles exist at each zoom level, so we need to guess and check (ie while + break)
      y = 0
      while True: #loop over y
        try:
          get(z,x,y)
        except InvalidURL: #using exceptions as messaging
          print("OpenStreetMap ran out of tiles at y =", y)
          break
        y += 1
      if y == 0: #sketchy, but I don't know how else to define "we ran off the right edge of the map" than "asking for the first of the right edge failed"
        print("OpenStreetMap ran out of tiles at (z,x,y) =",(z,x,y))
        break
      x += 1 #hm.. this never knows how to break

if __name__ == '__main__':
  rip(sys.argv[1])
