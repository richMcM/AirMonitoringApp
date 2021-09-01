# Air Monitoring Main App

#imports for LCD Screen Functions
from rpi_lcd import LCD


import time
import board
from busio import I2C
import adafruit_bme680

import os
import csv
import io

import logging
import datetime

#imports from Email_Alerts for Email Alert Functions
from Email_Alerts import email_alert

#imports for Nova Particle Matter Sensor Reading Function
from NovaPM_func import read_nova_pm_sensor

#import function to save sensor data to a local csv file
from BME680_func import append_csv

#import for BME680 Sensor Reading Function
from BME680_func import read_bme680_sensor

#import alarm buzzer function
from Buzzer_Alarm_func import buzz_alarm

#Ceate an instance of LCD
lcd = LCD()

#import function to save sensor data to ThingSpeak
import ThingSpeakWrite 

#Used for tracking, to track when last an email alert was sent
timeSinceLastEmailTimer = 0
sendFirstEmail = 0

print('Air Monitoring Program Running!')

while True:
    #Will increment to 1 once the very first notification email is sent so that time can be tracked so that an email is only sent once every 10 minutes at most
    sendFirstEmail = 0
    
    #Try to Read BME680 Sensor, store data to varialbles and Print to LCD screen
    try:
        #Getting BME680 Sensor Data 
        BME_Data = read_bme680_sensor()
        #Storing current temp,humidity and VOC reading to variables
        temp = round(BME_Data['Temp'], 3) # Temp Round to 3 decimal places
        hum = round(BME_Data['Humidity'], 2) # Humidity rounded to 2 places
        voc = BME_Data['Gas']
        
        lcd.clear()
        print("\nTemp: %0.1fc" % temp)
        print("Humidity: %0.1f %%" % hum)
        #Print Temperature and Humidy Reading on LCD
        lcd.text("Temp:%0.1fc" % temp + " Hu:%0.1f%%" % hum, 1)
        #Print VOC gas Reading on LCD
        print("VOCs: %d ohms" % voc)
        lcd.text("VOCs: %d ohms" % voc, 2)
    except:
        print('Error getting data from BME680 Sensor')
    
    #Try to Read SDS011 Particle Matter Sensor, store data to varialble and Print to LCD screen
    try:
        #Getting SDS011 Particle Matter Sensor Data 
        particle_matter_data = read_nova_pm_sensor()
        #Storing current PM10 and PM2.5 to variables
        pm25 = particle_matter_data['PM2_5']
        pm10 = particle_matter_data['PM10']
        print("PM2.5", pm25)
        #Print Particle Matter data to LCD screen
        lcd.text("PM2.5:   " + str(pm25) + "ug/m3", 3)
        print("PM10", pm10)
        lcd.text("PM10:   " + str(pm10) + "ug/m3", 4)
    except:
        print('Error getting data from SDS011 Particle Matter Sensor')
        
    
    
    time.sleep(5)

    #Try to Evaluate Particle Matter Data
    try:
        if pm25 > 10 or pm10 > 20:
        
            #As we know a notificaion will be sent we set the timer if no email notification has been sent prevoiusly since program startup
            if timeSinceLastEmailTimer == 0:
                    #Setting the time for the first sent notifiacation email
                    timeSinceLastEmailTimer = time.time()
                    sendFirstEmail+=1
                    
            #Used to calcluate time since last notification email was sent
            currentTime = time.time()
            timeDiff = currentTime -timeSinceLastEmailTimer
                
            #If Only PM2.5 is high
            if pm25 > 10 and pm10 < 21:
                    
                #Evaluates that at least 10 mins in seconds has passed since the last email and noise nitifcation were sent before notifying again
                #Also will send an email if it is the very first email to be sent
                if timeDiff > 600 or sendFirstEmail == 1:  
                    print("PM 2.5 is greater than 10ug/m3, Air Qulity is higher than optimal Recommended Level!")
                    #Sound Buzzer Alarm
                    buzz_alarm()
                    #Sent notification email
                    email_alert("rick_mcmanus@hotmail.com", "PM2.5 is greater than 10ug/m3", "Particle Matter 2.5 is above optimal recommended level. PM2.5 currenlty is at "
                    + str(pm25) + "ug/m3") 
                    #Sets time of the Most recent sent eamil and noise notifications
                    timeSinceLastEmailTimer = time.time()
                    
                #Print notification of PM2.5 being above reccomened level to LCD
                lcd.text("PM2.5 is High", 1)
                lcd.text("at : " + str(pm25) + "ug/m3", 2)
                time.sleep(10) #Display message for 10 seconds
                
            #If Only PM10 is high
            elif pm25 < 11 and pm10 > 20:
                
                #Evaluates that at least 10 mins in seconds has passed since the last email and noise nitifcation were sent before notifying again
                #Also will send an email if it is the very first email to be sent
                if timeDiff > 600 or sendFirstEmail == 1:  
                    print("PM10 is greater than 20ug/m3, Air Qulity is higher than optimal Recommended Level!")
                    #Sound Buzzer Alarm
                    buzz_alarm()
                    #Sent notification email
                    email_alert("rick_mcmanus@hotmail.com", "PM10 is greater than 20ug/m3", "Particle Matter 10 is above optimal recommended level. PM10 currenlty is at "
                    + str(pm10) + "ug/m3") 
                    #Sets time of the Most recent sent eamil and noise notifications
                    timeSinceLastEmailTimer = time.time()
                    
                #Print notification of PM10 being above reccomened level to LCD 
                lcd.text("PM10 is High", 1)
                lcd.text("at : " + str(pm10) + "ug/m3", 2)
                time.sleep(10) #Display message for 10 seconds
            
            #Both PM2.5 and PM10 are high
            elif pm25 > 10 and pm10 > 20:
                
                #Evaluates that at least 10 mins in seconds has passed since the last email and noise nitifcation were sent before notifying again
                #Also will send an email if it is the very first email to be sent
                if timeDiff > 600 or sendFirstEmail == 1:  
                    print("PM2.5 and PM10 are High, Air Qulity is higher than optimal Recommended Level!")
                    #Sound Buzzer Alarm
                    buzz_alarm()
                    #Sent notification email
                    email_alert("rick_mcmanus@hotmail.com", "PM2.5 and PM10 are Higher than Recommended",
                    "Particle Matter 2.5 is above optimal recommended level of 10ug/m3."
                    + " PM2.5 currenlty is at " + str(pm25) + "ug/m3"
                    + "\n\nParticle Matter 10 is also above optimal recommended level of 20ug/m3."
                    + " PM10 currenlty is at " + str(pm10) + "ug/m3") 
                    #Sets time of the Most recent sent eamil and noise notifications
                    timeSinceLastEmailTimer = time.time()
                    
                #Print notification of PM2.5 being above reccomened level to LCD
                lcd.text("PM2.5 is High", 1)
                lcd.text("at : " + str(pm25) + "ug/m3", 2)
                lcd.text("PM10 is High", 3)
                lcd.text("at : " + str(pm10) + "ug/m3", 4)
                time.sleep(10) #Display message for 10 seconds  
    except:
        print('Error Evaluating Particle Matter Data')
     
    #Try to save Data to ThingSpeak
    try:
        #Save pm25, pm10, temp, hum, voc sensor data to ThingSpeak
        ThingSpeakWrite.writeToThingSpeak(pm25, pm10, temp, hum, voc)
        print('Data Saved to ThingSpeak')
    except:
        print('Error Saving Data to ThingSpeak')
        
        #If problem with saving data to ThingSpeak Save Particle Matter and BME680 results to local CSV Files
        try:
            #Save BME680, Temp, Humidty and VOC gas Readings to Local Result File
            bme680_field_list = ['Date', 'Temp', 'Gas', 'Humidity']
            #Takes CSV file location, data fields and Sensor data i.e Temp, Humidity and VOC gas
            append_csv('./Sensor_Reading_Results/BME680_Results.csv', bme680_field_list, BME_Data)
            
            #Save Nove PM, PM2.5 and PM10 Readings to Local Result File                   
            nova_pm_field_list = ['Date', 'PM10', 'PM2_5']
            #Takes CSV file location, data fields and Sensor data i.e PM2.5 and PM10
            append_csv('./Sensor_Reading_Results/NovaPM_Results.csv', nova_pm_field_list, particle_matter_data)
            print('Saved sensor Reading to CSV!')
        #If problem saving Data Lacally Print Error
        except:
            print('Error Saving Sensor data locally')
            
