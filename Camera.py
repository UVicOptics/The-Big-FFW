"""

@author: farbodj

Big FFW Code Version 1

TODO: Change the size of the image to allow for angles > 10 degrees

---------------
| Camera Code |
---------------

This is the camera code to be called by both the Calibration and BigFFW in order
to collect images to calibrate the exposure time and to capture the final science
images for use by Rapid.

The inputs and outputs are as follows:
Input:
1) float gain
2) int n images
3) int input angle
4) string image path to save the image
    

Output:
1) saved image(s)

"""

import PyCapture2
from sys import exit
import time
import os


class CameraCode:
    
    """
    Default mode is automatic exposure time selection (within the FlyCapture program)
    If you'd like to control the exposure time then uncomment the commented lines
    below.
    """
    
    def main(self, gain, n_images, input_angle, image_path):
    #def main(self, exp_time, gain, n_images):
        self.gain = gain
        self.n_images = n_images
        self.image_path = image_path
        self.input_angle = input_angle
        self.pause_time = 3
        #self.exp_time = exp_time

        self.capture()
        

    def capture(self):
        bus = PyCapture2.BusManager()
        cam = PyCapture2.Camera()
        maxWidth = 2448
        maxHeight = 2048
         
        cam.connect(bus.getCameraFromIndex(0))
        #cam.setProperty(type = PyCapture2.PROPERTY_TYPE.AUTO_EXPOSURE, absValue = self.exp_time)
        cam.setProperty(type = PyCapture2.PROPERTY_TYPE.GAIN, absValue = self.gain)
        fmt7imgSet = PyCapture2.Format7ImageSettings(0, 0, 0, maxWidth, maxHeight, 
                                                     PyCapture2.PIXEL_FORMAT.MONO8) 
        fmt7pktInf, isValid = cam.validateFormat7Settings(fmt7imgSet)
        
        if not isValid: 	
            print ("Format7 settings are not valid!")	
            exit()      
            
        cam.setFormat7ConfigurationPacket(fmt7pktInf.recommendedBytesPerPacket, fmt7imgSet)
        
        cam.startCapture()
         
        for i in range(self.n_images):
            self.grabImages(cam)
            
            
            for filename in os.listdir("."):
                print (filename)
                if filename.startswith("fc2"):
                    os.rename(filename,"{}.{}.tif".format(self.input_angle, i))  
        
                
        cam.stopCapture()
        
    
    def grabImages(self, cam):
        time.sleep(self.pause_time)
        
        try:
            image = cam.retrieveBuffer()
           
        except PyCapture2.Fc2error as fc2Err:
            print ("Error retrieving buffer : ", fc2Err)
    

        print ("Saving the last image to fc2CustomImageEx.tif")
        os.chdir(self.image_path)
        image.save("fc2CustomImageEx.tif", PyCapture2.IMAGE_FILE_FORMAT.TIFF)
    

if __name__ == "__main__":
    X = CameraCode()
    X.main()
