import time
import SimpleCV as cv


cam=cv.Camera(0, { "width": 640, "height": 480 })

while(True):
    img=cam.getImage()
    barcode=img.toGray().findBarcode()
    #if(barcode): barcode.draw()
    #img.show()
    time.sleep(1)
    if(barcode != None):
        #for n in barcode:                                                    
         #   print(n)                                                         
        #print(barcode.height()[0])#distanceFrom()[0])                        
        #print((640*7)/barcode[0].width())#.data) 
        print(4500/barcode[0].width())
