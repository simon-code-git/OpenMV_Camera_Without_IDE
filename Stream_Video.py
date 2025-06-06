### Created by Simon Wong while working at BLINC Lab. 
### Updated June 6, 2025. 

import os
import serial
import struct
import time 
import cv2
import numpy as np

PORT = 'COM5' # Look for "USB Serial Device (COM#)" in Windows Device Manager. Make sure OpenMV IDE is NOT running. 
PATH = '/Users/Simon Wong/Desktop/OpenMV/Screenshots' # Folder must already be made for script to work. 
NUM_IMAGES = 1000000

serial_port = serial.Serial(PORT, 
                            baudrate=115200, 
                            bytesize=serial.EIGHTBITS, 
                            parity=serial.PARITY_NONE,
                            xonxoff=False, 
                            rtscts=False, 
                            stopbits=serial.STOPBITS_ONE, 
                            timeout=None, 
                            dsrdtr=True)

prev_time = time.time()
fps = 0

def capture_and_display(sp, count):
    global prev_time, fps

    sp.setDTR(True) 
    sp.write(b'snap')
    sp.flush() 
    size = struct.unpack('<L', sp.read(4))[0]
    img = sp.read(size)

    img = np.frombuffer(img, dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    current_time = time.time()
    elapsed = current_time - prev_time
    if elapsed > 0:
        fps = 1 / elapsed 
    prev_time = current_time
    resolution_text = f'Resolution: {img.shape[1]}x{img.shape[0]}'
    fps_text = f'FPS: {fps:.2f}'
    frame_num_text = f'Frame: {count + 1}'

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.3
    color = (0, 255, 0)
    thickness = 1
    line_type = cv2.LINE_AA
    cv2.putText(img, resolution_text, (5, 15), font, font_scale, color, thickness, line_type)
    cv2.putText(img, fps_text, (5, 30), font, font_scale, color, thickness, line_type)
    cv2.putText(img, frame_num_text, (5, 45), font, font_scale, color, thickness, line_type)

    cv2.namedWindow('OpenMV H7 Camera', cv2.WINDOW_NORMAL)
    cv2.imshow('OpenMV H7 Camera', img)
    key = cv2.waitKey(1) # Necessary for OpenCV event loop to refresh display window. 

    if key == 32:  # Press space bar to save screenshot to folder specified by PATH. 
        filename = os.path.join(PATH, f"Screenshot_{count}.png")
        cv2.imwrite(filename, img)
        print(f"Saved screenshot: {filename}")

for count in range(NUM_IMAGES): 
    capture_and_display(serial_port, count)
    if cv2.waitKey(1) & 0xFF == 27: # Press escape key while inside OpenCV window to end script prematurely. 
        break
cv2.destroyAllWindows()
