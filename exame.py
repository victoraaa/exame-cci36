#coding: utf-8

import pygame
import time

pygame.init()
w = 640
h = 480
size=(w,h)
screen = pygame.display.set_mode(size, pygame.RESIZABLE) 
c = pygame.time.Clock() # create a clock object for timing


filename="imgpeq.png"
img=pygame.image.load(filename)

img = pygame.transform.scale(img, (100,100))

print dir(img)
print img.get_width()
print img.get_height()
for line in range(1):
    print [img.get_at((line, column)) for column in range(img.get_height())]
    
#print img.__dict__
screen.blit(img,(0,0))
pygame.display.flip() # update the display
while True:
    for event in pygame.event.get ():
        if event.type == pygame.VIDEORESIZE:
            width, height = event.size
    pass
    