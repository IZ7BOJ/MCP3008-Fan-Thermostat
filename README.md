# MCP3008-Fan-Thermostat
# the script turns a fan on and off when temperature exceeds thresholds.
#
# the temperature is aquired by a MCP3008 ADC connected on the raspberry SPI Interface (MCP3008 Adafruit library needed);
# the sensor configured in the script is a 10KOhm NTC with Beta=3950 and pull-up resistor of 12K, but can be changed;
# the fan is controlled by one of the Raspberry GPIO pin (pin 25 by default) 
# if a 12V fan is used, it should be driven by a NPN transistor (eg: 2N2222) connected as follows:
#
# - emitter: connects to Raspberry GND and power supply GND
# - base: connects to 110 Ohm Resistor. The other pin of resistor to GPIO pin 25
# - collector: connects to fan GND
# - fan red (+): connects to external 12V power supply
#
# If other type of fan are used, the BJT can drive a 12V relè
#
# The scripts write on/off and exception events on a log file
#
# The original script is from:
# Source: https://github.com/dumbo25/rpi-fan/blob/master/run-fan.py
#
