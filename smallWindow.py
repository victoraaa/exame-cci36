import pygame
from pygame.locals import *
import subprocess

#First of all, let's ask what image we shall use
#print something
#filename = raw_input()

#Then, get the size:
#bla
#bla


pygame.init()
surf=pygame.display.set_mode((200,200))
pygame.display.set_caption("Small Window")
gameOver=False

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