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


def colorTest(strip,frames, colorOne, delay,colorTwo):

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
        colorExit(0)  
        
        
    print(GETdata)

#Loop through every LED setting it to Color1 update display
def colorSolid(strip):    
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
   


#Loop through every LED set to Color1, update display
#Loop through every LED set to Color2, update display 
def colorFlash(strip,frames, colorOne, delay, colorTwo):
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
          
            
            
#Loop over 65 - 90, for each loop color each LED per the Switch/Elif statement, display per x value
    #LED <= (rand +5) - abs(x-NUM) AND LED <= (rand -5) - abs(x-NUM)
    #Random Number determines position on Light Strip = +/-5
    #NUM determines when the Position will activate
    #Color One is the pulse Color
    #Color Pulse is the background Color
def colorPulse(strip,frames, colorOne, delay, colorTwo):
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
       
       


#https://agromonitoring.com/api/current-weather
def APIgetWeather(param1,param2,location):
    URL = "https://api.openweathermap.org/data/2.5/weather"
    apikey = ""
    payload = {'q':location,'appid':apikey}
    time.sleep(15) #only allow 1 request per second

    GETdata = requests.get(url = URL, params = payload)
    # if GETdata.status_code == 200:
        # print json.loads(GETdata.content.decode('utf-8'))
    GETdata = GETdata.json()
    
    print(GETdata)
    if param1 == "weather":
        return(GETdata[param1][0][param2])
    else:
        return(GETdata[param1][param2])
        
def colorWeather(strip):
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
        colorExit(0)  
   
# sunrise,sunset | solar_noon | day_length | civil_twilight_begin | civil_twilight_end | nautical_twilight_begin
# nautical_twilight_end | astronomical_twilight_begin | astronomical_twilight_end
def APIgetTime(param): 
#?lat=&lng=
    payload = {'lat':"36.7201600",'lng':"-4.4203400"}
    #automate location access (google api?/ ask browser?)
    URL = "https://api.sunrise-sunset.org/json"
    
    GETdata = requests.get(url = URL,params = payload) 
    GETdata = GETdata.json() 
    print(GETdata)
    
    if param == "solar_noon":
        noon = GETdata['results'][param]  
        (hr, min, sec) = noon.split(':')
        print(hr, min, sec)
        timeNoon = (int(hr) * 3600) + (int(min) * 60)
        print(sec.find('AM') == -1)
        if sec.find('AM') == -1:
            timeNoon = timeNoon + int(sec[0:1])
        else:
            timeNoon = timeNoon + (int(sec[0:1]) + 43200)
        return timeNoon
    #add more if statements for other access values   
    
def colorTime(strip):
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
        colorExit(0)  

   
def colorExit(option):
    
    if option == 0:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))                  
        strip.show()
    if option == 1:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))                  
            strip.show()
            time.sleep(.01)
   

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
                colorPulse(strip,frames, Color(LGreen, LRed, LBlue),Ldelay,Color(LEGreen, LERed,LEBlue ))  # Green wipe
            elif(Lmode == "solid"):
                colorSolid(strip)
            elif (Lmode == "weather"):
                colorWeather(strip)
            elif(Lmode == "flash"):
                colorFlash(strip,frames, Color(LGreen, LRed, LBlue),Ldelay,Color(LEGreen, LERed,LEBlue ))
            elif(Lmode == "test"):
                colorTest(strip,frames, Color(LGreen, LRed, LBlue),Ldelay,Color(LEGreen, LERed,LEBlue ))
            elif(Lmode == "time"):
                colorTime(strip)

    except KeyboardInterrupt:
        print("exit program")
        colorExit(0)   
        os._exit(0)
        
