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
import LED_low_level

#Loop over 65 - 90, for each loop color each LED per the Switch/Elif statement, display per x value
    #LED <= (rand +5) - abs(x-NUM) AND LED <= (rand -5) - abs(x-NUM)
    #Random Number determines position on Light Strip = +/-5
    #NUM determines when the Position will activate
    #Color One is the pulse Color
    #Color Pulse is the background Color
def animPulse(strip,frames, colorOne, delay, colorTwo):
    randvarOne = random.randint(85,100)
    randvarTwo = random.randint(105,115)
    randvarThree = random.randint(120,130)
    randvarFour = random.randint( 135,145)
    stripNextPulse = [0] * 150

    for j in range(strip.numPixels()):   #initialise the strip once because its an ANIMATION
        if(j<82):
            strip.setPixelColor(j,Color(0,0,0))
        else:    
            strip.setPixelColor(j,colorTwo)
            
        
    try:    
        while True:
            for x in range(0,25):
            
                #DEBUG BLOCK===============
                print("Frame: ", x)
                print(" ")
                #DEBUG BLOCK===============
                
                for i in range(strip.numPixels()):
            
                    if(i<82):
                        stripNextPulse[i] = Color(0,0,0) 
                    elif(i  <= (randvarOne+5) - abs(x-5) and i >= (randvarOne-5)+ abs(x - 5)):
                        stripNextPulse[i] = colorOne
                        #print(i)
                        print("20-25")
                    elif(i  <= (randvarTwo+5) - abs(x-15) and i >= (randvarTwo-5) + abs(x - 15)):
                        stripNextPulse[i] = colorOne
                        #print(i)
                        print("32-63")
                    elif(i  <= (randvarThree+5) - abs(x-10) and i >= (randvarThree-5) + abs(x - 10)):
                        stripNextPulse[i] = colorOne
                        #print(i)
                        print("70-100")
                    elif(i  <= (randvarFour+5) - abs(x-20) and i >= (randvarFour-5) + abs(x - 20)):
                        stripNextPulse[i] = colorOne
                        #print(i)
                        print("107-115")
                    else:
                        stripNextPulse[i] = colorTwo

                colorChange(strip,stripNextPulse, frames,delay)
    except KeyboardInterrupt:
        print("exit pulse")
        colorExit(1)  
        
#Loop through every LED set to Color1, update display
#Loop through every LED set to Color2, update display 
def animFlash(strip,frames, colorOne, delay, colorTwo):
    stripNextFlash = [0] * 150

    for j in range(strip.numPixels()):   #initialise the strip once because its an ANIMATION
        if(j<82):
            strip.setPixelColor(j,Color(0,0,0))
        else:    
            strip.setPixelColor(j,colorTwo)
    
    try:
        while True:
            for i in range(strip.numPixels()):
                if(i<82):
                    stripNextFlash[i] = Color(0,0,0)
                else:  
                    stripNextFlash[i] = colorOne
            colorChange(strip,stripNextFlash, frames,delay)

            for i in range(strip.numPixels()):
                if(i<82):
                    stripNextFlash[i] = Color(0,0,0)
                else:  
                    stripNextFlash[i] = colorTwo
            colorChange(strip,stripNextFlash, frames,delay)
            
    except KeyboardInterrupt:
        print("exit flash")
        colorExit(1)  

#Loop through every LED setting it to Color1 update display
def animSolid(strip):    
    try:
        while True:
            print("choose color: \n")
            LRed = input("Red: ")
            LBlue = input("Blue: ")
            LGreen = input("Green: ") 
            
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(LGreen,LRed,LBlue))                  
            strip.show()

        
    except KeyboardInterrupt:
        print("exit solid")
        colorExit(1)  

def animExit(option):
    
    if option == 0:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))                  
        strip.show()
    if option == 1:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))                  
            strip.show()
            time.sleep(.01)   
 