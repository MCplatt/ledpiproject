from neopixel import *
import time
from datetime import datetime
import argparse
import random
import math
import array
import numpy
from picamera import PiCamera
from PIL import Image

def picturetoTemplate(DispStart,DispEnd, strip,Pic): #TODO add multiple displays

    DispTotal = DispEnd - DispStart
    PicMid = 5 #rotate image so chevron design falls down frame
        
    im = Image.open("./LED_assets/" + Pic)
    stdHeight = int((float(DispTotal)/im.width) * im.height) #shrink height as a proportion of the width
    im = im.resize((DispTotal,stdHeight)) #width must be the size of the display
    
    BGim = Image.open("./LED_assets/background_template.png")

    BGim = BGim.resize((strip.numPixels(),stdHeight)) #Change height to match amount of frames in image/animation
    
    
    # print(DispEnd,DispTotal,PicMid)
    print("stdHeight",stdHeight)
    print("im: ",im.height,im.width)
    print("BGim: ",BGim.height,BGim.width)
    
    for j in range(stdHeight-1,-1,-1): #loop through image from bottom to top, 
        print("---------Frame: " + str(j))
        for i in range(DispTotal):
            if (i <= PicMid): #move image pixel and put pixel in the background image
                #DEBUG BLOCK===============
                print(DispStart + (i + (DispTotal - PicMid)),j,im.getpixel((i,j)))
                print("UNDER MID")
                #DEBUG BLOCK===============
                BGim.putpixel( ((DispStart + (i + (DispTotal - PicMid))), j), im.getpixel((i,j)) ) 
               
            else:    
                BGim.putpixel( ((DispStart + (i - PicMid)), j), im.getpixel((i,j)) ) 
                #DEBUG BLOCK===============
                # print((DispStart + (i - PicMid)),j,im.getpixel((i,j)))
                # print("OVER MID")
                #DEBUG BLOCK===============
    
    return BGim

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

def colorChange(strip, stripNext, Frames, delay, Start = 0, mod = 0):
# Start = new Starting point, starts the loop further in the colorchange loop, default = 0 
# mod = return a vector of what the output instead of changing color  
    stripTemp = []
    for j in range(strip.numPixels()):
        stripTemp.append(strip.getPixelColor(j))
    
    #DEBUG BLOCK===============
    # print("mod = ", mod)
    # print(Frames)
    #DEBUG BLOCK===============
    
    for i in range(Start,Frames):
        for n in range(strip.numPixels()):
            colorOneRBG = hex_to_rgb(hex(stripTemp[n]))
            colorTwoRBG = hex_to_rgb(hex(stripNext[n]))
            
            Tgreen = colorChangeFun(colorOneRBG[0],colorTwoRBG[0], Frames, i)
            Tred = colorChangeFun(colorOneRBG[1],colorTwoRBG[1], Frames, i)
            Tblue = colorChangeFun(colorOneRBG[2],colorTwoRBG[2], Frames, i)
        
            if (mod == 1):
                stripTemp[n] = Color(Tgreen,Tred,Tblue)
            else:
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
        if (mod == 1):
            return stripTemp
        else:
            strip.show()
            time.sleep(delay)