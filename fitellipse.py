#!/usr/bin/python
"""
This program is a demonstration of ellipse fitting.

Trackbar controls threshold parameter.

Gray lines are contours.  Colored lines are fit ellipses.

Original C implementation by:  Denis Burenkov.
Python implementation by: Roman Stanchak, James Bowman
"""

import sys
import random
import cv2.cv as cv

# some definitions
win_name = "Edge"
trackbar_name = "Threshold"

def contour_iterator(contour):
    while contour:
        yield contour
        contour = contour.h_next()

class FitEllipse:

    def __init__(self, source_image, slider_pos, use_intensity):
        
        self.source_color = source_image
        self.source_image = cv.CreateImage((self.source_color.width, self.source_color.height), 8, 1)
        cv.CvtColor(self.source_color, self.source_image, cv.CV_BGR2GRAY)
        self.intensity = use_intensity
        
        if self.intensity == False :
 
            # create the output im
            self.col_edge = cv.CreateImage((self.source_image.width, self.source_image.height), 8, 3)
        
            self.edge = cv.CreateImage((self.source_image.width, self.source_image.height), 8, 1)
            
        cv.CreateTrackbar("Threshold", "Result", slider_pos, 255, self.process_image)
        self.process_image(slider_pos)
       
  
    def on_trackbar(self, position):

        cv.Smooth(self.source_image, self.edge, cv.CV_BLUR, 3, 3, 0)
        cv.Not(self.source_image, self.edge)
    
        # run the edge dector on gray scale
        cv.Canny(self.source_image, self.edge, position, position * 3, 3)
    
        # reset
        cv.SetZero(self.col_edge)
    
        # copy edge points
        cv.Copy(self.source_color, self.col_edge, self.edge)
    
        # show the im
        cv.ShowImage(win_name, self.col_edge)
        self.process_image (position)


    def process_image(self, slider_pos):
        """
        This function finds contours, draws them and their approximation by ellipses.
        """
        use_this = self.source_image
        if self.intensity == False :
            cv.Smooth(self.source_image, self.edge, cv.CV_BLUR, 9, 9, 0)
            cv.Not(self.source_image, self.edge)
        
            # run the edge dector on gray scale
            cv.Canny(self.source_image, self.edge, slider_pos, slider_pos * 3, 3)
        
            # reset
            cv.SetZero(self.col_edge)
        
            # copy edge points
            cv.Copy(self.source_color, self.col_edge, self.edge)
            use_this = self.edge
     
            
        stor = cv.CreateMemStorage()
    
        # Create the destination images
        image02 = cv.CloneImage(use_this)
        cv.Zero(image02)
        image04 = cv.CreateImage(cv.GetSize(self.source_image), cv.IPL_DEPTH_8U, 3)
        cv.Zero(image04)
    
        # Threshold the source image. This needful for cv.FindContours().
        cv.Threshold(use_this, image02, slider_pos, 255, cv.CV_THRESH_BINARY)
    
        # Find all contours.
        cont = cv.FindContours(image02,
            stor,
            cv.CV_RETR_LIST,
            cv.CV_CHAIN_APPROX_NONE,
            (0, 0))
    
        for c in contour_iterator(cont):
            # Number of points must be more than or equal to 6 for cv.FitEllipse2
            if len(c) >= 6:
                # Copy the contour into an array of (x,y)s
                PointArray2D32f = cv.CreateMat(1, len(c), cv.CV_32FC2)
                for (i, (x, y)) in enumerate(c):
                    PointArray2D32f[0, i] = (x, y)
    
                # Draw the current contour in gray
                gray = cv.CV_RGB(100, 100, 100)
                cv.DrawContours(image04, c, gray, gray,0,1,8,(0,0))
    
                # Fits ellipse to current contour.
                (center, size, angle) = cv.FitEllipse2(PointArray2D32f)
    
                # Convert ellipse data from float to integer representation.
                center = (cv.Round(center[0]), cv.Round(center[1]))
                size = (cv.Round(size[0] * 0.5), cv.Round(size[1] * 0.5))
    
                # Draw ellipse in random color
                color = cv.CV_RGB(random.randrange(256),random.randrange(256),random.randrange(256))
                cv.Ellipse(image04, center, size,
                          angle, 0, 360,
                          color, 2, cv.CV_AA, 0)
    
        # Show image. HighGUI use.
        cv.ShowImage( "Result", image04 )


  