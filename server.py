import time
import RPi.GPIO as GPIO

def my_callback(channel):
    print('This is a edge event callback function!')
    print('Edge detected on channel %s'%channel)
    print('This is run in a different thread to your main program')

print "Hello from Resin"

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.IN)

GPIO.add_event_detect(40, GPIO.RISING, callback=my_callback)  # add rising edge detection on a channel

while True:
	time.sleep(1)
