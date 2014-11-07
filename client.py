#!/usr/bin/python

'''
Created on Sep 14, 2014

@author: shalom
'''

from Tkinter import *
from ttk import *
import time
import logging
import math
import io
import os




try:
    if os.uname()[1] == 'raspberrypi':
        import picamera
        isPy = True
    else:
        import pygame
        import pygame.camera
        from pygame.locals import *
        isPy = False
    import Image
    import ImageChops
except:
    print """
        Couldn't import some packages. Try the following and then run again:
        sudo apt-get install python-picamera python3-picamera python-rpi.gpio python-imaging
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

def takePictureIntoFile(camera):
    logger.info('Take a picture')
    dateNow = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())
    fileName = '/tmp/image-%s.jpg' % dateNow
    camera.capture(fileName)
    logger.info('Picture taken %s', fileName)
    return fileName

#=======================================

def takePictureIntoImage(camera):
    if isPy:
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        image = Image.open(stream)
        return image
    else:
        camSurf = camera.get_image()
        data = pygame.image.tostring( camSurf, 'RGBA')
        image = Image.fromstring('RGBA', camSurf.get_size(), data)
        return image



#=======================================
def normalizeComponent(histogram, offset, length):
    pass

#=======================================

def normalizeHistogram(histogram):
    componentLength = len(histogram) / 3

    for component in range(1, 3):
        normalizeComponent(histogram, componentLength * component, componentLength)

#=======================================

def rmsDiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    # diff = ImageChops.difference(im1, im2)
    # diff.histogram()

    h1 = im1.histogram()
    h2 = im2.histogram()


    sq = (((pix1 - pix2) ** 2) for pix1, pix2 in zip(h1, h2))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / min(len(h1), len(h2)))
    return rms

#=======================================

def doNextImage(previousImage, camera):
    nextImage = takePictureIntoImage(camera)

    if previousImage:
        logger.info("Have previous file %s", previousImage);
        # nextImage = Image.open(nextImageFile)
        # previousImage = Image.open(previousImageFile)
        diff = rmsDiff(previousImage, nextImage)
        logger.info("Diff is: %f", diff)

    return nextImage


#=======================================
def imageCycle(cycleTime):
    previousImage = None

    if isPy:
        with picamera.PiCamera() as camera:
            while True:
                previousImage = doNextImage(previousImage, camera)
                time.sleep(cycleTime)
    else:
        cam = pygame.camera.Camera("/dev/video0",(640,480))
        cam.start()
        while True:
            previousImage = doNextImage(previousImage, cam)
            time.sleep(cycleTime)

#=======================================
#=======================================


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    
    if not isPy:
        pygame.init()
        pygame.camera.init()

    imageCycle(0.5)


