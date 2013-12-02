#coding: utf-8
import pygame
from pygame.locals import *

import random


#re-scales smaller image to larger image size, and makes a comparison iterating 
#through all the pixels
def simple_comparison(img1, img2):
	img1_size = img1.get_size()
	img2_size = img2.get_size()
	#re-scale smaller image to larger image
	if img1_size[0]*img1_size[1] < img2_size[0]*img2_size[1]:
		img1 = pygame.transform.scale(img1, img2_size)
	else:
		img2 = pygame.transform.scale(img2, img1_size)
	
	#go through all pixels and count equalities and differences
	equal, different = 0, 0
	for row in range(img1.get_height()):
		for column in range(img2.get_width()):
			if img1.get_at((column, row)) == img2.get_at((column, row)):
				equal += 1
			else:
				different += 1
	
	similarity = float(equal)/(equal+different)
	return similarity


#selects 100 random points in the images and check if they're similar.
def random_comparison(img1, img2):
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

	similarity = float(2*very_similar + similar)/(2*very_similar + similar + 3*not_similar)
	return similarity


#since at random_comparison the chosen points are random, let's run that 10 times to get an average
def statistical_random_comparison(img1, img2):
	sum_similarities = 0
	for i in range(10):
		sum_similarities += random_comparison(img1, img2)
	
	average_similarity = float(sum_similarities)/10
	return average_similarity


#Separates the images into regions, and creates histograms for each color in each region.
#Compares the histograms and, based on the number of similar regions, compares the images.
def color_histogram_region_comparison(img1, img2):
	BUCKETS = 4
	REGIONS = 10

	class Buckets():
		def __init__(self):
			self.red_buckets = {i:0 for i in range(BUCKETS)}
			self.green_buckets = {i:0 for i in range(BUCKETS)}
			self.blue_buckets = {i:0 for i in range(BUCKETS)}

		def add_color(self, color):
			red = color[0]
			self.red_buckets[min(int(BUCKETS*float(red)/255), BUCKETS-1)] += 1

			green = color[1]
			self.green_buckets[min(int(BUCKETS*float(green)/255), BUCKETS-1)] += 1

			blue = color[2]
			self.blue_buckets[min(int(BUCKETS*float(blue)/255), BUCKETS-1)] += 1

		def normalize(self):
			total_pixels = sum(self.red_buckets.values())
			for bucket, count in self.red_buckets.items():
				self.red_buckets[bucket] = float(count)/total_pixels
			for bucket, count in self.green_buckets.items():
				self.green_buckets[bucket] = float(count)/total_pixels
			for bucket, count in self.blue_buckets.items():
				self.blue_buckets[bucket] = float(count)/total_pixels

	def make_normalized_buckets_per_region(img):
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
		def similar_color_buckets(color_buckets1, color_buckets2):
			difference_sum = 0
			for key in color_buckets1.keys():
				difference_sum += abs(color_buckets1[key] - color_buckets2[key])
			#print difference_sum
			return difference_sum < 0.15

		if (similar_color_buckets(buckets_per_region1.red_buckets, buckets_per_region2.red_buckets) and
			similar_color_buckets(buckets_per_region1.green_buckets, buckets_per_region2.green_buckets) and
			similar_color_buckets(buckets_per_region1.blue_buckets, buckets_per_region2.blue_buckets)
		):
			return True
		else:
			return False


	img1_per_region_buckets = make_normalized_buckets_per_region(img1)
	img2_per_region_buckets = make_normalized_buckets_per_region(img2)
	similar_regions, different_regions = 0, 0
	for buckets_per_region1, buckets_per_region2 in zip(img1_per_region_buckets, img2_per_region_buckets):
		if similar_buckets(buckets_per_region1, buckets_per_region2):
			similar_regions += 1
		else:
			different_regions += 1

	similarity = float(similar_regions)/(similar_regions + 2*different_regions)
	return similarity
