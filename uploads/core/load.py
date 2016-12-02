from scipy import misc

import numpy as np
from math import pow, sqrt

from uploads.core.models import Sprite
from django.core.files import File

import sys
import os

def load_all_images():
    # images_hist = []
    for filename in os.listdir('/home/mfurquim/projects/imageorganizer/media/images'):
        sprite = Sprite()
        sprite.image.save(filename, File(open('/home/mfurquim/projects/imageorganizer/media/images/'+filename, 'rb')))
        sprite.save()
        # image = load_image("images/"+filename)
        # image_tuple = (filename,image)
        # images_hist.append(image_tuple)
        # images_hist

def get_closests(uploaded, sprites):
    uploaded_hist = load_image("media/"+uploaded)
    images_hist = load_images_hist(sprites)
    unordered_dist = []
    for img in images_hist:
        img_hist = img[1]
        dist = distance(img_hist, uploaded_hist)
        img_tupple = (img[0], dist)
        unordered_dist.append(img_tupple)
    ordered_dist = sorted(unordered_dist, key=lambda tup: tup[1])
    return ordered_dist


def load_images_hist(sprites):
    images_hist = []
    for sprt in sprites:
        img_hist = load_image("media/"+sprt.image.name)
        image_tuple = (sprt,img_hist)
        images_hist.append(image_tuple)
    return images_hist

def load_image(filename):
    img = misc.imread(filename)
    hist = get_hist(img)
    return hist

def get_hist(image):
    image = image[::4,::4,:]
    # Normalizing images:
    im_norm = (image-image.mean())/image.std()

    # Computing a 10-bin histogram in the range [-e, +e] (1 standard deviationto 255 for each of the colours:
    # (the first element [0] is the histogram, the second [1] is the array of bins.)
    hist_red = np.histogram(im_norm[:,:,0], range=(-np.e,+np.e))[0]
    hist_green = np.histogram(im_norm[:,:,1], range=(-np.e,+np.e))[0]
    hist_blue = np.histogram(im_norm[:,:,2], range=(-np.e,+np.e))[0]
    # Concatenating them into a 30-dimensional vector:
    histogram = np.concatenate((hist_red, hist_green, hist_blue)).astype(np.float)
    return histogram/histogram.sum()
#
# images_hist = load_all_images()
#
# # print (images_hist[0][1])
def distance(hist1, hist2):
    dist = 0
    for i in range(len(hist1)):
        diff = hist1[i] - hist2[i]
        dist += pow(diff, 2.0)
    dist = sqrt(dist)
    return dist
#
# def closest(images_hist, hist):
#     unordered_dist = []
#     for img in images_hist:
#         img_hist = img[1]
#         dist = distance(img_hist, hist)
#         img_tupple = (img[0], dist)
#         unordered_dist.append(img_tupple)
#     ordered_dist = sorted(unordered_dist, key=lambda tup: tup[1])
#     return ordered_dist
#
# images = load_all_images()
# cl = closest(images, images[2345][1])
# firsts = []
# for a in cl:
#     if a[1] > 0.175:
#         break
#     firsts.append(a)
#
# for c in firsts:
#     print (c)
#
# for c in firsts:
#     print ("feh images/%s &" % c[0])
