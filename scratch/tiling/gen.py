# gen.py
# generate random tiles

import sys, os, os.path
#using the pillow fork of PIL http://pillow.readthedocs.org/en/latest/reference/ImageDraw.html
from PIL import Image, ImageDraw, ImageOps

def generate(root):
	"create a repository of zoom/longitude/latitude (ie z/x/y)"
	"file structure commonly used (e.g. by OpenStreetMap)"
	"in folder 'root'"

	
	# gotcha: the file structure is not totally standardized: the meaning of tiles is.. unclear; the; Bing uses a different scheme
	# hmmm somehow ol3js knows how to deal with running off the end 
	if os.path.exists(root):
		raise ValueError("'%s' already exists; delete or move it before trying again")
	os.mkdir(root)
	os.chdir(root)


	T = Image.new('RGB', (256,256)) #256 seems to be the standard size?
	brush = ImageDraw.Draw(T)

	for z in range(20):
		os.mkdir(str(z))
		os.chdir(str(z))
		print("zoom level", z)
		for x in range(256):
			os.mkdir(str(x))
			os.chdir(str(x))
			for y in range(256):
				colour = (z,x,y)
				
				# to cause a checkerboard pattern, tiles with different x-y parities are inverted
				if (x % 2 != y % 2):
					colour = tuple([255-e for e in colour])
				brush.rectangle([(0,0), T.size], fill=colour)
				
				T.save(str(y)+".png")
			os.chdir("..") #unixism
		os.chdir("..")

if __name__ == '__main__':
	generate(sys.argv[1])
