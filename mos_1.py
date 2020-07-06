import RPi.GPIO as GPIO
import os
from time import sleep
import datetime
import Adafruit_DHT
from firebase import firebase

mos_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(mos_pin,GPIO.IN)
sensor = Adafruit_DHT.DHT11
temp_pin = 17

firebase = firebase.FirebaseApplication('https://garden-d744a.firebaseio.com/', None)

def callback(pin):
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_pin)
    str_temp = ' {0:0.2f} *C '.format(temperature)
    str_hum  = ' {0:0.2f} %'.format(humidity)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    firebase.put('Home_garden_automation','temperature',str(temperature))
    firebase.put('Home_garden_automation','humidity',str(humidity))
    
    time = datetime.datetime.now().strftime("%H:%M")
    start_hour = str(firebase.get('/Home_garden_automation/start_hour',None))[1:3]
    start_min = str(firebase.get('/Home_garden_automation/start_min',None))[1:3]
    end_hour = str(firebase.get('/Home_garden_automation/end_hour',None))[1:3]
    end_min = str(firebase.get('/Home_garden_automation/end_min',None))[1:3]
    
    start_time = start_hour+':'+start_min
    end_time = end_hour+':'+end_min
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin,GPIO.IN)
    
    if ((time > start_time) and (time < end_time)):
        try:
            if GPIO.input(pin):
                import sol_1
                execfile('sol_1.py')
                print("Pump on(Auto)")
            else:
                import sol_2
                execfile('sol_2.py')
                print("Pump off(Auto)")
        except KeyboardInterrupt:
            GPIO.cleanup()
    else:
        print("\nAuto Mode completed in given time \nOR \nChange time to perform Auto Mode")
        GPIO.cleanup()
    sleep(1)
    os.system('clear')
while True:
    motor_state = firebase.get('/Home_garden_automation/motor_state',None)
    if (motor_state == unicode("2")):
        callback(mos_pin)
        sleep(1)
    else:
        break