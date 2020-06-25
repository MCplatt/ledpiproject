#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Coleman Platt
#


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
from LED_animations import *
from LED_low_level import *
from LED_api_calls import *

# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

LRed = 0
LBlue = 0
LGreen = 0


def modeTest(strip,frames, colorOne, delay,colorTwo):

    try:
        while True:
            h = 640 # change this to anything < 2592 (anything over 2000 will likely get a memory error when plotting
            cam_res = (int(h),int(0.75*h)) # keeping the natural 3/4 resolution of the camera
            cam_res = (int(16*numpy.floor(cam_res[1]/16)),int(32*numpy.floor(cam_res[0]/32)))
            print("cam_res", cam_res)
            cam = PiCamera()
            ## making sure the picamera doesn't change white balance or exposure
            ## this will help create consistent images
            cam.resolution = (cam_res[1],cam_res[0])
            cam.framerate = 30
            time.sleep(2) #let the camera settle
            cam.iso = 100
            cam.shutter_speed = cam.exposure_speed
            cam.exposure_mode = 'off'
            gain_set = cam.awb_gains
            cam.awb_mode = 'off'
            cam.awb_gains = gain_set
            # prepping for analysis and recording background noise
            # the objects should be removed while background noise is calibrated
            data = numpy.empty((cam_res[0] * cam_res[1]*3),dtype=numpy.uint8)
            noise = numpy.empty((cam_res[0] * cam_res[1]*3),dtype=numpy.uint8)
            #x,y = numpy.meshgrid(numpy.arange(numpy.shape(data)[1]),numpy.arange(0,numpy.shape(data)[0]))
            rgb_text = ['Red','Green','Blue'] # array for naming color
            # input("press enter to capture background noise (remove colors)")
            cam.capture(noise,format ='rgb')
            noise = noise-numpy.mean(noise) # background 'noise'
            # looping with different images to determine instantaneous colors
            while True:
                try:
                    print('===========================')
                    #input("press enter to capture image")
                    cam.capture(data,'rgb')
                    print("data" , data)
                    
                    mean_array,std_array = [],[]
                    for i in range(0,3):
                        # calculate mean and STDev and print out for each color
                        print(data[i], numpy.mean(data) ,numpy.mean(noise[i]))
                        time.sleep(1)
                        mean_array.append(numpy.mean(data[i]-numpy.mean(data)-numpy.mean(noise[i])))
                        std_array.append(numpy.std(data[i]-numpy.mean(data)-numpy.mean(noise[i])))
                        print('-------------------------')
                        print(rgb_text[i]+'---mean: {0:2.1f}, stdev: {1:2.1f}'.format(mean_array[i],std_array[i]))
                    # guess the color of the object
                    print('--------------------------')
                    print('The Object is: {}'.format(rgb_text[numpy.argmax(mean_array)]))
                    print('--------------------------')
                except KeyboardInterrupt:
                    break
            
            
    except KeyboardInterrupt:
        print("exit weather")
        animExit(0)  
        
        
    print(GETdata)
          
            
        
def modeWeather(strip):
    stripNextWeather = [0] * 150
    primary = "weather" #raw_input("param1: ")
    secondary = "icon" #raw_input("param2: ")
    loc = "Louisville" # raw_input("Location: ")
    frames = 255
    delay = .0001


    for j in range(strip.numPixels()):   #initialise the strip once because its an ANIMATION
            strip.setPixelColor(j,Color(0,0,0))
    
    try:
        while True:
            weather = APIgetWeather(primary,secondary,loc)
            print("weather icon code", weather[0:2])
            if weather[0:2] == "01": # Clear Sky-----------------------------
                for i in range(strip.numPixels()):
                    if(i<82):
                        stripNextWeather[i] = Color(0,0,0)
                    else:  
                        stripNextWeather[i] = Color(245,245,255)
                colorChange(strip,stripNextWeather, frames,delay)
            elif weather[0:2] == "02":  #Few Clouds--------------------------
                for i in range(strip.numPixels()):
                    if(i<82):
                        stripNextWeather[i] = Color(0,0,0)
                    else:  
                        stripNextWeather[i] = Color(225,245,245)
                colorChange(strip,stripNextWeather, frames,delay)            
            elif weather[0:2] == "03": #scattered clouds---------------------
                for i in range(strip.numPixels()):
                    if(i<82):
                        stripNextWeather[i] = Color(0,0,0)
                    else:  
                        stripNextWeather[i] = Color(100,150,150)
                colorChange(strip,stripNextWeather, frames,delay)            
            elif weather[0:2] == "04": # broken Clouds---------------------------
                for i in range(strip.numPixels()):
                    if(i<82):
                        stripNextWeather[i] = Color(0,0,0)
                    else:  
                        stripNextWeather[i] = Color(100,100,150)
                colorChange(strip,stripNextWeather, frames,delay)            
            elif weather[0:2] == "09": #shower rain---------------------------
                for i in range(strip.numPixels()):
                    if(i<82):
                        stripNextWeather[i] = Color(0,0,0)
                    else:  
                        stripNextWeather[i] = Color(50,0,255)
                colorChange(strip,stripNextWeather, frames,delay)            
            elif weather[0:2] == "10":#rain-----------------------------------
                for i in range(strip.numPixels()):
                    if(i<82):
                        stripNextWeather[i] = Color(0,0,0)
                    else:  
                        stripNextWeather[i] = Color(0,0,200)
                colorChange(strip,stripNextWeather, frames,delay)            
            elif weather[0:2] == "11": #thunder storm--------------------------
                for i in range(strip.numPixels()):
                    if(i<82):
                        stripNextWeather[i] = Color(0,0,0)
                    else:  
                        stripNextWeather[i] = Color(0,150,225)
                colorChange(strip,stripNextWeather, frames,delay)            
            elif weather[0:2] == "13": #snow --------------------------------
                for i in range(strip.numPixels()):
                    if(i<82):
                        stripNextWeather[i] = Color(0,0,0)
                    else:  
                        stripNextWeather[i] = Color(245,245,255)
                colorChange(strip,stripNextWeather, frames,delay)            
            elif weather[0:2] == "50": #mist----------------------------------
                for i in range(strip.numPixels()):
                    if(i<82):
                        stripNextWeather[i] = Color(0,0,0)
                    else:  
                        stripNextWeather[i] = Color(100,100,100)
                colorChange(strip,stripNextWeather, frames,delay)        
        
        
    except KeyboardInterrupt:
        print("exit weather")
        animExit(0)  
   
    
def modeTime(strip):
    delay = 1
    colorDay = Color(200,200,255)#GRB
    colorNight = Color(100,100,1)
    stripNextTime = [0] * 150

    try:
        while True:
            now = datetime.now()
            timeCurr = (now.hour *3600) + (now.minute * 60) + now.second  #Decimal time in seconds
            timeDay = APIgetTime("solar_noon") 
            timeNight = (timeDay + 43200) % 86400
            print(timeDay,timeNight)
            print(timeCurr)
            if((timeCurr >= timeNight) and (timeCurr < timeDay)):
                print("Night -> Day-----------------------------------")    
                for i in range(strip.numPixels()):
                    if(i < 82): 
                        strip.setPixelColor(i, Color(0,0,0))                #Initialise strip because NULL = 0
                        stripNextTime[i] = Color(0,0,0)       #MUST INIT STRIP MID LOOP BECAUSE ENTRENCE POINT IS VARIABLE
                    else:
                        strip.setPixelColor(i, colorNight)                    #Initialise strip because NULL = 0
                        stripNextTime[i] = colorDay        #INIT Copy strip to temp array
                
                timeCurrAdj = timeCurr - timeNight  # Find how many frames into the cycle the time is and start the color change timeCurrAdj man frames in
                
                colorChange(strip,stripNextTime, abs(timeDay - timeNight) ,delay,timeCurrAdj)

            elif((timeCurr < timeNight) or (timeCurr >= timeDay)):
                print("Day -> Night-----------------------------------")
                for i in range(strip.numPixels()):           #make next frame 
                    if(i < 82):
                        strip.setPixelColor(i, Color(0,0,0))
                        stripNextTime[i] = Color(0,0,0)
                    else:
                        strip.setPixelColor(i, colorDay)
                        stripNextTime[i] = colorNight
                        
                if (timeCurr >= timeDay): # Find how many frames into the cycle the time is and start the color change timeCurrAdj man frames in
                    timeCurrAdj = timeCurr - timeDay
                elif(timeCurr <= timeNight):
                    timeCurrAdj = timeCurr + (86400 - timeDay)
                    
                colorChange(strip,stripNextTime, (timeNight + (86400 - timeDay)) ,delay, timeCurrAdj)

    except KeyboardInterrupt:
        print("exit Time")
        animExit(0)  

   

if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)    # Create NeoPixel object with appropriate configuration.
    strip.begin()    # Intialize the library (must be called once before other functions).

    method = raw_input("Color choice(manual / auto):")
    
    if(method == "manual"):
        print("Color Main")
        LRed = input("Red: ")
        LBlue = input("Blue: ")
        LGreen = input("Green: ") 
        print("Color Secondary")
        LERed = input("Red: ")
        LEBlue = input("Blue: ")
        LEGreen = input("Green: ")
        
    elif(method == "auto"):
        print("Color Main/Day")
        LGreen = 255
        LRed = 40
        LBlue = 25
        print("Color Secondary/Night")
        LEGreen = 75
        LERed = 255
        LEBlue = 20

    print("Main Color code:", hex(Color(LGreen, LRed, LBlue)))
    print("Secondary Color code:", hex(Color(LEGreen, LERed, LEBlue)))    
    print("-----------------------------------------")
    
    Lmode = ""
    try:
        while Lmode != "quit":  #=============MENU LOOP==============
        
            print("")
            Lmode = raw_input("   -=-=-=-=-=| MAIN MENU |=-=-=-=-=- \n'Flash' - Alternate between two colors \n'Pulse' - Secondary Color is shown with Main color appearing/dissappearing \n'Solid' - Main color is displayed \n'Test' - used for prototyping programming structures \n'Time' - Alternates between two colors on a 24hr(86400sec) time frame \n'Weather' - fetch internet weather and display  \n  'Quit' to quit \n - Choose your mode: ")
            Lmode = Lmode.lower()
            Ldelay = input("Delay between Frames (Sec) (.0001 fast - 2 slow):")
            frames = input("Frames: ")
            if (Lmode == "pulse"):
                animPulse(strip,frames, Color(LGreen, LRed, LBlue),Ldelay,Color(LEGreen, LERed,LEBlue ))  # Green wipe
            elif(Lmode == "solid"):
                animSolid(strip)
            elif (Lmode == "weather"):
                modeWeather(strip)
            elif(Lmode == "flash"):
                animFlash(strip,frames, Color(LGreen, LRed, LBlue),Ldelay,Color(LEGreen, LERed,LEBlue ))
            elif(Lmode == "test"):
                modeTest(strip,frames, Color(LGreen, LRed, LBlue),Ldelay,Color(LEGreen, LERed,LEBlue ))
            elif(Lmode == "time"):
                modeTime(strip)

    except KeyboardInterrupt:
        print("exit program")
        animExit(0)   
        os._exit(0)
        
