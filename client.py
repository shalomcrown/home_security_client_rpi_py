#!/usr/bin/python

'''
Created on Sep 14, 2014

@author: shalom
'''

from Tkinter import *
from ttk import *
import time
import logging



try:
    import picamera
    from PIL import Image
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
      self.password =  self.passwordEntry.get()
      self.url = self.serverUrlMenu.get()
      self.OK = True
      self.root.destroy()

   def run(self):
      self.root = Tk()
      self.root.title('HomeSec - Login')

      label = Label(self.root, text='Server login details', font = "Verdana 10 bold")
      label.grid(column=0, columnspan=2, row=0)

      Label(self.root, text="Server URL").grid(row = 1, column=0)
      self.serverUrlMenu = Combobox(self.root, values=["localhost:8080"])
      self.serverUrlMenu.grid(row=1, column=1)

      Label(self.root, text="User Name").grid(row = 2, column=0)
      self.usernameEntry = Entry(self.root)
      self.usernameEntry.grid(row=2, column=1)
      
      Label(self.root, text="Password").grid(row=3, column=0)
      self.passwordEntry = Entry(self.root, show="*")
      self.passwordEntry.grid(row=3, column = 1)
      
      Separator(self.root, orient='horizontal').grid(row=4, column=0, columnspan=2)
      
      cancelButton = Button(self.root, text="Cancel", command=self.pressedCancel).grid(row=5, column=0)
      Button(self.root, text="OK", command=self.pressedOk).grid(row=5, column=1, sticky=E)
      
      self.root.mainloop()

      return self.OK
      


def testLogin():
   pass

#=======================================

def takePicture():
    logger.info('Take a picture')
    with picamera.PiCamera() as cam:
        dateNow = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())
        fileName = '/tmp/image-%s.jpg' % dateNow
        cam.capture(fileName)
        logger.info('Picture taken %s', fileName)
        return fileName

#=======================================

def rmsDiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*(idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

#=======================================

def doNextImage(previousImageFile):
    nextImageFile = takePicture()

    if previousImageFile:
        logger.info("Have previous file %s", previousImageFile);
        with Image.open(nextImageFile) as nextImage:
            with Image.open(previousImageFile) as previousImage:
                diff = rmsDiff(previousImage, nextImage)
                logger.info("Diff is: %f", diff)
    
    return nextImageFile


#=======================================
def imageCycle(cycleTime):
    previousImageFile = None
    
    while True:
        previousImageFile = doNextImage(previousImageFile)
        time.sleep(cycleTime)

#=======================================
#=======================================


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    imageCycle(0.5)

    
