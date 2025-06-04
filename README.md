# OpenMV Camera Without Using OpenMV IDE

Using these scripts, you can capture images and video on your Windows PC from an OpenMV H7 camera, without using OpenMV IDE. 

## Installing script on OpenMV camera
1. Start by copying one of the `OpenMV_USB.py` or `OpenMV_USB_No_LED.py` files to the your OpenMV camera, which should be visible in the file explorer.
2. Wait approximately 10 seconds. 
3. Unplug the camera.
4. Reconnect the camera, and make sure the updated file is still in the OpenMV camera's filesystem.

## Running the scripts on your PC
1. Make sure the pyserial and OpenCV libraries are both installed in your Python Environment. 
2. Open `Capture_Single_Image.py` or `Capture_Video.py` or `Stream_Video.py` in a code editor or terminal.
3. Look in the Windows Device Manager for the OpebCV camera listed as "USB Serial Device (COM#)". Enter "COM#" as the value of `PORT`.
4. Create a folder for images to be stored in the same working directory as the scripts. Enter the path as the value of `PATH`. 
