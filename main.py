#coding: utf-8
import pygame
from pygame.locals import *

import random
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
	

def simple_comparison(img1, img2):
	img1_size = img1.get_size()
	img2_size = img2.get_size()
	#re-scale smaller image to larger image
	if img1_size[0]*img1_size[1] < img2_size[0]*img2_size[1]:
		img1 = pygame.transform.scale(img1, img2_size)
	else:
		img2 = pygame.transform.scale(img2, img1_size)

	save_image_with_size(img1, img1.get_size(), 'a.png')[1]()
	save_image_with_size(img2, img2.get_size(), 'b.png', 200)[1]()
	
	#go through all pixels and count equalities and differences
	equal, different = 0, 0
	for row in range(img1.get_height()):
		for column in range(img2.get_width()):
			if img1.get_at((column, row)) == img2.get_at((column, row)):
				equal += 1
			else:
				different += 1
	print equal, different
	print "simple_comparison says that probability of being the same is {}".format(float(equal)/(equal+different))

def compare_random(img1, img2):
	def points_similarity(p1, p2):
		if (abs(p1[0] - p2[0]) <= 8 and
			abs(p1[1] - p2[1]) <= 8 and
			abs(p1[2] - p2[2]) <= 8
		):
			return 1
		elif (abs(p1[0] - p2[0]) <= 20 and
		      abs(p1[1] - p2[1]) <= 20 and
			  abs(p1[2] - p2[2]) <= 20
		):	
			return 0.5
		else:
			return 0
		

	#get a hundred random points
	points_pairs = []
	for i in range(100):
		r = random.random()
		p_img1 = int(r*img1.get_width()), int(r*img1.get_height())
		p_img2 = int(r*img2.get_width()), int(r*img2.get_height())
		points_pairs.append((p_img1, p_img2))

	very_similar, similar, not_similar = 0, 0, 0
	#compare points
	for pair in points_pairs:
		point_similarity = points_similarity(img1.get_at(pair[0]), img2.get_at(pair[1]))
		if point_similarity is 1:
			very_similar += 1
		elif point_similarity is 0.5:
			similar += 1
		else:
			not_similar += 1

	print very_similar, similar, not_similar
	similarity = float(2*very_similar + similar)/(2*very_similar + similar + 3*not_similar)
	#print "compare_random says that probability of being the same is {}".format(similarity)
	return similarity


def statistical_compare_random(img1, img2):
	sum_similarities = 0
	for i in range(10):
		sum_similarities += compare_random(img1, img2)
	print "statistical_compare_random says that probability of being the same is {}".format(float(sum_similarities)/10)


def color_histogram_region_comparison(img1, img2):
	BUCKETS = 4
	REGIONS = 10

	class Buckets():
		def __init__(self):
			self.red_buckets = {i:0 for i in range(BUCKETS)}
			self.green_buckets = {i:0 for i in range(BUCKETS)}
			self.blue_buckets = {i:0 for i in range(BUCKETS)}

		def add_color(color):
			red = color[0]
			self.red_buckets[round(float(red*BUCKETS)/255)] += 1

			green = color[1]
			self.green_buckets[round(float(green*BUCKETS)/255)] += 1

			blue = color[2]
			self.blue_buckets[round(float(blue*BUCKETS)/255)] += 1

		def normalize(self):
			total_pixels = sum(self.red_buckets.values())
			for bucket, count in self.red_buckets.items():
				self.red_buckets[bucket] = float(count)/total_pixels
			for bucket, count in self.green_buckets.items():
				self.green_buckets[bucket] = float(count)/total_pixels
			for bucket, count in self.blue_buckets.items():
				self.blue_buckets[bucket] = float(count)/total_pixels

	def make_normalized_buckets(img):
		width = img.get_width()
		height = img.get_height()
		all_region_buckets = []
		#makes a group of buckets for each region
		for x_region in range(REGIONS):
			for y_region in range(REGIONS):
				current_region_buckets = Buckets()
				for x in range(int(float(x_region*width)/REGIONS), int(float((x_region+1)*width)/REGIONS)):
					for y in range(int(float(y_region*height)/REGIONS), int(float((y_region+1)*height)/REGIONS)):
						current_region_buckets.add_color(img.get_at((x, y)))
				current_region_buckets.normalize()
				all_region_buckets.append(current_region_buckets)

		return all_region_buckets

	def similar_buckets(buckets_per_region1, buckets_per_region2):
		def compare_color_buckets(color_buckets1, color_buckets2):
			difference_sum = 0
			for key in color_buckets1.keys():
				difference_sum += abs(color_buckets1[key] - color_buckets2[key])
			
			return difference_sum < 0.2

		if compare_color_buckets


	img1_per_region_buckets = make_normalized_buckets(img1)
	img2_per_region_buckets = make_normalized_buckets(img2)
	similar, different = 0, 0
	for buckets_per_region1, buckets_per_region2 in zip(img1_per_region_buckets, img2_per_region_buckets):
		if similar_buckets(buckets_per_region1, buckets_per_region2):
			similar += 1
		else:
			different += 1

	similarity = float(similar)/(similar + different)
	return similarity


def compare_images(img1, img2):
	simple_comparison(img1, img2)
	statistical_compare_random(img1, img2)
	return 1

#Executes the main program
def main():

	#First of all, let's ask what image we shall use
	print "Qual imagem você quer usar? Digite o nome do arquivo se ele estiver no diretório atual, "\
		  "e o endereço completo se ele estiver em outro diretório."
	filename = raw_input()
	img = pygame.image.load(filename)
	#print dir(img)


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

	#open_small_image()
	#open_large_image()

	#Compare both images and print results in command line
	compare_images(small_img, large_image)


main()