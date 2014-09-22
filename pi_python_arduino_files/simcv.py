#! /usr/bin/env python

import time
import os.path as path
from SimpleCV import Color, Image, np, Camera

class ObjectRead():
    def __init__(self, display=False):
        self.display=display
    
    img=None
    cam=None
    
    def startCamera(self,width=640,height=480):
        self.cam = Camera(0, { "width": width, "height": height })
        return self.cam
    
    def getImage(self):
        self.img=self.cam.getImage()
        return self.img    
    
class QR(ObjectRead):
    
    img=None
    bar=None
    def __init__(self,display=False):
        self.display=display
    
    def getXY(self):
        self.img=self.getImage()
        self.bar=self.img.toGray().findBarcode()
        if(self.display):
            #if(self.bar): self.bar.draw()
            self.img.show()
            
        return self.bar
    
class Face(ObjectRead):
    faces=None
    face=None
    faceImage=None
    DBfaces=None
    
    def __init__(self,display=False):
        self.display=display
        self.quality = 200 #400
        self.minMatch = 0.3 #0.3
        self.mode = "unsaved"
        self.saved = False
        self.minDist = 0.25
            
    def getXY(self):
        self.img = self.getImage() 
        self.faces = self.img.findHaarFeatures("./facetrack-training.xml")
        ret=None
        if(self.faces): 
            self.face=self.faces[-1]
            #if(self.display):self.face.draw()
            ret= (self.face.x, self.face.y)
        if(self.display): self.img.show()
        return ret
    
    def saveFace(self,name):
        self.img = self.getImage() 
        self.faces = self.img.findHaarFeatures("./facetrack-training.xml")
        ret=True
        if(self.faces): 
            self.face=self.faces[-1]
            #if(self.display): self.face.draw()
            self.face.crop().save("./faces/"+name+".jpg")
            ret=True
        else:
            ret=False 
        if(self.display): self.img.show()
        return ret
    
    def getFace(self, name):
        self.faceImage = Image(name)
        return faceImage
    
    def recognise(self,facename='irakli'):
        if(not facename): savedface=self.face
        self.img = self.getImage()
        self.faces = self.img.findHaarFeatures("./facetrack-training.xml") 
        #if(self.display): self.faces.draw()
        rec=None
        if(self.faces):       
            self.face = self.faces[-1]
            template = self.face.crop()
            template.save("./faces/tempface.jpg")
            rec=Image('./faces/'+facename+'.jpg').findKeypointMatch(template,self.quality,self.minDist,self.minMatch)
        if(self.display): self.img.show()
        return rec


'''
qr=QR(display=True)

qr.startCamera(width=320,height=240) #(width=160,height=120)

while(1):
    xy=qr.getXY()
    print(xy)
    time.sleep(1)
'''
'''
f=Face(display=True)    
cam=f.startCamera()

while(1):
    #f.saveFace('111')
    keypoints=f.recognise('irakli',display=True)
    print(keypoints)
    time.sleep(1)
'''
