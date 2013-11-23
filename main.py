import pygame
from pygame.locals import *

import subprocess

#First of all, let's ask what image we shall use
print "What image do you want to use?"
filename = raw_input()

#Then, get the size:
print "What should be the width of the window? Minimum value is 20px"
width = max(20, int(raw_input()))
print "What should be the height of the window? Minimum value is 20px"
height = max(20, int(raw_input()))

#This opens a new process as if it was issuing the command in the terminal.
#You can use as many arguments as you need, and you will have a reference to the new process.
#Documentation for subprocess: http://docs.python.org/2/library/subprocess.html
subp = subprocess.Popen(["python", "largeWindow.py", "argument1", "second argument"])

#Scale image to small size, save it
#Initialize the first window, passing image and size
#bla bla

#Scale image to large size, save it
#Initialize the second window, passing image and large size
#bla bla


#Compare both images and print results in command line

