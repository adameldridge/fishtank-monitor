import os
import time
import sqlite3
import datetime


#Load drivers
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Load file path of sensor output
tempSensor = '/sys/bus/w1/devices/28-031700d6ffff/w1_slave'

#Custom sleep function to allow interrupts
def sleep(n):
    for i in range(n):
        time.sleep(1)

#Read raw date from file
def tempRaw():
    f = open(tempSensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

#Process file contents
def readTemp():
    lines = tempRaw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = tempRaw()
    tempOutput = lines[1].find('t=')
    if tempOutput != -1:
        tempString = lines[1].strip()[tempOutput+2:]
        temp = float(tempString) / 1000.0
        return temp

#Store result in database
def storeTemp(temp):

    #Connect to database
    conn = sqlite3.connect('../fishtank.db')
    c = conn.cursor()

    # Insert record into database
    date = str(datetime.datetime.now().date())
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print (date, time, temp)
    c.execute("INSERT INTO watertemp (date, time, temp) VALUES (?,?,?)",
              (date, time, temp))

    # Commit to database and close
    conn.commit()
    conn.close()

#Run main loop
try:
    while True:
        storeTemp(readTemp())  
        sleep(300)
        
except KeyboardInterrupt:
    print("Exiting, bye")
    
