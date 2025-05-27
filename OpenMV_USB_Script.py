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
            buffer = img.compress(quality=90).bytearray()
            usb.write(struct.pack("<L", len(buffer)))
            usb.write(buffer)
           

