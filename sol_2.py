import RPi.GPIO as GPIO
import time

solenoid = 21

GPIO.setmode(GPIO.BCM)
#GPIO.setup(solenoid, GPIO.OUT)

def func1():
    return

try:
    GPIO.output(solenoid, GPIO.LOW)
    time.sleep(1)
    GPIO.cleanup()
except:
    func1()