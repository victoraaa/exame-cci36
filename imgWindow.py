import pygame
from pygame.locals import *
import sys

filename = sys.argv[1]
caption = sys.argv[2]
width = int(sys.argv[3])
heigth = int(sys.argv[4])
window_position_x = int(sys.argv[5])

print filename
print caption
print width
print heigth

import os  

os.environ['SDL_VIDEO_WINDOW_POS'] = str(window_position_x) + ",0"

pygame.init()
display = pygame.display.set_mode((width, heigth))
pygame.display.set_caption(caption)
gameOver=False

img = pygame.image.load(filename) 
display.blit(img,(0,0))
pygame.display.flip() # update the display

while not gameOver:
    for e in pygame.event.get():
        if e.type==QUIT:
            gameOver=True
        if e.type==KEYDOWN:
            if e.key==K_ESCAPE:
                gameOver=True
                

#print the comparison in the shell
#bla
#bla
