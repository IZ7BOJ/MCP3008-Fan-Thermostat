The script turns a fan on and off when temperature exceeds thresholds.

the temperature is aquired by a MCP3008 ADC connected on the raspberry SPI Interface (MCP3008 Adafruit library needed);
the sensor configured in the script is a 10KOhm NTC with Beta=3950 and pull-up resistor of 12K, but can be changed;
the fan is controlled by one of the Raspberry GPIO pin (pin 25 by default);

If a 12V fan is used, it should be driven by a NPN transistor (eg: 2N2222) connected as follows:
- emitter: connects to Raspberry GND and power supply GND
- base: connects to 110 Ohm Resistor. The other pin of resistor to GPIO pin 25
- collector: connects to fan GND
- fan red (+): connects to external 12V power supply

If other type of fan are used, the BJT can drive a 12V relè

The scripts write on/off and exception events on a log file

The original script is from:
Source: https://github.com/dumbo25/rpi-fan/blob/master/run-fan.py

You can start automatically the script using systemd

Create a systemd service file using:
$ sudo nano /lib/systemd/system/run-fan.service
   
with the contents as shown below (remove # and leading spaces):
[Unit]
Description=run fan when hot
After=meadiacenter.service

[Service]
User=root
Group=root
Type=simple
ExecStart=/usr/bin/python /home/pi/run-fan.py #Insert real path of the script!!
Restart=Always

[Install]
WantedBy=multi-user.target

ctrl-o, ENTER, ctrl-x to save and exit the nano editor

After any changes to /lib/systemd/system/run-fan.service:
sudo systemctl daemon-reload
sudo systemctl enable run-fan.service
sudo reboot

Ensure the run-fan.service in systemd is enabled and running:
systemctl list-unit-files | grep enabled
systemctl | grep running | grep fan
systemctl status run-fan.service -l

If there are any issues with starting the script using systemd, 
then examine the journal using:
sudo journalctl -u run-fan.service
