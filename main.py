import pygame
from pygame.locals import *

import subprocess

#First of all, let's ask what image we shall use
print "What image do you want to use?"
filename = raw_input()
img = pygame.image.load(filename)

#Then, get the size:
print "What should be the width of the window? Minimum value is 20px"
small_width = max(20, int(raw_input()))
large_width = int(2.75*small_width)
print "What should be the height of the window? Minimum value is 20px"
small_height = max(20, int(raw_input()))
large_height = int(2.75*small_height)

#Scale image to small size, save it
small_img = pygame.transform.scale(img, (small_width, small_height))
small_img_filename = "small_{}".format(filename)
pygame.image.save(small_img, small_img_filename)


#Scale image to large size, save it
large_img = pygame.transform.scale(img, (large_width, large_height))
large_img_filename = "large_{}".format(filename)
pygame.image.save(large_img, large_img_filename)


#This opens a new process as if it was issuing the command in the terminal.
#You can use as many arguments as you need, and you will have a reference to the new process.
#Documentation for subprocess: http://docs.python.org/2/library/subprocess.html

#Initialize the first window, passing image and size
small_window = subprocess.Popen(
	[
		"python", "imgWindow.py",
		small_img_filename,
		"Small Image",
		str(small_width),
		str(small_height),
		str(0)
	]
)

#Initialize the second window, passing image and large size
large_window = subprocess.Popen(
	[
		"python", "imgWindow.py",
		large_img_filename,
		"Large Image",
		str(large_width),
		str(large_height),
		str(small_height + 50)
	]
)


#Compare both images and print results in command line

