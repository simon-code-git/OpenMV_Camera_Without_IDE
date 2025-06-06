### Created by Simon Wong while working at BLINC Lab. 
### Updated May 28, 2025. 

import os
import serial
import struct
import time 
import cv2

PORT = 'COM5' # Look for "USB Serial Device (COM#)" in Windows Device Manager. Make sure OpenMV IDE is NOT running. 
PATH = '/Users/Simon Wong/Desktop/OpenMV/Video_Images' # Folder must already be made for script to work. 
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

images = sorted(
                [img for img in os.listdir(PATH) if img.startswith('img_') and img.endswith('.jpg')],
                key=lambda x: int(x.split('_')[1].split('.')[0]))
frame = cv2.imread(os.path.join(PATH, images[0]))
height, width, layers = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
filename = os.path.join(PATH, 'video.mov')
video = cv2.VideoWriter(filename, fourcc, framerate, (width, height)) 
for image in images:
    img_path = os.path.join(PATH, image)
    frame = cv2.imread(img_path)
    video.write(frame)
video.release()
print('Saved "video.mov" ')
