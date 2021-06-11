from neopixel import *
import time
from datetime import datetime
import argparse
import random
import math
import array
from PIL import Image
import numpy
import json
from picamera import PiCamera
from LED_low_level import *
import os

 
def pictureToAnim(strip,dispStart,dispEnd,picture,frames,delay,mod = 0): #USE OPTIONAL PARAMTERS TO MAKE TIMED ANIMATION OPTIONAL
#Mod = return Picture in list form, each elemnt is (g,r,b) form
    pictureMod = picture[:(picture.find('.'))] + "MOD" + picture[picture.find('.'):]
    
    print(os.listdir("./LED_assets/"))
    
    if((pictureMod) in os.listdir("./LED_assets/")):
        im = Image.open("./LED_assets/" + pictureMod)
    else:
        im = picturetoTemplate(dispStart,dispEnd,strip,picture) #81 to 148 is the current frame size this adjusts with different frame size and length
        im.save("./LED_assets/" + pictureMod)


    pixels = list(im.getdata())
    print(len(pixels))
    if(mod == 1):
        return pixels

    stripNextPic = [0] * strip.numPixels()
    
    try:
        while True:
            #print("Height: " + str(im.height) + "Width: " + str(im.width))
            #print(im.size)
            for j in range(im.height):
                print("Frame: " + str(j))
                for i in range(im.width):
                    x = (strip.numPixels() * j) + i
                    #print(x)
                    stripNextPic[i] =  Color(pixels[x][1],pixels[x][0],pixels[x][2])
                
                colorChange(strip,stripNextPic, frames,delay)
            
    except KeyboardInterrupt:
        print("exit pic")
        animExit(1,strip)  

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

    for j in range(strip.numPixels()): #initialise the strip once because its an ANIMATION
        if(j<82):
            strip.setPixelColor(j,Color(0,0,0))
        else:    
            strip.setPixelColor(j,colorTwo)
            
        
    try:    
        while True:
            for x in range(0,25):
            
                #DEBUG BLOCK===============
                # print("Frame: ", x)
                # print(" ")
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
        animExit(1,strip)  
        
#Loop through every LED set to Color1, update display
#Loop through every LED set to Color2, update display 
def animFlash(strip, dispStart, dispEnd, frames, colorOne, delay, colorTwo):
    stripNextFlash = [0] * strip.numPixels()

    for j in range(strip.numPixels()):   #initialise the strip once because its an ANIMATION
        if(j<dispStart or j>dispEnd):
            strip.setPixelColor(j,Color(0,0,0))
        else:    
            strip.setPixelColor(j,colorTwo)
    
    try:
        while True:
            for i in range(strip.numPixels()):
                if(j<dispStart and j>dispEnd):
                    stripNextFlash[i] = Color(0,0,0)
                else:  
                    stripNextFlash[i] = colorOne
            colorChange(strip,stripNextFlash, frames,delay)

            for i in range(strip.numPixels()):
                if(j<dispStart and j>dispEnd):
                    stripNextFlash[i] = Color(0,0,0)
                else:  
                    stripNextFlash[i] = colorTwo
            colorChange(strip,stripNextFlash, frames,delay)
            
    except KeyboardInterrupt:
        print("exit flash")
        animExit(1,strip)  

#Loop through every LED setting it to Color1 update display
def animSolid(strip,color,dispStart,dispEnd,mod = 0):  #MOD is the amount of delay till exiting the loop
    try:
        print(strip,color,dispStart,dispEnd,mod)
        while True:
            for i in range(strip.numPixels()): 
                if(i > dispStart and i < dispEnd): #TODO add dynamic pixel start
                    strip.setPixelColor(i, color)
                else:  
                    strip.setPixelColor(i, Color(0,0,0))
                                  
            strip.show()
            if mod > 0:
                time.sleep(mod)
                break
        
    except KeyboardInterrupt:
        print("exit solid")
        animExit(1,strip)  

def animExit(option,strip):
    if option == 0: #blank off, no anim
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))                  
        strip.show()
    if option == 1: #anim off one-by-one
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))                  
            strip.show()
            time.sleep(.01)   
 