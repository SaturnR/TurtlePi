import time
import numpy as np
from SimpleCV import *

cam=Camera(0, { "width": 640, "height": 480 })

while(True):
    img=cam.getImage()
    bar=img.toGray().findBarcode()
    #img.show()
    time.sleep(1)
    if(bar!=None): 
        #bar.draw(Color.GREEN) #draw the outline of the barcode in green
        print(bar)
