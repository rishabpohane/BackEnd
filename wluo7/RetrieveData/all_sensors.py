#!/usr/bin/python
import signal, sys, time
from Adafruit_I2C import Adafruit_I2C
from adc_read import ADS1115_Read
import Adafruit_BBIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855



def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

########
#TEMP
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

# BeagleBone Black software SPI configuration.
CLK = 'P9_12'
CS  = 'P9_15'
DO  = 'P9_23'
temp_sensor = MAX31855.MAX31855(CLK, CS, DO)
#TEMP
#######

########
#ACCEL
gain = 4096
sps = 860
adc = ADS1115_Read()
#ACCEL
#######

######
#GYRO
i2c = Adafruit_I2C(0x6b)
i2c.write8(0x20,0x0F) #switch to normal mode(enable x,y,z) (set Hz to 100)
i2c.write8(0x23,0x00) #set resolution. 245 dps, sensitivity = 0.00875
xrot = 0#the actual rotation in each axis
yrot = 0
zrot = 0
xlo = 0
xhi = 0
xdata = 0
ylo = 0
yhi = 0
ydata = 0
zlo = 0
zhi = 0
zdata = 0
xavg = 0
yavg = 0
zavg = 0
check_bit = 0

n=0
c = 1000
while n<c:
  check_bit = i2c.readU8(0x27) 
  if(check_bit & 8 == 8):
    xlo = i2c.readU8(0x28)
    xhi = i2c.readS8(0x29)
    ylo = i2c.readU8(0x2A)
    yhi = i2c.readS8(0x2B)
    zlo = i2c.readU8(0x2C)
    zhi = i2c.readS8(0x2D)
    xavg += (xlo | (xhi<<8)) * 0.0000875
    yavg += (ylo | (yhi<<8)) * 0.0000875
    zavg += (zlo | (zhi<<8)) * 0.0000875
    n += 1
xavg = xavg/c
yavg = yavg/c
zavg = zavg/c
print "xavg %f\tyavg %f\tzavg %f" % (xavg,yavg,zavg)
#GYRO
######


n = 0;
while True:
  time.sleep(0.3)
  check_bit = i2c.readU8(0x27) 
  if(check_bit & 8 ==8):

    xlo = i2c.readU8(0x28)#read the xlo bit. it is signed
    xhi = i2c.readS8(0x29)#read the xhi bit. it is signed
    ylo = i2c.readU8(0x2A)
    yhi = i2c.readS8(0x2B)
    zlo = i2c.readU8(0x2C)
    zhi = i2c.readS8(0x2D)
    xdata = (xlo | (xhi<<8))
    ydata = (ylo | (yhi<<8)) 
    zdata = (zlo | (zhi<<8))

    xdata *= 0.00875
    ydata *= 0.00875
    zdata *= 0.00875

    xrot += xdata *0.01 - xavg # multiply by frequency (default is 100 hz)
    yrot += ydata *0.01 - yavg
    zrot += zdata *0.01 - zavg

    distance = adc.read(3)
    distance = 12.434 * ( distance ** (-1.065))#approximation into cm
    xaccel = adc.read(0)#accelerometer also hooked up
    yaccel = adc.read(1)
    zaccel = adc.read(2)
  
    temp = sensor.readTempC()

    f = open('/root/wluo7/SensorData/distance.dat', 'w')
    f.write("%.4f" % (distance))
    f.close()
    f = open('/root/wluo7/SensorData/gyroscope.dat', 'w')
    f.write("%.4f" % (zrot))
    f.close()
    f = open('/root/wluo7/SensorData/accelerometer.dat', 'w')
    f.write("%.4f" % (zaccel))
    f.close()
    f = open('/root/wluo7/SensorData/temperature.dat', 'w')
    f.write("%.4f" % (temp))
    f.close()
    #print "Dist: %.4f\tx: %.4f\ty: %.4f\tz: %.4f\txrot: %.4f\tyrot: %.4f\tzrot %.4f" % (distance,xaccel,yaccel,zaccel, xrot, yrot,zrot)
    n += 1

