### Written by Simon Wong while working at BLINC Lab. 
### May 28, 2025. 

import sensor
import pyb
import struct

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # QVGA resolution is 320x240.
sensor.skip_frames(time = 2000)

usb = pyb.USB_VCP()

while True:
    if usb.any():
        cmd = usb.read().decode().strip()
        pyb.LED(2).on()
        if cmd == "snap":
            img = sensor.snapshot()

            # Add additional image processing code here... 

            buffer = img.compress(quality=90).bytearray()
            usb.write(struct.pack("<L", len(buffer)))
            usb.write(buffer)          

