#!/usr/bin/python

"""
" cvpy.py
" python-cv
"
" Created by Arman Garakani on 9/9/13.
" Copyright 2013 Arman Garakani. All rights reserved.
"""
# write your python code below

import PIL
import fnmatch
import os
import Tkinter
from PIL import Image, ImageTk
import tkFileDialog
import cv
from fitellipse import FitEllipse
from opencvface import Haarface


class tracer:
    def __init__(self, func):             # On @ decoration: save original func
        self.calls = 0
        self.func = func
    def __call__(self, *args):            # On later calls: run original func
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        self.func(*args)



def searchpath(path, target):
    hits = []
    def scandirs(path):
        for currentFile in glob.glob( os.path.join(path, '*') ):
            if os.path.isdir(currentFile):
                scandirs(currentFile)
            (file_path, dir_name) = os.path.split(currentFile)
            if dir_name == target:
                hits.append ((dir_name, currentFile))
    scandirs(path)
    return hits

def check_absolute (abs_or_rel_path):
    """
        Returns a a tuple (exists, absolute_path)
        """
    # relative or path return (exists, absolute)
    if os.path.isabs (abs_or_rel_path):
        return (os.path.exists(abs_or_rel_path), abs_or_rel_path)
    abs_path = os.path.abspath (abs_or_rel_path)
    return (os.path.exists( abs_path), abs_path)


def yieldfiles (dirname):

    images = ['*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff']

    for root, dirnames, filenames in os.walk(dirname):
        for extensions in images:
            for filename in fnmatch.filter(filenames, extensions):
                yield os.path.join(root, filename)

@tracer
def print_path (filename):

    print filename



def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.

@tracer
def display_wait (filename, troot):

    try:
        fimage = Image.open (filename)
        troot.geometry('%dx%d' % (fimage.size[0],fimage.size[1]))
        (width, height) = fimage.size
        geom = str(width) + 'x' + str ( height )

        tkpi = ImageTk.PhotoImage(fimage)

        label_image = Tkinter.Label(troot, image=tkpi)
        label_image.place(x=0,y=0,width=width,height=height)
        label_image.pack()
        root.mainloop ()
    except Exception, e:
        pass

@tracer
def display_wait_highgui (filename):
    
    src=cv.LoadImage(filename, 0);
    cv.NamedWindow( "Source", 1 );
    cv.ShowImage( "Source", src );
    cv.WaitKey(0);

@tracer
def fit_ellipse_dynamic (filename, intensity):
    
    source_image = cv.LoadImage(filename, cv.CV_LOAD_IMAGE_COLOR)
      # Create windows.
    cv.NamedWindow("Source", 1)
    cv.NamedWindow("Result", 1)

    # Show the image.
    cv.ShowImage("Source", source_image)

    fe = FitEllipse(source_image, 70, intensity)

    print "Press any key to exit"
    cv.WaitKey(0)

    cv.DestroyWindow("Source")
    cv.DestroyWindow("Result")
  
@tracer
def haarface (filename):
    
    source_image = cv.LoadImage(filename, cv.CV_LOAD_IMAGE_COLOR)
  
 

    hf = Haarface (source_image)


@tracer
def print_mom0 (filename):

    fimage = cv.LoadImage (filename, cv.CV_LOAD_IMAGE_GRAYSCALE)
    v = cv.Avg (fimage);
    print v;



def process_path_tk (dirname):

    root = Tkinter.Tk ()
    root.bind("<Button>", button_click_exit_mainloop)

    for fname in yieldfiles (dirname):
        display_wait(fname, root)


def process_path (dirname):
        
    gray_is_true = False
    for fname in yieldfiles (dirname):
        haarface (fname)


        