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
# they aren't. that is false. untrue. non.

class DownloadError(Exception): pass

def get(z,x,y):
  "downloads data to z/x/y.json, relative to the current working directory"

  url = template.format(server = random.choice(["a","b","c"]),
                              archive = archive,
                              z = z, x = x, y = y)

  tile = requests.get(url)
  if tile.status_code != 200:
    raise InvalidURL("Couldn't download",z,x,y, tile.status_code)
  if not ('features' in tile.json() and tile.json()['features']):
    #print("\tempty")
    return #OSM generates a geojson file that looks valid but is empty if you ask for an area it doesn't know about; skip saving these
  print(url)  
  os.makedirs(os.path.join(str(z),str(x)), exist_ok=True)
  with open(os.path.join(*[str(e) for e in [z,x,y]])+".json","w") as j:
    j.write(tile.text)

def rip(root, zoom, extent):
  "root is a folder to be created for storage"
  "extent is a list [(x0,y0),(xl,yl)] which gives the rectangle of tiles to download"
  "extent only makes sense with reference to a particular zoom level..."
  if os.path.exists(root):
    raise ValueError("'%s' already exists; delete or move it before trying again" % root)
  os.mkdir(root)
  os.chdir(root)

  for z in [zoom]: #range(depth): 
    print("zoom level", z)
    for x in range(*extent[0]):
      for y in range(*extent[1]):
        try:
          get(z,x,y)
        except InvalidURL: #using exceptions as messaging
          print("OpenStreetMap ran out of tiles at y =", y)
          break
      
      # how do I communicate "there's no more tiles past this extent"?

if __name__ == '__main__':
  #it seems that OSM only has vector tiles for buildings at zoom level 14 and 15
  rip(sys.argv[1], zoom=15, extent=[[4500,6000],[4500,6000]])
