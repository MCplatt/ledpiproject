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
LED_COUNT      = 300      # Number of LED pixels.
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


def modeCam(strip,heightDisp,widthDisp,dispStart,dispEnd,frames, delay):

    try:
        while True:
            ##Cam Init---------------------------------------------------------------------------
            #h = 640 # change this to anything < 2592 (anything over 2000 will likely get a memory error when plotting
            cam_res = (int(640),int(480)) # keeping the natural 3/4 resolution of the camera
            #cam_res = ( int(16*numpy.floor(cam_res[0]/16)) , int(32*numpy.floor(cam_res[1]/32)) )
            print("cam_res:", cam_res)
            print("disp", widthDisp,heightDisp)



            cam = PiCamera()## CAM INIT----
            cam.resolution = (cam_res[0],cam_res[1])
            cam.framerate = 30
            
            
            time.sleep(2) #let the camera settle

            cam.iso = 100
            cam.shutter_speed = cam.exposure_speed
            cam.exposure_mode = 'off'
            cam.awb_mode = 'off'

            gain_set = cam.awb_gains
            cam.awb_gains = gain_set
            data = numpy.empty((cam_res[0]* cam_res[1]*3),dtype=numpy.uint8)
            # prepping for analysis and recording background noisez
            # the objects should be removed while background noise is calibrated

            # noise = numpy.empty((cam_res[0]* cam_res[1]*3),dtype=numpy.uint8)
            # input("press enter to capture background noise (remove colors)")
            # cam.capture(noise,'rgb')
            # print("noise Multi","Noise array",1- (numpy.mean(noise)/255),noise)
            # noise = noise * (1-(numpy.mean(noise)/255)) # background 'noise'
            # print("noise",noise)
            # x,y = numpy.meshgrid(numpy.arange(numpy.shape(data)[1]),numpy.arange(0,numpy.shape(data)[0]))
            # rgb_text = ['Red','Green','Blue'] # array for naming color

            # displayWidth = dispEnd-dispStart
            
            pixelSize = ((cam_res[0]*cam_res[1])/widthDisp/heightDisp)*3
            camPixel = [0] * pixelSize

            pixelHeight = cam_res[0] / dispHeight
            pixelWidth = cam_res[1] / dispWidth
            # dataWidthAdjust = [0] * heightDispAdjust * widthDispAdjust * 3
            # dataBothAdjust = [0] 
                    

            # stripResHeight = 1 
            # pixelResHeight = 100
            dispPixelMean = [0] * pixelSize
            dispRGB = [0] *3
                         # looping with different successive images to determine instantaneous colors
            dispStripNext = [0] * strip.numPixels()  
            while True:
                try:
                    print('===========================')

                   # raw_input("press enter to capture image")

                    cam.capture('testPic.jpg')
                    cam.capture(data,'rgb')
                    # print("data",data)
                    
                    time.sleep(.1)
                    
                    # raw_input("press enter to capture image")
                    """
                    step = widthDispAdjust / widthDisp 
                    print("Step", step)
                    
                    for itr in range(0,widthDispAdjust * heightDispAdjust*3, (step+2)):
                        for j in range(3):
                            dataWidthAdjust[h] = numpy.mean(data[ itr+j : itr+j+step : 3])
                            h+=1

                            print("itr", itr,"----", dataWidthAdjust[h], numpy.mean(data[ itr+j : itr+j+step : 3]))

                    h = 0
                    step = ((heightDispAdjust / heightDisp)*widthDisp) 
                    for itr in range(0,widthDisp * heightDispAdjust*3):
                        dispStripNext[h] = Color(numpy.mean(data[ itr+1 : itr+1+step : widthDisp]), numpy.mean(data[ itr : itr+step : widthDisp]), numpy.mean(data[ itr+2 : itr+2+step : widthDisp]))
                        h+=1



                        print("itr", itr,"----", dispStripNext[h], numpy.mean(data[ itr+1 : itr+1+step : widthDisp]), numpy.mean(data[ itr : itr+step : widthDisp]), numpy.mean(data[ itr+2 : itr+2+step : widthDisp]))
                        
                        if itr%widthDisp:
                            itr += step - widthDisp

                    # print(dispStripNext)
                    colorChange(strip,dispStripNext, frames,delay)


                    """
                    itr  = 0
                    h = 0
                    for s in range(0,cam_res[0]*cam_res[1]*3,pixelWidth*3):
                        for i in range(3):
                            itrTwo = 0
                            for h in range(0, pixelHeight):
                                #print(data.size)
                                print("===" , s, i,h)
                                #print(s+i+(cam_res[0]*h),(s+i+(cam_res[0]*h) + pixelWidth*3))
                                #print(h)
                                pixStart = (s+i+(cam_res[0]*h))
                                pixEnd = (s+i+(cam_res[0]*h) + pixelWidth)
                                dispPixelMean[itrTwo] = numpy.mean(data[ pixStart : pixEnd : 3])
                                #print("dispPixelMean", dispPixelMean[itrTwo])
                                itrTwo = itrTwo + 1
                            
                            dispRGB[i] = numpy.mean(dispPixelMean)
                        #print("-------------------------------------------------------")
                        #print(dispRGB[0],dispRGB[1],dispRGB[2])
                        #print(itr + dispStart)
                        if(itr + dispStart) < dispEnd:
                           dispStripNext[itr + dispStart] = Color(int(dispRGB[1]),int(dispRGB[0]),int(dispRGB[2]))
                        itr = itr + 1
                    colorChange(strip,dispStripNext, frames,delay)
                    ## mean_array,std_array = [],[]
                    # for i in range(3):

                       # print(i)
                      #  cameraDisplay(strip,camStrip,frames,delay)

                        # print(i)
                        # calculate mean and STDev and print out for each color
                        # print(data, numpy.mean(data) ,numpy.mean(noise))
                        # print('points', data[i::3] ,noise[i::3])
                        # time.sleep(1)
                        # print(data[i::3],"-",numpy.mean(data) , "-", numpy.mean(noise[i::3]))
                        # mean_array.append(numpy.mean(data[i::3]))#-numpy.mean(noise[i::3]
                        # std_array.append(numpy.std(data[i::3]))#-numpy.mean(data)-numpy.mean(noise[i::3]
                        # print(rgb_text[i]+'---mean: {0}, stdev: {1}'.format(mean_array,std_array))
                        # print('-------------------------')
                    # guess the color of the object
                    print('--------------------------')
                except KeyboardInterrupt:
                    break
                    print("exit Cam")
            cam.close()
            break
            
    except KeyboardInterrupt:
        print("exit Cam")
        animExit(1,strip)            
            
        
def modeWeather(strip,dispStart,dispEnd,mod=0):
#mod = Modification, return the picture in list form each element is a color(g,r,b)
    stripNextWeather = [0] * 150
    primary = "weather" #raw_input("param1: ")
    secondary = "icon" #raw_input("param2: ")
    loc = "Louisville" # raw_input("Location: ")
    frames = 255
    delay = .0001
# pictureToAnim(strip,picList[int(animIndex)],frames,Ldelay) #TODO Figure out animation for dynamic 
# animSolid(strip)

    for j in range(strip.numPixels()):   #initialise the strip once because its an ANIMATION
            strip.setPixelColor(j,Color(0,0,0))
    
    weathColor ={
                    "01":animSolid(strip,Color(235,235,255),10,dispStart,dispEnd),# Clear Sky-------------------------
                    "02":pictureToAnim(strip,dispStart,dispEnd,"/fewclouds.png",10,.001,1),#Few Clouds-------------------------
                    "03":pictureToAnim(strip,dispStart,dispEnd,"/fewclouds.png",30,.001,1),#scattered clouds-------------------
                    "04":pictureToAnim(strip,dispStart,dispEnd,"/clouds.png",24,.001,1), # broken Clouds--------------------
                    "09":pictureToAnim(strip,dispStart,dispEnd,"/rain.png",15,.001,1),#shower rain---------------------------
                    "10":pictureToAnim(strip,dispStart,dispEnd,"/rain.png",30,.001,1),#rain-----------------------------------
                    "11":pictureToAnim(strip,dispStart,dispEnd,"/lightningrain.png",24,.001,1),#thunder storm------------------------
                    "13":pictureToAnim(strip,dispStart,dispEnd,"/snow.png",24,.001,1),#snow ------------------------------
                    "50":pictureToAnim(strip,dispStart,dispEnd,"/clouds.png",30,.001,1)#mist--------------------------------
                }    
    try:
        while True:
            weather = APIgetWeather(primary,secondary,loc)
            print("weather icon code", weather[0:2])
            print(weathColor[weather[0:2]])
            weathColor[weather[0:2]]
            # for i in range(strip.numPixels()):           #make next frame 
                # if(i < 82):
                    # strip.setPixelColor(i, Color(0,0,0))
                # else:
                    # strip.setPixelColor(i, weathColor[weather[0:2]])
                  
            #colorChange(strip,stripNextWeather, frames,delay)             

    except KeyboardInterrupt:
        print("exit weather")
        animExit(0,strip)  
   
#mod = modification
# 1 is multiframe
def modeTime(strip, dispStart, dispEnd, mod = 0):
    delay = 1
    colorDay = Color(200,200,255)#GRB
    colorNight = Color(100,100,1)
    stripNextTime = [0] * 300

    try:
        while True:
            now = datetime.now() #Get Time parameters
            timeCurr = (now.hour *3600) + (now.minute * 60) + now.second  #Decimal time in seconds
            timeDay = APIgetTime("solar_noon") 
            timeNight = (timeDay + 43200) % 86400

            print(timeDay,timeNight)
            print(timeCurr)

            if((timeCurr >= timeNight) and (timeCurr < timeDay)):
                print("Night -> Day-----------------------------------")    
                for i in range(strip.numPixels()):
                    if(i > dispStart and i < dispEnd): 
                        strip.setPixelColor(i, colorNight)                    #Initialise strip because NULL = 0
                        stripNextTime[i] = colorDay        #INIT Copy strip to temp array
                    else: 
                        strip.setPixelColor(i, Color(0,0,0))                #Initialise strip because NULL = 0
                        stripNextTime[i] = Color(0,0,0)       #MUST INIT STRIP MID LOOP BECAUSE ENTRENCE POINT IS VARIABLE

                timeCurrAdj = timeCurr - timeNight  # Find how many frames into the cycle the time is and start the color change timeCurrAdj man frames in
                OutputVec = colorChange(strip,stripNextTime, abs(timeDay - timeNight) ,delay,timeCurrAdj,mod)

                if (mod == 1): 
                    return OutputVec
                    
            elif((timeCurr < timeNight) or (timeCurr >= timeDay)):
                print("Day -> Night-----------------------------------")
                for i in range(strip.numPixels()):           #make next frame 
                    if(i > dispStart and i < dispEnd):
                        strip.setPixelColor(i, colorDay)
                        stripNextTime[i] = colorNight
                    else:
                        strip.setPixelColor(i, Color(0,0,0))
                        stripNextTime[i] = Color(0,0,0)
                        
                if (timeCurr >= timeDay): # Find how many frames into the cycle the time is and start the color change timeCurrAdj man frames in
                    timeCurrAdj = timeCurr - timeDay
                elif(timeCurr <= timeNight):
                    timeCurrAdj = timeCurr + (86400 - timeDay)
 
                OutputVec = colorChange(strip,stripNextTime, (timeNight + (86400 - timeDay)) ,delay, timeCurrAdj,mod)
                if (mod == 1): 
                    return OutputVec

    except KeyboardInterrupt:
        print("exit Time")
        animExit(0,strip)  
        
def modeMulti(strip):

    try:
        while True:
            stripMulti = []
            for j in range(strip.numPixels()):
                stripMulti.append(strip.getPixelColor(j))

            timeArray = modeTime(strip, 81,148,1)
            
            for i in range(strip.numPixels()):
                if (i > 81) and (i<148):
                    if timeArray[i] > 0:
                        stripMulti[i] = timeArray[i]
            # modeWeather(strip,)
            # modeCam(strip,frames, Color(LGreen, LRed, LBlue),Ldelay,Color(LEGreen, LERed, LEBlue)) #GLOBAL COLORS   
            colorChange(strip,stripMulti,1,.0001)
    except KeyboardInterrupt:
        print("exit Multi")
        animExit(0,strip)  


if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)    # Create NeoPixel object with appropriate configuration.
    strip.begin()    # Intialize the library (must be called once before other functions).

    method = "auto" #raw_input("Color choice(manual / auto):")
    
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
        LGreen = 0
        LRed = 0
        LBlue = 255
        print("Color Secondary/Night")
        LEGreen = 0
        LERed = 255
        LEBlue = 0
    # MULTIFRAME VARIABLES make setable at some point, constant for now
    timeBounds = (50,100)
    weatherBounds = (100,150)
    camBounds = (150,200)

    print("Main Color code:", hex(Color(LGreen, LRed, LBlue)))
    print("Secondary Color code:", hex(Color(LEGreen, LERed, LEBlue)))    
    print("-----------------------------------------")
    
    Lmode = ""
    try:
        while Lmode != "quit":  #=============MENU LOOP==============

            print("")
            #Menu text
            Lmode = raw_input("   -=-=-=-=-=| MAIN MENU |=-=-=-=-=- \n(1)'Flash' - Alternate between two colors \n(2)'Pulse' - Secondary Color is shown with Main color appearing/dissappearing \n(3)'Solid' - Main color is displayed \n(4)'MODE Cam' - used for prototyping programming structures \n(5)'MODE Time' - Alternates between two colors on a 24hr(86400sec) time frame \n(6)'MODE Weather' - fetch internet weather and display \n(7)'PicTest' - converts pic (left to right) to LED strip display \n(8) `MODE MultiFrame` - Displays all three modes at the same time dynamicly \n  'Quit' to quit \n - Choose your mode: ")
            Lmode = Lmode.lower()
            
            if (Lmode == "2"):#MATH PULSE
                Ldelay = input("Delay between Frames (Sec) (.0001 fast - 2 slow):")
                frames = input("Frames: ")
                animPulse(strip,frames, Color(LGreen, LRed, LBlue),Ldelay,Color(LEGreen, LERed,LEBlue))  # GLOBAL COLORS
                
            elif(Lmode == "3"):#ANIM SOLID
                print("choose color: \n")
                LRed = input("Red: ")
                LBlue = input("Blue: ")
                LGreen = input("Green: ") 
                DispStart = input("start position: ")
                DispEnd = input("end position: ")
                animSolid(strip,Color(LGreen,LRed,LBlue),DispStart,DispEnd)
                
            elif (Lmode == "6"):#MODE WEATHER
                modeWeather(strip,81,148)
                
            elif(Lmode == "1"):#ANIM FLASH
                Ldelay = .0001 #input("Delay between Frames (Sec) (.0001 fast - 2 slow):")
                frames = 60 #input("Frames: ")
                startIn = 50 #input("Start index: ")
                endIn = 250 #input("End Index: ")
                animFlash(strip,startIn,endIn,frames, Color(LGreen, LRed, LBlue),Ldelay,Color(LEGreen, LERed, LEBlue)) #GLOBAL COLORS
                
            elif(Lmode == "4"):#MODE CAM work in progress
                Ldelay = .001 #input("Delay between Frames (Sec) (.0001 fast - 2 slow):")
                frames = 10 #input("Frames: ")
                startIn = 0 #input("Start index: ")
                endIn = 299 #input("End Index: ")
                dispHeight = 20 #input("Display Height: ")
                dispWidth = 15 #input("Display Width: ")
                modeCam(strip,dispHeight,dispWidth,startIn,endIn,frames,Ldelay) 
                
            elif(Lmode == "5"): #MODE TIME
                modeTime(strip, 81,148)
                
            elif(Lmode == "7"): #picture animation mode
                print("ANIMATIONS")
                picList = os.listdir("./LED_assets/")
                print(picList)
                iter = 0
                for anim in picList: #show only stock anims not the processed
                    if(anim.find("MOD") == -1):
                        print(str(iter) + ': ' + anim)
                    iter+=1    
                        
                animIndex = raw_input("Number from list above: ")
                print(picList[int(animIndex)])
                Ldelay = input("Delay between Frames (Sec) (.0001 fast - 2 slow):")
                frames = input("Frames: ")
                startIn = input("Start index: ")
                endIn = input("End Index: ")
                pictureToAnim(strip,startIn,endIn,picList[int(animIndex)],frames,Ldelay)
                # DEBUG pictureToAnim(strip,0,299,picList[7],24,.0001)
            elif(Lmode == "8"):
                modeMulti(strip)
                
                

                
                
    except KeyboardInterrupt:
        print("exit program")
        animExit(0,strip)   
        os._exit(0)
        
4