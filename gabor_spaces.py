#!/usr/bin/env python

'''
gabor_threads.py
=========

Sample demonstrates:
- use of multiple Gabor filter convolutions to get Fractalius-like image effect (http://www.redfieldplugins.com/filterFractalius.htm)
- use of python threading to accelerate the computation

Usage
-----
gabor_threads.py [image filename]

'''


from multiprocessing.pool import ThreadPool

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv
import cv2

def build_filters(ksize, sigma, a, b, c):
    filters = []
    for theta in np.arange(0, np.pi, np.pi / 16):
        kern = cv2.getGaborKernel((ksize, ksize), sigma, theta, a, b, c, ktype=cv2.CV_32F)
        kern /= 1.5*kern.sum()
        filters.append(kern)
    return filters

def display_filter (ksize, sigma, a, b, c, fi):
    filters = build_filters (ksize, sigma, a, b, c)
    plt.imshow (filters[fi], cmap = cm.Greys_r)
    plt.show()


def build_gfilters(ksize, sigma):
    filters = []
    kern = cv2.getGaussianKernel(ksize, sigma, ktype=cv2.CV_32F)
    k2 = kern * cv2.transpose (kern)
    filters.append(kern)
    return filters



def process_threaded(img, filters, threadn = 8):

    def f(kern):
        return cv2.matchTemplate(img, kern, cv.CV_TM_CCORR_NORMED)
    pool = ThreadPool(processes=threadn)
    accum = None
    for fimg in pool.imap_unordered(f, filters):
        if (accum == None) :
           accum = np.zeros_like (fimg)
        accum += fimg * fimg
    return accum

if __name__ == '__main__':
    import sys
    from common import Timer

    print __doc__
    try: img_fn = sys.argv[1]
    except: img_fn = '../cpp/baboon.jpg'

    gimg = cv2.imread(img_fn, 0)
    img = gimg.astype (np.float32) / 255.0
    filters = build_filters(127, 15.0, 127.0, 1.0, 0.5)
    gfilters = build_gfilters (127, 31.0)
    with Timer('running multi-threaded'):
        res2 = process_threaded (img, gfilters)

    plt.imshow(res2, cm.Greys_r)
    plt.show ()

    cv2.imshow('img', img)
    cv2.waitKey()
    cv2.destroyAllWindows()
