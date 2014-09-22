import spidev
import time
import RPi.GPIO as GPIO

from array import array
import socket
import time
import sys
import simcv
import os

#from Tkinter import Tk
#from tkSimpleDialog import askstring

# --------------- tcp client configuration -------------
#root = Tk()
#root.withdraw()

PORT = 42001
HOST = "192.168.1.155" #"192.168.43.64" #askstring('Scratch Connector', 'IP:')
#if not HOST:
#    sys.exit()
'''
print("Connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("Connected!")

def sendScratchCommand(cmd):
    n = len(cmd)
    a = array('c')
    a.append(chr((n >> 24) & 0xFF))
    a.append(chr((n >> 16) & 0xFF))
    a.append(chr((n >>  8) & 0xFF))
    a.append(chr(n & 0xFF))
    scratchSock.send(a.tostring() + cmd)

def sendValue(name, value):
        """send a 'sensor-update'"""
        bcast_str = 'sensor-update "{name:s}" {value:s}'.format( name=name, value=value)
#        if logger.isEnabledFor(logging.INFO):logger.info('ScratchSender, send value: %s' , bcast_str)       
        scratchSock.send(bcast_str)
'''
# ---------------------------------------------------

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.LOW)

spi=spidev.SpiDev()

spi.open(0,0)

def clear():
    GPIO.output(25, GPIO.HIGH)
    spi.writebytes([0])
    time.sleep(0.05)
    GPIO.output(25, GPIO.LOW)
    time.sleep(0.1)

def readAngle():
    return 0


def moution(ang,m):
    return [0,0]


def left(angle):
    an1=angle/256
    an0=angle%256
    b=[1,1,an1,an0,135,111]
    a=spi.xfer([1,1,an1,an0,135,111])
    time.sleep(0.01)
    while((a[1:]!=b[0:5]) or (a[0]!=0)):
        a=spi.xfer([1,1,an1,an0,135,111])
        if(a[0]==111): 
            GPIO.output(25, GPIO.HIGH)
        else:
            GPIO.output(25, GPIO.LOW)
    print(a)

def right(angle):
    an1=angle/256
    an0=angle%256
    b=[1,2,an1,an0,135,111]
    a=spi.xfer([1,2,an1,an0,135,111])
    print(a)


def goStraight(dist):
    dist_1=dist/256
    dist_0=dist%256
    b=[6,dist_1,dist_0,135,1]
    spi.xfer(b)
    print(b)
    run=True
    n=0
    if(dist<40):cp=5
    else: cp=dist/10
    while(run):
        n+=1
        run=not getFeedback()
        if(n==cp):
            clear()
            goStraight(dist)
        time.sleep(0.1)
    print('End of Command')


def goBack(dist):
    dist_1=dist/256
    dist_0=dist%256
    b=[8,dist_1,dist_0,135,1]
    spi.xfer(b)
    print(b)
    run=True
    n=0
    if(dist<40):cp=5
    else: cp=dist/10
    while(run):
        n+=1
        run=not getFeedback()
        if(n==cp):
            clear()
            goBack(dist)
        time.sleep(0.1)
    print('End of Command')

def magPosition(angle):
    for n in range(5):
        magPos(angle)

def magPos(angle):
    pwm=135
    an1=angle/256
    an0=angle%256
    b=[16,an1,an0,pwm,1]
    spi.xfer(b)
    print(b)
    run=True
    n=0
    if(angle<10):cp=3
    else: cp=angle/5
    while(run):
        n+=1
        run=not getFeedback()
        if(n==cp):
            clear()
            magPos(angle)
        time.sleep(0.1)
    print('End of Command')


def clearPosition():
    spi.xfer([22,0,0,0,0])


def stopCompass():
    a=[24,0,0,0,0]
    f=spi.xfer(a)
    print(a)


def gripPosition(angle):
    #clear()
    pwm=120
    an1=angle/256
    an0=angle%256
    a=[10,an1,an0,pwm,1]
    spi.xfer(a)
    print(a)

def camPosition(angle):
    #clear()
    pwm=120
    an1=angle/256
    an0=angle%256
    a=[12,an1,an0,pwm,1]
    #f=spi.readbytes(1)
    spi.xfer(a)
    print(a)


def jointPosition(angle):
    pwm=120
    an1=angle/256
    an0=angle%256
    a=[14,an1,an0,pwm,1]
    spi.xfer(a)
    print(a)
    run=True
    n=0
    while(run):
        n+=1
        run=not getFeedback()
        if(n==40):
            clear()
            jointPosition(angle)
        time.sleep(0.1)
    print('End of Command')


def readCompass():
    spi.xfer([18])
    time.sleep(0.1)
    spi.readbytes(1)
    f=spi.readbytes(1)
    MSB=f[0]
    print(MSB)
    f=spi.readbytes(1)
    spi.readbytes(1)
    LSB=f[0]
    print(LSB)
    r=(MSB<<8)+LSB;
    print(str(r))
    return r

def getFeedback():
    b1=spi.readbytes(1)[0]
    print(b1)
    if(b1==255):return True
    else: return False

#========================== camera functions =================
'''
cam = None
qr = None
fc = None

def startCamera():
    co=simcv.ObjectRead()
    #global cam
    qr=simcv.QR()
    fc=simcv.Face()
    cam = co.startCamera()

def stopCamera():
    del cam
    del qr
    del fc

def QRxy():
    #global qr
    return qr.getXY(display=False)

def getfaceXY():
    #global fc
    return fc.getXY(display=False)

'''
#========================== client side========================

#--------------------------------------------------------------

qr = simcv.QR(display=False)
camera = qr.startCamera(width=640,height=480) # width=1280,height=960) 
fc = simcv.Face(display=False)
fc.cam = camera

'''
while True:
    #print('start')
    time.sleep(0.01)
    dat=scratchSock.recv(1024)
    if not dat: break
    cmm=dat.split(' "')[1].split("'")
    #print(dat)
    if(len(cmm)>1):
        dist=int(float(cmm[0]))
        com=cmm[1]
        name=cmm[2].split('"')[0]
#        print(com)
        print('distance='+str(dist) +'-and command-'+com)

        if(com=='straight'):
            goStraight(dist)
            print("str")           
            #time.sleep(dist/100)           
        if(com=='back'):
            goBack(dist)
            print("back"+str(dist))           
            #time.sleep(dist/100)
        elif(com=='left'):
            magPosition(int(dist))
            print("left")
            #time.sleep(1)
        elif(com=='right'):
            magPosition(int(dist))
            print("right")
            #time.sleep(1)
        elif(com=='clearposit'):
            clearPosition()
            print('clear mag position')
            time.sleep(0.5)
        elif(com=='reset'):
            clear()
            print("clear")
            time.sleep(0.1)
        elif(com=='stopcompass'):
            stopCompass()
            print("stop comapss")
        elif(com=='readcompass'):
            sendScratchCommand('sensor-update "compass" '+str(readCompass()))
            #readCompass()
            #sendValue("GetComapass",str(readCompass()))
            print("send compass value")
            time.sleep(0.01)
        elif(com=='getqrxy'):
            xy = qr.getXY()
            if(xy): 
                print(xy) #------------------------
                sendScratchCommand('sensor-update "QRx" '+str(xy[0].x))
                sendScratchCommand('sensor-update "QRy" '+str(xy[0].y))
            else:
                sendScratchCommand('sensor-update "QRx" '+str(None))
                sendScratchCommand('sensor-update "QRy" '+str(None))
        elif(com=='getqrdist'):
            qrd=qr.getXY()
            if(qrd): 
                dist = 44800/qrd[0].width()
                print(dist) #----------------------
                sendScratchCommand('sensor-update "QRdist" '+str(dist))
            else:
                sendScratchCommand('sensor-update "QRdist" '+str(None))
        elif(com=='getfacexy'):
            xy=fc.getXY()
            if(xy): 
                print(xy)
                sendScratchCommand('sensor-update "faceX" '+str(xy[0]))
                sendScratchCommand('sensor-update "faceY" '+str(xy[1]))
        elif(com=='saveface'):
            saved=fc.saveFace(name)
            sendScratchCommand('sensor-update "faceSaved" '+str(saved))
            print(saved)
        elif(com=='recognise'):
            keypoints=fc.recognise(name)
            sendScratchCommand('sensor-update "faceRecognition" '+str(keypoints))
            print(keypoints) 
        elif(com=='camposition'):
            camPosition(dist)
            print('camposition')
            time.sleep(0.01)
        elif(com=='gripper'):
            gripPosition(dist)
            print('gripper')
            time.sleep(0.01)
        elif(com=='joint'):
            jointPosition(dist)
            print('joint')
            time.sleep(0.01)
        elif(com=='speak'):
            os.system("espeak -v ka '" + name+ "'")
            #os.system("espeak -v ka --stdout '"+name+ "' | aplay -D hw:1,0")
            
'''
#===============================================================


'''clear()
while(1):
    magPosition(0)
    time.sleep(3)
    magPosition(90)
    time.sleep(3)
    magPosition(180)
    time.sleep(3)
    magPosition(270)
    time.sleep(3)
    magPosition(360)
    time.sleep(3)
    magPosition(270)
    time.sleep(3)
    magPosition(180)
    time.sleep(3)
    magPosition(90)
    time.sleep(3)
    magPosition(0)
#    clear()
'''


'''
#QR read
qr=simcv.QR(display=True)
qr.startCamera() #width=1280,height=960)

while(1):
    xy =qr.getXY()
    if(xy): print(xy)
    time.sleep(1)
'''
'''
#save face
fc=simcv.Face(display=False)
fc.startCamera(width=320,height=240)

while(1):
    xy=fc.getXY()
    if(xy): print(xy)
    time.sleep(1)

'''
''' 
#recognise
fc=simcv.Face(display=False)
fc.startCamera(width=640,height=480)

while(1):
    #keypoints=fc.saveFace("irakli")
    keypoints=fc.recognise('irakli')
    print(keypoints)
    time.sleep(1)
'''
