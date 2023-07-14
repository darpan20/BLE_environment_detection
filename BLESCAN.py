import time
import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import digitalio
import adafruit_sdcard
import storage
from adafruit_ble import BLERadio

from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
import board
import busio as io
i2c = io.I2C(board.SCL, board.SDA)   #initializing the I2C interface for our firmware

#create an instance of the SSD1306 I2C driver 
import adafruit_ssd1306
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c,addr=0x3c)
ble = BLERadio()

found = set()
scan_responses = set()
# By providing Advertisement as well we include everything, not just specific advertisements.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# Use board.SD_CS for Feather M0 Adalogger
cs = digitalio.DigitalInOut(board.D10)

# Or use a GPIO pin like 15 for ESP8266 wiring:
#cs = digitalio.DigitalInOut(board.GPIO15)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
btn = DigitalInOut(board.SWITCH)
btn.direction = Direction.INPUT
btn.pull = Pull.UP


def start_stop():
 oled.fill(0)
 oled.text("Press start!!",10,10,1)
 oled.show()

 print("Press start!!")
 while True:
   pressed=True
   c=0
   if not btn.value:
     
     with open("/sd/test.txt", "a") as f:
	for advertisement in ble.start_scan(interval=5.0,window=0.5,timeout=None):
	    pressed=btn.value
	    
            if not pressed and c!=0:
               ble.stop_scan()
               oled.fill(0)
               oled.text("stopped!!!",1,1,1)
               oled.show()

               
               return
	    addr = advertisement.address
	   
	    rssi = advertisement.rssi
	    tx_power = advertisement.tx_power
	
	    found.add(addr)   
	    print("READING#"+repr(addr)[8:-1]+" "+ repr(rssi)+" "+repr(tx_power))      # repr or tring both for string printing of object
	    oled.fill(0)
	    oled.text("Received:",10,0,1)
	    oled.text("rssi:"+repr(rssi)+" tx_pwr:"+repr(tx_power),5,10,1)
	    oled.text(repr(addr)[8:-1],1,20,1)
            oled.show()
	    f.write(repr(addr)[8:-1]+" "+ repr(rssi)+" "+repr(tx_power)+'\n')
 	    print("Written data!!")
	    print("\t"+repr(found))
          
            time.sleep(0.2)   
            c+=1

start_stop()   
