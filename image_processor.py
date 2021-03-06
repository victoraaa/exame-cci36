# coding: utf-8

import os

import pygame
from pygame.locals import *

from comparisons import simple_comparison, statistical_random_comparison, color_histogram_region_comparison

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
#This is a complicated function that I'm not proud of, but what the hell
def save_image_with_size(img, size, filename, y_pos=0):

    new_img = pygame.transform.scale(img, size)
    pygame.image.save(new_img, filename)

    return new_img, wrapper(open_subprocess_with_img, filename, size, y_pos)


def compare_images(img1, img2):
    result_1 = "Simple comparison algorithm: {}"
    result_1 = result_1.format(simple_comparison(img1, img2))

    result_2 = "Statistical Random Comparison: {}"
    result_2 = result_2.format(statistical_random_comparison(img1, img2))

    result_3 = "Region Buckets: {}"
    result_3 = result_3.format(color_histogram_region_comparison(img1, img2))

    return (result_1, result_2, result_3)
    # print "simple_comparison says that probability of being the same is {}".format(simple_comparison(img1, img2))
    # print "statistical_random_comparison says that probability of being the same is {}".format(statistical_random_comparison(img1, img2))
    # print "region-buckets says that probability of being the same is {}".format(color_histogram_region_comparison(img1, img2))


def create_images(file_name, size):

    #First of all, let's ask what image we shall use
    # print "Qual imagem você quer usar? Digite o nome do arquivo se ele estiver no diretório atual, "\
    #       "e o endereço completo se ele estiver em outro diretório."
    # filename = raw_input()
    img = pygame.image.load(file_name)

    #Then, get the size:
    print "Qual a largura desejada da janela? O menor valor aceito é 20px, e o maior, 200px"
    small_width = max(20, min(int(size[0]), 200))
    large_width = int(2.75 * small_width)
    print "Qual a altura desejada da janela? O menor valor aceito é 20px, e o maior, 150px"
    small_height = max(20, min(int(size[1]), 150))
    large_height = int(2.75 * small_height)

    file_name = file_name.split(os.sep)[-1]
    file_names = ("small_{}".format(file_name), "large_{}".format(file_name))
    #Scale image to small size, save it
    small_img, open_small_image = save_image_with_size(img, (small_width, small_height), file_names[0])

    #Scale image to large size, save it
    large_image, open_large_image = save_image_with_size(img, (large_width, large_height), file_names[1], small_width + 100)

    open_small_image()
    open_large_image()

    #Compare both images and print results in command line
    results = compare_images(small_img, large_image)

    return (file_names, results)
