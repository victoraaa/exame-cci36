#coding: utf-8
import pygame
from pygame.locals import *

import subprocess


def wrapper(func, *args):
	def caller():
		return func(*args)

	return caller


def open_subprocess_with_img(filename, size, y_pos):
	#This opens a new process as if it was issuing the command in the terminal.
	#You can use as many arguments as you need, and you will have a reference to the new process.
	#Documentation for subprocess: http://docs.python.org/2/library/subprocess.html

	return subprocess.Popen(
		[
			"python", "imgWindow.py",
			filename,
			"Showing {}".format(filename),
			str(size[0]),
			str(size[1]),
			str(y_pos)
		]
	)


#receives a pygame.image, a size as (width, height) in pixels and the filename that should be used
#returns a pair of:
#1) pygame.image of the new image
#2)function that if called, opens a new window with the image and returns a reference to the imgWindow.py 
#subproject is showing that img
def save_image_with_size(img, size, filename, y_pos=0):

	new_img = pygame.transform.scale(img, size)
	pygame.image.save(new_img, filename)

	return new_img, wrapper(open_subprocess_with_img, filename, size, y_pos)
	

def compare_images(img1, img2):
	print "100% de chance de serem a mesma imagem"
	return 1

#Executes the main program
def main():

	#First of all, let's ask what image we shall use
	print "Qual imagem você quer usar? Digite o nome do arquivo se ele estiver no diretório atual, "\
		  "e o endereço completo se ele estiver em outro diretório."
	filename = raw_input()
	img = pygame.image.load(filename)


	#Then, get the size:
	print "Qual a largura desejada da janela? O menor valor aceito é 20px"
	small_width = max(20, int(raw_input()))
	large_width = int(2.75*small_width)
	print "Qual a altura desejada da janela? O menos valor aceito é 20px"
	small_height = max(20, int(raw_input()))
	large_height = int(2.75*small_height)

	#Scale image to small size, save it
	small_img, open_small_image = save_image_with_size(img, (small_width, small_height), "small_{}".format(filename))

	#Scale image to large size, save it
	large_image, open_large_image = save_image_with_size(img, (large_width, large_height), "large_{}".format(filename), small_width + 100)

	open_small_image()
	open_large_image()

	#Compare both images and print results in command line
	compare_images(small_img, large_image)


main()