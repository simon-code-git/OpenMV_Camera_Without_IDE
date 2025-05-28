### Created by Simon Wong while working at BLINC Lab. 
### May 28, 2025. 

import os
import serial 
import struct

PORT = 'COM5'
PATH = '/Users/Simon Wong/Desktop/OpenMV'

sp = serial.Serial(PORT, 
                   baudrate=115200, 
                   bytesize=serial.EIGHTBITS, 
                   parity=serial.PARITY_NONE,
                   xonxoff=False, 
                   rtscts=False, 
                   stopbits=serial.STOPBITS_ONE, 
                   timeout=None, 
                   dsrdtr=True)
sp.setDTR(True) 
sp.write(b'snap')
sp.flush()
size = struct.unpack('<L', sp.read(4))[0]
img = sp.read(size)
sp.close()

with open(os.path.join(PATH, 'img.jpg'), "wb") as file:
    file.write(img)