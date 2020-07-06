import RPi.GPIO as GPIO
import time

solenoid = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(solenoid, GPIO.OUT)

GPIO.output(solenoid, GPIO.HIGH)