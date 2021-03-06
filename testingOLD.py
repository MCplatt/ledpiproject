#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
import random
import math
import numpy
import sys
import os
# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

LRed = 0
LBlue = 0
LGreen = 0

def colorSolid(strip,color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
        

def ColorWipeFunc(var):
    return 150 - var
# Define functions which animate LEDs in various ways.

def colorPulse(strip, colorOne, delay, colorTwo):



    randvarOne = random.randint(20,25)
    randvarTwo = random.randint(32,63)
    randvarThree = random.randint(70,100)
    randvarFour = random.randint( 107 , 115)
    colorthree = Color(40,100,0)
 
    
    halfWidth = 7
    
    for x in range(65,90):
    
        
        print("Frame: ", x)
        
        print(" ")
       #print(100 + 50*sine, 50 + 50*sine) 
        for i in range(strip.numPixels()):
           # if((x-25) <= 115 and x > 0):
            if(i  <= (randvarOne + 5) - abs(x-80) and i >= (randvarOne-5) + abs(x - 80)):
                strip.setPixelColor(i, colorTwo)
                print("1")
            elif(i  <= (randvarTwo+5) - abs(x-70) and i >= (randvarTwo-5)+ abs(x - 70)):
                strip.setPixelColor(i, colorTwo)
                print("2")
            elif(i  <= (randvarThree+5) - abs(x-75) and i >= (randvarThree-5) + abs(x - 75)):
                strip.setPixelColor(i, colorTwo)
                print("3")
            elif(i  <= (randvarFour+5) - abs(x-85) and i >= (randvarFour-5) + abs(x - 85)):
                strip.setPixelColor(i, colorTwo)
                print("4")
            else:
                strip.setPixelColor(i, colorOne)
            
        time.sleep(delay)
        strip.show()

def fun(x):
    return float((25/8)*numpy.cos((x+37)*math.pi/24))



 
def colorTest(strip, color, delay):

    colorone = Color(240,50,10)
    colorTwo = Color(250,50,10)
    colorthree = Color(150,150,150)
   
   
    
    for x in range(1,150):
        func = int(75 + 75*numpy.sin((x+37)*math.pi/24))
        # var = Symbol('var')
        # funcprime = int(76 + 74*numpy.sin(var*math.pi/24))
        # xprime = funcprime.diff(var)
        funcNext = int(76 + 74*numpy.sin((x+38)*math.pi/24))
        xprime = abs(fun(x))
        # if(xprime == 0):
            # xprime == 1
        print("x: ", x)
        print("f(x) = ", func)
        print("f(x+1) = ", funcNext)
        print("Delay * xprime ", xprime)
       #print(100 + 50*sine, 50 + 50*sine) 
        # for i in range(strip.numPixels() - 1):
           # # if((x-25) <= 115 and x > 0):
            # if(x == func or x == func+1):
                # strip.setPixelColor(i, colorTwo)
                # #print("True")
    
            # else:
                # strip.setPixelColor(i, colorone)
            
        # time.sleep(delay)
        # strip.show()
        
    
        for ix in range( func, funcNext-1):
            for i in range(strip.numPixels()):
                   # if((x-25) <= 115 and x > 0):    
                if(i >= ix-5 and i <= ix+5):
                    strip.setPixelColor(i, colorthree)
                else:
                    strip.setPixelColor(i, colorone)
            print(1/ (delay*xprime))
            time.sleep(1/ (delay*xprime))
            strip.show()
                

        
# Main program logic follows:
if __name__ == '__main__':

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    print("Color Background")
    LRed = input("Red: ")
    LBlue = input("Blue: ")
    LGreen = input("Green: ") 
    print(" ")
    print("Color Main")
    LERed = input("Red: ")
    LEBlue = input("Blue: ")
    LEGreen = input("Green: ")     

    
    try:
       # Loption = input("display(pulse,solid):")
        while True: 
            #if (Loption == "pulse"):
            colorPulse(strip, Color(LGreen, LRed, LBlue),.2,Color(LEGreen, LERed, LEBlue))  # Green wipe
      #      colorWipe(strip, Color(0,0,0),1)
          #  if (Loption == "solid"):
           #     colorSolid(strip,Color(LGreen,LRed,LBlue))

    except KeyboardInterrupt:
        print("exit")
        try:
            sys.exit(0)
        except SystemExit:
            colorSolid(strip, Color(0,0,0))
            os._exit(0)
        
