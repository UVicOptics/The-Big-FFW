#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 16:57:15 2018

##########################################################
##########################################################
#  UVic's FiTS Team (Stephanie Monty, Farbod Jahandar and Jooyoung Lee) -- Last update: April - 2018
#  Univeristy of Victoria
#  contact info:
#  Stephanie Monty <montys@uvic.ca>
#  Farbod Jahandar <farbodj@uvic.ca>, <farbod.jahandar@gmail.com>
#  Jooyoung Lee <leejy0028@gmail.com>
#  Please find the references section after the last part
#  of the script for more details.
##########################################################
##########################################################
"""
from Camera import CameraCode
from Stage import StageCode
from Rapid import RapidCode
import os
import numpy as np


class BigFFW:
    
    ##########################################################
    # This main function calls the individual classes for the
    # different components of the Big FFW flowchart.
    # 
    # It calls the three components once to initialize the stage
    # to position 0 then loops through the flowchart for all the
    # images in the user-specified list.
    #
    # 
    ##########################################################
    
    def main(self, angle_list, rot_angle, gain, n_images, image_path, output_path):
        
        #Remove the user entered commas in the list of angles           
#        angle_list = [ang for ang in angle_list if ang != ","]
        angle_list = [ang for ang in angle_list]
                
                
        
        camera = CameraCode()
        stage = StageCode()
        rapid = RapidCode()
        
        #This command ensures the .dll file that is required by the PI
        #controller is in the same directory as the stage code
        cwd = os.getcwd()
        
        #Connects the stage only once and saves the connected device info
        pi_device = stage.connect()
        stage.main(pi_device, angle_list[0])
        
        camera.main(gain, n_images, angle_list[0], image_path)
        
        
        for num in range(1, len(angle_list)):
            #Changes the directory back to the location of the .dll file
            #before callign stage code.
            os.chdir(cwd)
            stage.main(pi_device, angle_list[num])
            camera.main(gain, n_images, angle_list[num], image_path)
        
        rapid.main(image_path, output_path, rot_angle)
            
        print ("Completed!, Your results can be found in %s" % (output_path))
        
        #Change back to the directory where the *.dll file is
        os.chdir(cwd)
        #Move the stage back to zero
        stage.main(pi_device, 0)# (-1 * int(angle_list[len(angle_list) - 1])))
        
if __name__ == "__main__":
    B = BigFFW()
    B.main() 
        
        
        
