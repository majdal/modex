# vecrip.py
# copy down OSM's vectiles-buildings archive
# depends on python-requests

import os.path
import requests
archive = "vectiles-buildings"
template = "http://{server}.tile.openstreetmap.us/{archive}/{z}/{x}/{y}.json

# OSM's standard is zoom/x/y
#...why are OSM's vector tiles in z/x/y
# and their raster tiles in z/y/x? are they?

def rip(root, depth=20):
  if os.path.exists(root):
    raise ValueError("'%s' already exists; delete or move it before trying again")
  os.mkdir(root)
  os.chdir(root)

  for z in range(depth):
    os.mkdir(str(z))
    os.chdir(str(z))
    print("zoom level", z)
    x = 0
    while True: #we don't know how many tiles exist at each zoom level, so we need to guess and check (ie while + break)
      y = 0
      os.mkdir(str(x))
      os.chdir(str(x))
      while True: #loop over y
        url = template.format(server = random.choice(["a","b","c"]),
                              archive = archive,
                              z = zoom, x = x, y = y)
        tile = requests.get(url)
        if tile.status_code != 200:
          print("OpenStreetMap ran out of tiles at y =", y)
          break
        with open(str(y)+".json","w") as j:
          j.write(tile.text)
        y += 1
      if y == 0:
        print("OpenStreetMap ran out of tiles at (z,x,y) =",(z,x,y))
        break
      x += 1 #hm.. this never knows how to break

if __name__ == '__main__':
  rip(sys.argv[1])
