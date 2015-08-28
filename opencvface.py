#!/usr/bin/python
import os
import sys
import cv2
import cv2.cv as cv
import numpy as np
from common import clock, draw_str

sys.path.append(os.path.dirname(__file__))

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''


class Haarface:

    def __init__(self, source_image):
        
    
          
        self.cascade_fn = os.path.dirname(__file__) + "/haarcascade_frontalface_alt.xml"
        self.nested_fn  = os.path.dirname(__file__) + "/haarcascade_eye.xml"

        self.cascade = cv2.CascadeClassifier(self.cascade_fn)
        self.nested = cv2.CascadeClassifier(self.nested_fn)
    
    
        self.source_color = source_image
        self.source_image = cv2.cvtColor(np.asarray(self.source_color[:,:]), cv2.COLOR_BGR2GRAY)
        self.gray = np.asarray(self.source_image, dtype=np.uint8)
        self.gray = cv2.equalizeHist(self.gray)
       
                                                            
        
        self.process_image()
       

    def draw_rects(img, rects, color):
       for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


    def detect(self, img, cascade):
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        return rects

   

    def draw_rects(self, img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


    def process_image(self):
        """
        This function finds faces, draws them and their approximation by ellipses.
        """
        t = clock()
        rects = self.detect(self.gray, self.cascade)
        vis = self.source_color
        self.draw_rects(np.asarray(vis[:,:]), rects, (0, 255, 0))
        for x1, y1, x2, y2 in rects:
            roi = self.gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            subrects = self.detect(roi.copy(), self.nested)
            self.draw_rects(np.asarray(vis_roi[:,:]), subrects, (255, 0, 0))
        dt = clock() - t

        draw_str(np.asarray(vis[:,:]), (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect',  np.asarray(vis[:,:]))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
      
