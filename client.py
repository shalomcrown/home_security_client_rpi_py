#!/usr/bin/python

'''
Created on Sep 14, 2014

@author: shalom
'''

from Tkinter import *
from ttk import *
import time


try:
    import picamera
except:
    print """
        Couldn't import picamera. Try the following and then run again:
        sudo apt-get install python-picamera python3-picamera python-rpi.gpio imagemagick python-pythonmagick
    """
    exit(-1)


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
#=======================================


if __name__ == "__main__":
    with picamera.PiCamera() as cam:
        dateNow = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())
        #cam.start_preview()
        #time.sleep(5)
        cam.capture('/tmp/image-%s.jpg' % dateNow)
        #cam.stop_preview()

    
