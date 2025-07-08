### Created by Simon Wong while working at BLINC Lab. 
### Updated June 13, 2025. 

import serial
import struct
import cv2 as cv
import numpy as np

class CameraStream: 
    def __init__(self, port='COM5', baudrate=115200, rotation=0, **kwargs): 
        self.use_webcam = kwargs.get('use_webcam', False)
        if self.use_webcam: 
            self.camera = cv.VideoCapture(0)
            self.camera.isOpened()
        else: 
            self.serial_port = serial.Serial(port, 
                                            baudrate=baudrate, 
                                            bytesize=serial.EIGHTBITS, 
                                            parity=serial.PARITY_NONE, 
                                            xonxoff=False, 
                                            rtscts=False, 
                                            stopbits=serial.STOPBITS_ONE, 
                                            timeout=None, 
                                            dsrdtr=True)
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
        if self.use_webcam: 
            _, img = self.camera.read()
        else: 
            self.serial_port.setDTR(True)
            self.serial_port.write(b'snap')
            self.serial_port.flush()
            size = struct.unpack('<L', self.serial_port.read(4))[0]
            img = self.serial_port.read(size)
        img = np.frombuffer(img, dtype=np.uint8)
        img = cv.imdecode(img, cv.IMREAD_COLOR)
        img = cv.rotate(img, self.rotation) # Something goes wrong when rotation not 0, fuzzy purple/green screen. 
        self.img = img
    
    def display(self): 
        cv.namedWindow('OpenMV H7 Camera', cv.WINDOW_NORMAL)
        cv.imshow('OpenMV H7 Camera', self.img)
        cv.waitKey(1) 

    def dominant_colour(self, normalize_components=False, decimals=2, max_component=False): 
        data = self.img
        data = data.reshape((-1, 3)).astype(np.float32)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, _, center = cv.kmeans(data, 1, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
        center = center[0].astype(int)[::-1] # Reorder vector to RGB since OpenCV uses BGR. 
        r, g, b = center
        if not max_component: 
            if normalize_components: # Normalizes based on fraction that each component (RGB) makes up of total colour. 
                sum = r + g + b
                if sum == 0: 
                    return [0, 0, 0]
                r = round(float(r / sum), decimals)
                g = round(float(g / sum), decimals)
                b = round(float(b / sum), decimals)
            rgb = dict(zip(("RED", "GREEN", "BLUE"), (r, g, b)))
            return rgb
        if max_component: 
            rgb = dict(zip(("Red", "Green", "Blue"), (r, g, b)))
            return max(rgb, key=rgb.get)
    
    def detect_shapes(self): 
        grayed = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(grayed, (5, 5), 0) # Gaussian kernel size. 
        edged = cv.Canny(blurred, 100, 150) # Lower and upper Canny thresholds. 
        contours, _ = cv.findContours(edged, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        shape = 'Unknown'
        try: 
            contour = max(contours, key=cv.contourArea)
            perimeter = cv.arcLength(contour, True)
            approximation = cv.approxPolyDP(contour, 0.02 * perimeter, True) # Second parameter is approximation accuracy.
            vertices = len(approximation)
            if vertices == 3: 
                shape = "Triangle"
            elif vertices == 4: 
                shape = "Rectangle"
            elif vertices >= 5: 
                shape = "Circle"
            cv.drawContours(self.img, [approximation], -1, (0, 255, 0), 2)
            return shape
        except: 
            return shape
        
camera = CameraStream(port='COM4', baudrate=115200, rotation=0, use_webcam=False)
while True: 
    camera.capture()
    shape = camera.detect_shapes()
    print(shape)
    camera.display()
