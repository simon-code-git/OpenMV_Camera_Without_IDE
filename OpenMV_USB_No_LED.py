### Created by Simon Wong while working at BLINC Lab. 
### June 4, 2025. 

import sensor
import pyb
import struct

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # QVGA resolution is 320x240.
sensor.skip_frames(time = 2000)

usb = pyb.USB_VCP() 

pyb.LED(0).off()
pyb.LED(1).off()
pyb.LED(2).off()

while True:
    if usb.any():
        cmd = usb.read().decode().strip()
        if cmd == "snap":
            img = sensor.snapshot()
            buffer = img.compress(quality=90).bytearray()
            usb.write(struct.pack("<L", len(buffer)))
            usb.write(buffer)
           

