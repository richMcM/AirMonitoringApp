import urllib.request
import requests


# Write Key C49FFS3J5D523Q74
def writeToThingSpeak(pm25, pm10, temp, hum, voc):
    URL='https://api.thingspeak.com/update?api_key='
    KEY='C49FFS3J5D523Q74'
    HEADER='&field1={}&field2={}&field3={}&field4={}&field5={}'.format(pm25, pm10, temp, hum, voc)
    new_URL = URL+KEY+HEADER
    data=urllib.request.urlopen(new_URL)
    print(data)
    print(new_URL)
    

#if __name__ == '__main__':
 #   main()