### Created by Simon Wong while working at BLINC Lab. 
### June 4, 2025. 

import sensor
import pyb
import struct
import time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

usb = pyb.USB_VCP()

led = pyb.LED(1)
led_is_on = False
LED_OFF_TIMEOUT = 500 # Minimum LED time on. 
last_activity_time = time.ticks_ms()  

while True:
    current_time = time.ticks_ms()
    if usb.any():
        if not led_is_on:
            led.on()
            led_is_on = True
        last_activity_time = current_time
        try:
            cmd_bytes = usb.read()
            if cmd_bytes:
                cmd = cmd_bytes.decode().strip()
                if cmd == "snap":
                    img = sensor.snapshot()
                    compressed_img = img.compress(quality=90)
                    buffer = compressed_img.bytearray()
                    usb.write(struct.pack("<L", len(buffer)))
                    usb.write(buffer)    
        except Exception as e:
            pass
    if led_is_on and time.ticks_diff(current_time, last_activity_time) > LED_OFF_TIMEOUT: 
        # If the time difference is greater than minimum time, then turn off. 
        led.off()
        led_is_on = False

