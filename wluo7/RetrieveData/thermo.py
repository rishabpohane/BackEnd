#!/usr/bin/python
import time

import Adafruit_BBIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

# BeagleBone Black software SPI configuration.
CLK = 'P9_12'
CS  = 'P9_15'
DO  = 'P9_23'
sensor = MAX31855.MAX31855(CLK, CS, DO)

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
while True:
    temp = sensor.readTempC()
    internal = sensor.readInternalC()
    print('Thermocouple Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(temp, c_to_f(temp)))
    print('    Internal Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(internal, c_to_f(internal)))
    time.sleep(1.0)
