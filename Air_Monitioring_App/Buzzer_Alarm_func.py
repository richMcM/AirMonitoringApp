# Buzzer Alarm Function

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Buzzer_PIN = 25 #Set Bizzer Signal pin to GPIO 25
GPIO.setup(Buzzer_PIN, GPIO.OUT, initial=GPIO.LOW) #Setup GPIO specifying buzzer signal pin and setting pin signal to low initially
buzzer = GPIO.PWM(Buzzer_PIN, 1000) # Set frequency to 1 Khz

def buzz_alarm():
    buzzer.start(1) # Set dutycycle to 1%
    sleep(0.15) #length of time for buzzer to sounds in seconds
    buzzer.stop() # Stop the buzzer


'''
print('[Press CTRL + C to end the script!]')
try: # Main program loop
    while True:
        print('Buzzer will be on for 3 seconds')
        print(GPIO.output(Buzzer_PIN, GPIO.HIGH)) # Buzzer ON
        sleep(3) # Wait for 3 seconds
        print('Buzzer wil be off for 1 second')
        GPIO.output(Buzzer_PIN, GPIO.LOW) # Buzzer OFF
        sleep(1) # Wait for a second
        # Scavenging work after the end of the program
except KeyboardInterrupt:
    print('\nScript end!')
    
'''