#!/usr/bin/env python

#########################
#
# the script turns a fan on and off when temperature acquired by an external ADC MCP3008
# exceeds thresholds.
#
# the script was tested on a raspberry pi equipped with MCP3008 ADC connected on SPI Interface
# and using adafruit MCP3008 library
#
#########################

#########################
#
# run-fan requires an NPN transistor and a resistor to be connected
# as follows:
# - emitter: connects to Raspberry GND and power supply GND
# - base: connects to 110 Ohm Resistor. The other pin of resistor to GPIO pin 25
# - collector: connects to fan GND
# - fan red (+): connects to external 12V power supply
#
# GPIO pin 25 is used, but it can be changed
#
#########################

#########################
#
# The original script is from:
# Source: https://github.com/dumbo25/rpi-fan/blob/master/run-fan.py
#
#########################
#
# CONFIGURATION SECTION NTC Value in Ohm
NTC=10000
# NTC Beta constant. See on the datasheet, otherwise leave it unchanged
beta=3950
# Pull up resistor in Ohm (in series with the NTC, connected to Vcc)
Rpullup=12000
# GPIO or BCM pin number to turn fan on and off
outpin = 25
# Time to sleep between checking the temperature
sleepTime = 30
# Log file path and name
logpath='/var/log/fan.log'
# Log enable
debug=1
# switch-on threshold in degrees centigrade
threshold=50
# delta for switch off, referred to upper threshold
delta = 5
# ADC3008 channel connectet to the NTC
adcchannel=1
# Temperature compensation, in degrees (if reading has an offset
compensation= 6
#########################
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import os
import time
import signal
import sys
import RPi.GPIO as GPIO
import datetime
import math
#########################
fileLog = open(logpath , 'a+', 0)
#########################
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
########################
# Log messages should be time stamped
def timeStamp():
    t = time.time()
    s = datetime.datetime.fromtimestamp(t).strftime('%Y/%m/%d %H:%M:%S - ')
    return s

# Write messages in a standard format
def printMsg(s):
    fileLog.write(timeStamp() + s + "\n")

#########################
class Pin(object):
    pin=outpin
    def __init__(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.setwarnings(False)
            if debug:
                printMsg("Initialized: run-fan using GPIO pin: " + str(self.pin))
        except:
            if debug:
                printMsg("If method setup doesn't work, need to run script as sudo")
            exit

    # resets all GPIO ports used by this program
    def exitPin(self):
        GPIO.cleanup()

    def set(self, state):
        GPIO.output(self.pin, state)

# Fan class
class Fan(object):
    fanOff = True

    def __init__(self):
        self.fanOff = True

    # Turn the fan on or off
    def setFan(self, temp, on, myPin):
        if on:
            if debug:
                printMsg("Turning fan on : {0:.2f}" .format(temp))
            myPin.set(on)
            self.fanOff = not on
        else:
            if debug:
                printMsg("Turning fan off : {0:.2f}" .format(temp))
            myPin.set(off)
            self.fanOff = on

# Temperature class
class Temperature(object):
    Temperature = 0.0
    startTemperature = 0.0
    stopTemperature = 0.0

    def __init__(self):

        # Start temperature in Celsius
        self.startTemperature = threshold

        # Wait until the temperature is M degrees under the Max before shutting off
        self.stopTemperature = self.startTemperature - delta
        if debug:
            printMsg("Start fan at: " + str(self.startTemperature))
            printMsg("Stop fan at: " + str(self.stopTemperature))

    def getTemperature(self):
        temp=mcp.read_adc(adcchannel)
#Steinhart-Hart formula for NTC conversion. Beta=3950, NTC value=10K, pull-up resistor=
        temp_conv=1/(((1/float(beta))*math.log(Rpullup/(float(1024)/temp-1)/NTC))+(1/298.15))-273.15+compensation
        self.Temperature=temp_conv
#        if debug:
#            printMsg("temp is {0:.2f}".format(temp_conv))
# Using the acquired temperature, turn the fan on or off
    def checkTemperature(self, myFan, myPin):
        self.getTemperature()
        if self.Temperature > self.startTemperature:
            # need to turn fan on, but only if the fan is off
            if myFan.fanOff:
                myFan.setFan(self.Temperature, True, myPin)
        elif self.Temperature <= self.stopTemperature:
            # need to turn fan off, but only if the fan is on
            if not myFan.fanOff:
                myFan.setFan(self.Temperature, False, myPin)

if debug:
    printMsg("Starting thermostat")
try:
    myPin = Pin()
    myFan = Fan()
    myTemp = Temperature()
    while True:
        myTemp.checkTemperature(myFan, myPin)
        # Read the temperature every N sec (sleepTime)
        # Turning a device on & off can wear it out
        time.sleep(sleepTime)

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    if debug:
        printMsg("keyboard exception occurred")
    myPin.exitPin()
    fileLog.close()

except:
    if debug:
        printMsg("ERROR: an unhandled exception occurred")
    myPin.exitPin()
fileLog.close()
