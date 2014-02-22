# gen.py
# generate random tiles

import sys, os, os.path
#using the pillow fork of PIL http://pillow.readthedocs.org/en/latest/reference/ImageDraw.html
from PIL import Image, ImageDraw, ImageOps, ImageColor

def generate(root, depth=20, size=256):
	"create a repository of zoom/longitude/latitude (ie z/x/y)"
	"file structure commonly used (e.g. by OpenStreetMap)"
	"in folder 'root'"
	"256 seems to be the standard tile size?"
	
	# gotcha: the file structure is not totally standardized: the meaning of tiles is.. unclear; the; Bing uses a different scheme
	# hmmm somehow ol3js knows how to deal with running off the end 
	if os.path.exists(root):
		raise ValueError("'%s' already exists; delete or move it before trying again" % root)
	os.mkdir(root)
	os.chdir(root)

	
	T = Image.new('RGB', (size,size)) 
	brush = ImageDraw.Draw(T)
	


	for z in range(depth):
		os.mkdir(str(z))
		os.chdir(str(z))
		print("zoom level", z)
		# each zoom level has a resolution of 2**z tiles each way
		resolution = 2**z
		for x in range(resolution):
			os.mkdir(str(x))
			os.chdir(str(x))
			for y in range(resolution):
				# there are several options I've come up with for generating colouring patterns
				# 
				HUE = z*360/depth
				HUE += x*60/resolution #slide through a (colour) angle of 60deg (1/6th of the colour wheel, or approx one full human-identifiable hue) as the 'globe' rotates 'east', just to give some tone
				HSV = (HUE, 60, 60)
				## to cause a checkerboard pattern, tiles with different x-y parities are inverted
				if (x % 2 != y % 2):
					HSV = (HSV[0], HSV[1]-10, HSV[2]-10)
				
				RGB = ImageColor.getrgb("hsl(%d, %d%%, %d%%)" % HSV) #note: this can also be done with the built-in "colorsys" module
				
				#RGB = (x,y,z)
				#
				#RGB = (z,x,y)
				## to cause a checkerboard pattern, tiles with different x-y parities are inverted
				#if (x % 2 != y % 2):
				#	RGB = tuple([255-e for e in colour])
				
				brush.rectangle([(0,0), T.size], fill=RGB)
				
				# demarque the borders of the world by putting something on the tiles with 0 as a coordinate
				if x == 0: #vertical
					brush.line([(0,0), (0, T.size[1])], fill="steelblue", width=2)
				if y == 0: #horizontal
					brush.line([(0,0), (T.size[0], 0)], fill="steelblue", width=4) #for some reason the top is harder to distinguish than the side

				T.save(str(y)+".png")
			os.chdir("..") #unixism
		os.chdir("..")

if __name__ == '__main__':
	generate(sys.argv[1], int(sys.argv[2])+1)
