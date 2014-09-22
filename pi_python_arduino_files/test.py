import time
from robkit3 import *



while(1):
    goStraight(100)
    time.sleep(1)
    goBack(100)
    time.sleep(1)
    magPosition(180)
    time.sleep(1)
    clearPosition()
    time.sleep(1)
    goStraight(100)
    time.sleep(1)
    gripPosition(0)
    time.sleep(1)
    jointPosition(180)
    time.sleep(1)
    goStraight(100)
    time.sleep(1)
    jointPosition(0)
    time.sleep(1)
    gripPosition(180)
    time.sleep(1)
