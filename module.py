### Created by Simon Wong while working at BLINC Lab. 
### Updated June 13, 2025. 

import serial
import struct
import cv2 as cv
import numpy as np

class CameraStream: 
# Everything is contained in a single class. 
    def __init__(self, port='COM4', baudrate=115200, rotation=0): # Initializes camera class. Make sure to specify COM port. 
        self.serial_port = serial.Serial(port, 
                                        baudrate=baudrate, # Serial communication speed. 
                                        bytesize=serial.EIGHTBITS, # Number of data bits per cycle. 
                                        parity=serial.PARITY_NONE, # No error checking. 
                                        xonxoff=False, # No software flow control. 
                                        rtscts=False, # No hardware flow control using RTS/CTS lines. 
                                        stopbits=serial.STOPBITS_ONE, # Number of stop bits. 
                                        timeout=None, # Wait forever until data arrives. 
                                        dsrdtr=True) # Hardware flow control using DSR/DTR lines. 
        if rotation == 0: 
            self.rotation = None
        elif rotation == 90: 
            self.rotation = cv.ROTATE_90_CLOCKWISE
        elif rotation == 180: 
            self.rotation = cv.ROTATE_180
        elif rotation == 270: 
            self.rotation = cv.ROTATE_90_COUNTERCLOCKWISE
        else: 
            self.rotation = None
            
    def capture(self): 
    # Function for capturing a single frame from the camera. 
        self.serial_port.setDTR(True) # Set the DTR (data terminal ready) line to active. 
        self.serial_port.write(b'snap') # Sends command to camera to capture an image. 
        self.serial_port.flush() # Waits for snap command to be sent (empty before) before continuing. 
        size = struct.unpack('<L', self.serial_port.read(4))[0] # Gets size from 4 little-endian unsigned long bytes. 
        img = self.serial_port.read(size) # Reads the size number of bytes from the serial port. 
        img = np.frombuffer(img, dtype=np.uint8) # Converts byte data to numpy 8-bit integer array. 
        img = cv.imdecode(img, cv.IMREAD_COLOR) # Decodes numpy array of encoded JPEG image to OpenCV image matrix. 
        img = cv.rotate(img, self.rotation) # Rotates image. 
        self.img = img 
    
    def display(self): 
    # Function for displaying captured frames. 
        cv.namedWindow('OpenMV H7 Camera', cv.WINDOW_NORMAL) # Defines new OpenCV window. 
        cv.imshow('OpenMV H7 Camera', self.img) # Displays captured image. 
        cv.waitKey(1) # Necessary for OpenCV to update window. 

    def dominant_colour(self, normalize_components=False, decimals=2, max_component=False): 
    # Function for calculating the dominant colour of a frame. 
        data = self.img
        data = data.reshape((-1, 3)).astype(np.float32)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, _, center = cv.kmeans(data, 1, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
        center = center[0].astype(int)[::-1] # Reorder vector to RGB since OpenCV uses BGR. 
        r, g, b = center
        if not max_component: # Return a dictionary with RGB values. 
            if normalize_components: # Normalizes based on fraction that each component (RGB) makes up of total colour. 
                sum = r + g + b
                if sum == 0: 
                    return [0, 0, 0]
                r = round(float(r / sum), decimals)
                g = round(float(g / sum), decimals)
                b = round(float(b / sum), decimals)
            rgb = dict(zip(("RED", "GREEN", "BLUE"), (r, g, b)))
            return rgb
        if max_component: # Return the most prominent component (red, green, or blue). 
            rgb = dict(zip(("Red", "Green", "Blue"), (r, g, b)))
            return max(rgb, key=rgb.get)
    
    def detect_shapes(self, draw_on_img=True): 
    # Function for detecting/identifying shapes (triangles, squares, circles). 
        grayed = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY) # Convert to grayscale for Canny edge algorithm. 
        blurred = cv.GaussianBlur(grayed, (5, 5), 0) # Use Gaussian blur to reduce noisy edges. 
        edged = cv.Canny(blurred, 100, 150) # Convert to Canny edge images (only edges are black, everything else is white). 
        contours, _ = cv.findContours(edged, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE) # Finds boundaries from the black/white Canny image. 
        shape = 'Unknown'
        try: # Necessary because max() causes error if the contours list is empty. 
            contour = max(contours, key=cv.contourArea) # Only look at the largest contour/shape seen by the camera. 
            perimeter = cv.arcLength(contour, True) # Calculates the arc length perimeter of the shape. 
            approximation = cv.approxPolyDP(contour, 0.02 * perimeter, True) # Approximates contour to polygon with less vertices. 
            vertices = len(approximation)
            if vertices == 3: 
                shape = "Triangle"
            elif vertices == 4: 
                shape = "Rectangle"
            elif vertices >= 5: 
                shape = "Circle"
            if draw_on_img:
                cv.drawContours(self.img, [approximation], -1, (0, 255, 0), 2) # Draws shape outline onto captured image. 
            return shape
        except: 
            return shape
        
camera = CameraStream(port='COM4', baudrate=115200, rotation=0)
while True: 
    camera.capture()
    shape = camera.detect_shapes()
    print(shape)
    camera.display()
