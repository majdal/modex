# gen.py
# generate random tiles

import os, os.path
#using the pillow fork of PIL http://pillow.readthedocs.org/en/latest/reference/ImageDraw.html
from PIL import Image, ImageDraw

def tile(size, colour):
	"generate a tile; returns a PIL Image object"
	I = Image.new('RGB', size)
	brush = ImageDraw.Draw(I)
	brush.rectangle([(0,0), I.size], fill=colour)
	return I

def generate(root):
	"create a repository of zoom/longitude/latitude (ie z/x/y)
	"file structure commonly used (e.g. by OpenStreetMap)
	"in folder 'root'"
	
	# gotcha: the file structure is not totally standardized: the meaning of tiles is.. unclear; the; Bing uses a different scheme
	# hmmm somehow ol3js knows how to deal with running off the end 
	if os.exists(root):
		raise ValueError("'%s' already exists; delete or move it before trying again")
	os.mkdir(root)
	for z in range(20):
		os.mkdir(str(z))
		for x in range(256):
			for y in range(256):
				T = tile((x,y,z), (256,256)) #256 seems to be the standard size?
				T.save(os.path.join(str(z),str(y),str(x)+".png","PNG")
	

if __name__ == '__main__':
	generate(sys.argv[1])
