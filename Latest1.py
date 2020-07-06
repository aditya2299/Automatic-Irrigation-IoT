from time import sleep
import RPi.GPIO as GPIO
import os
import datetime
import Adafruit_DHT
from firebase import firebase
import urllib2, urllib, httplib

GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
sensor = Adafruit_DHT.DHT11
temp_pin = 17 
GPIO.setwarnings(False)
humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_pin)

firebase = firebase.FirebaseApplication('https://garden-d744a.firebaseio.com/', None)


def update_firebase():
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_pin)
    motor_state = firebase.get('/Home_garden_automation/motor_state',None)
    print "motor_state",motor_state
    
    if humidity is not None and temperature  is not None:
        str_temp = ' {0:0.2f} *C '.format(temperature)
        str_hum  = ' {0:0.2f} %'.format(humidity)
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        
    if (motor_state == unicode("1")):
        #turn on motor
        import sol_1
        execfile('sol_1.py')
        print("Pump on\n")
    elif (motor_state == unicode("2")):
        #automate
        print "motor automatic control"
        import mos_1
        execfile('mos_1.py')
    elif (motor_state == unicode("0")):
        #turn off motor
        import sol_2
        execfile('sol_2.py')
        print("Pump off\n")
    else:
        print('Failed to get reading. Try again!')
        sleep(1)

    #data = {"temp": temperature, "humidity": humidity}
    firebase.put('Home_garden_automation','temperature',str(temperature))
    firebase.put('Home_garden_automation','humidity',str(humidity))
    #firebase.post('/sensor/MOISTURE',data_M)
    os.system('clear')

while True:
    update_firebase()
    sleep(1)
