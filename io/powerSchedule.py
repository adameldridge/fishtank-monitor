#Import dependencies
import RPi.GPIO as GPIO
import datetime
import time
import requests

#Set pin numbering mode
GPIO.setmode(GPIO.BCM)

#Setup pins
power = 27
GPIO.setup(power, GPIO.OUT)

#Custom sleep function to allow interrupts
def sleep(n):
    for i in range(n):
        time.sleep(1)

#Function for sending notifications
def send_notification(event):
  requests.post('http://maker.ifttt.com/trigger/'+ event + '/with/key/mcoQxo3fXk-U71XcPETtcHcgLfO1FIJ8vcGt8tKRkgp')

#lights_on_notifications_sent = 0
#lights_off_notifications_sent = 0

try:
    #Run main loop
    while True: 
        #Set current time
        now = datetime.datetime.now()

        #Set power schedule
        powerOnTime = now.replace(hour=17, minute=15, second=0, microsecond=0)
        powerOffTime = now.replace(hour=23, minute=15, second=0, microsecond=0)

        #Determine if power should be on or off
        if (now > powerOnTime and now < powerOffTime):
            #GPIO.output(power, GPIO.HIGH)
            GPIO.setup(power, GPIO.OUT)
            print("Power on: " + str(now))
            #lights_off_notifications_sent = 0
            #lights_on_notifications_sent += 1
            #if (lights_on_notifications_sent == 1):
             # send_notification("fish_tank_lights_on")
        else:
            #GPIO.output(power, GPIO.LOW)
            GPIO.setup(power, GPIO.IN)
            print("Power off: " + str(now))
            #lights_on_notifications_sent = 0
            #lights_off_notifications_sent += 1
            #if (lights_off_notifications_sent == 1):
             # send_notification("fish_tank_lights_off")

        #Delay for 5 seconds
        sleep(60)

except KeyboardInterrupt:
    print("Exiting, bye")
    #send_notification("fish_tank_lights_off")
    GPIO.cleanup()
