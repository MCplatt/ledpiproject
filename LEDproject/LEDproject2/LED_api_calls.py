from neopixel import *
import time
from datetime import datetime
import argparse
import math
import array
import numpy
import sys
import os
import requests
import json
from picamera import PiCamera
import LED_low_level

#https://agromonitoring.com/api/current-weather
def APIgetWeather(param1,param2,location):
    URL = "https://api.openweathermap.org/data/2.5/weather"
    apikey = "5e62e6d5676f5954155893401110d3f2"
    payload = {'q':location,'appid':apikey}
    time.sleep(5) #only allow 1 request per 5 second

    GETdata = requests.get(url = URL, params = payload)
    # if GETdata.status_code == 200:
        # print json.loads(GETdata.content.decode('utf-8'))
    GETdata = GETdata.json()
    
    print(GETdata)
    if param1 == "weather":
        return(GETdata[param1][0][param2])
    else:
        return(GETdata[param1][param2])
        
        
        
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