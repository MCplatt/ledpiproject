from neopixel import *
import time
from datetime import datetime
import argparse
import random
import math
import array
import numpy
import sys
import os
import requests
import json
from picamera import PiCamera


def hex_to_rgb(value):
    value = value.lstrip('0x')
    value = value.zfill(6)
    
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

def colorChangeFun(LEDColorOne,LEDColorTwo,Frame,CurrFrame):
    LightMedian = (LEDColorOne + LEDColorTwo)/2
    LightDif = LEDColorOne - LEDColorTwo
    HalfFrame = Frame/2
    if HalfFrame <= 0:
        HalfFrame = 1
        
    if Frame <= 1:
        return LEDColorTwo
    else:
        #print(int(  LightMedian + ((LightDif/2)  * (float(HalfFrame - CurrFrame)/HalfFrame))  ))
        return abs(int(  LightMedian + ((LightDif/2)  * (float(HalfFrame - CurrFrame)/HalfFrame))  ))

def colorChange(strip, stripNext, Frames, delay, mod = 0):
#mod = mofifier, starts the loop further in the colorchange loop, default = 0   
    stripTemp = []
    for j in range(strip.numPixels()):
        stripTemp.append(strip.getPixelColor(j))
    
    #DEBUG BLOCK===============
    # print("mod = ", mod)
    # print(Frames)
    #DEBUG BLOCK===============
    
    for i in range(mod,Frames):
        for n in range(strip.numPixels()):
            colorOneRBG = hex_to_rgb(hex(stripTemp[n]))
            colorTwoRBG = hex_to_rgb(hex(stripNext[n]))
            
            Tgreen = colorChangeFun(colorOneRBG[0],colorTwoRBG[0], Frames, i)
            Tred = colorChangeFun(colorOneRBG[1],colorTwoRBG[1], Frames, i)
            Tblue = colorChangeFun(colorOneRBG[2],colorTwoRBG[2], Frames, i)
            
            strip.setPixelColor(n,Color(Tgreen,Tred,Tblue))
            
            
        #DEBUG BLOCK===============
        # print("")
        # print("FRAME",i)
        # print("Green","Red","Blue")
        # print(colorOneRBG)
        # print(Tgreen,Tred,Tblue)
        # print(colorTwoRBG)
        # print("")     
        #DEBUG BLOCK===============
        
        strip.show()
        time.sleep(delay)

