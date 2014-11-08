#!/usr/bin/python

'''
Created on Sep 14, 2014

@author: shalom
'''

from Tkinter import *
from ttk import *
import logging
import time




try:
    import numpy as np
    import cv2
    import cv
except:
    print """
        Couldn't import some packages. Try the following and then run again:
        sudo apt-get install python-numpy python-opencv
        sudo modprobe bcm2835-v4l2
    """
    exit(-1)

logger = logging.getLogger(__name__)

#====================================================

class LoginDetails:
    def pressedCancel(self):
        self.OK = False
        self.root.destroy()

    def pressedOk(self):
        self.username = self.usernameEntry.get()
        self.password = self.passwordEntry.get()
        self.url = self.serverUrlMenu.get()
        self.OK = True
        self.root.destroy()

    def run(self):
        self.root = Tk()
        self.root.title('HomeSec - Login')
        
        label = Label(self.root, text='Server login details', font="Verdana 10 bold")
        label.grid(column=0, columnspan=2, row=0)
        
        Label(self.root, text="Server URL").grid(row=1, column=0)
        self.serverUrlMenu = Combobox(self.root, values=["localhost:8080"])
        self.serverUrlMenu.grid(row=1, column=1)
        
        Label(self.root, text="User Name").grid(row=2, column=0)
        self.usernameEntry = Entry(self.root)
        self.usernameEntry.grid(row=2, column=1)
        
        Label(self.root, text="Password").grid(row=3, column=0)
        self.passwordEntry = Entry(self.root, show="*")
        self.passwordEntry.grid(row=3, column=1)
        
        Separator(self.root, orient='horizontal').grid(row=4, column=0, columnspan=2)
        
        cancelButton = Button(self.root, text="Cancel", command=self.pressedCancel).grid(row=5, column=0)
        Button(self.root, text="OK", command=self.pressedOk).grid(row=5, column=1, sticky=E)
        
        self.root.mainloop()
        
        return self.OK



def testLogin():
    pass


#=======================================
#     dateNow = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())

def takePictureIntoImage(camera):
#     camSurf = camera.get_image()
#     data = pygame.image.tostring( camSurf, 'RGBA')
#     image = Image.fromstring('RGBA', camSurf.get_size(), data)

    retval, im = camera.read()
    return im





#=======================================
def normalizeComponent(histogram, offset, length):
    pass

#=======================================

def normalizeHistogram(histogram):
    componentLength = len(histogram) / 3

    for component in range(1, 3):
        normalizeComponent(histogram, componentLength * component, componentLength)

#=======================================

def diffCoeff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    hsv1 = cv2.cvtColor(im1,cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(im2,cv2.COLOR_BGR2HSV)

    h1 = cv2.calcHist([hsv1], [0, 1], None, [180, 256], [0, 180, 0, 256])
    h2 = cv2.calcHist([hsv2], [0, 1], None, [180, 256], [0, 180, 0, 256])

#     h1rgb = cv2.calcHist([im1], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
#     h2rgb = cv2.calcHist([im2], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
        
    cv2.normalize(h1,h1,0,255,cv2.NORM_MINMAX)
    cv2.normalize(h2,h2,0,255,cv2.NORM_MINMAX)
    
#     cv2.normalize(h1rgb,h1rgb,0,255,cv2.NORM_MINMAX)
#     cv2.normalize(h2rgb,h2rgb,0,255,cv2.NORM_MINMAX)
    
    rms = cv2.compareHist(h1, h2, 0)
#     rms = cv2.compareHist(h1rgb, h2rgb, 0)

    return rms

#=======================================

def doNextImage(previousImage, camera):
    nextImage = takePictureIntoImage(camera)

    if previousImage is not None:
        logger.info("Have previous file");
        # nextImage = Image.open(nextImageFile)
        # previousImage = Image.open(previousImageFile)
        diff = diffCoeff(previousImage, nextImage)
        logger.info("Diff is: %f", diff)

    return nextImage


#=======================================
def imageCycle(cycleTime):
    previousImage = None
    cam = cv2.VideoCapture(0)
    #cv2.namedWindow('Homesec image')
    
    while True:
        previousImage = doNextImage(previousImage, cam)
        #cv2.imshow('Homesec image', previousImage);
        #cv2.waitKey(500)
        time.sleep(cycleTime)

#=======================================
#=======================================


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    
    imageCycle(0.5)


