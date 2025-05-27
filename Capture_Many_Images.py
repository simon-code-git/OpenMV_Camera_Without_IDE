import os
import serial
import struct
import time 

PORT = 'COM5' # Look for USB Serial Device (COM#) in Windows Device Manager. Make sure OpenMV IDE is NOT running. 
PATH = '/Users/Simon Wong/Desktop/OpenMV/Many_Images'
NUM_IMAGES = 100

serial_port = serial.Serial(PORT, 
                            baudrate=115200, 
                            bytesize=serial.EIGHTBITS, 
                            parity=serial.PARITY_NONE,
                            xonxoff=False, 
                            rtscts=False, 
                            stopbits=serial.STOPBITS_ONE, 
                            timeout=None, 
                            dsrdtr=True)

def capture(sp, count):
    sp.setDTR(True) 
    sp.write(b'snap')
    sp.flush() 
    size = struct.unpack('<L', sp.read(4))[0]
    img = sp.read(size)
    file_path = os.path.join(PATH, f'img_{count}.jpg')
    with open(file_path, 'wb') as file:
        file.write(img)
        print(f'Saved "img_{count}.jpg" ')

start = time.time()
for count in range(NUM_IMAGES): 
    capture(serial_port, count)
end = time.time()
framerate = NUM_IMAGES / (end - start)
print(f'Average framerate: {framerate:.2f}')


    