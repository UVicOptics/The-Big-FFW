#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This example helps you to get used to PIPython."""

from random import uniform

from pipython import GCSDevice, pitools

import sys


CONTROLLERNAME = 'C-863.11'
STAGES = ('M-037.DG1',)  # connect stages to axes
REFMODE = ('POS',)  # reference the connected stages


class StageCode:
            
    def main(self, pi_device, input_angle):
        self.input_angle = input_angle
        self.pidevice = pi_device
    
        self.compute()
        

    def connect(self):
        """Connect, setup system and move stages and display the positions in a loop."""
        self.pidevice = GCSDevice(CONTROLLERNAME)

        self.pidevice.ConnectUSB(serialnum='0145500270') #Serial number is not identical, check your connection.
        print('connected: {}'.format(self.pidevice.qIDN().strip()))
        if self.pidevice.HasqVER(): #Checking the version of PI controller. 
            print('version info: {}'.format(self.pidevice.qVER().strip()))

        print('initialize connected stages...')
        pitools.startup(self.pidevice, stages=STAGES)

        self.pidevice.SVO(self.pidevice.axes,1) #SVO is servo ON for a controller
        self.pidevice.VEL(self.pidevice.axes,3) #VEL is a velocity of a motor
        self.pidevice.RON(self.pidevice.axes,0) #RON is a reference mode, 0 means off.
        self.pidevice.POS(self.pidevice.axes,0) #POS is abolute position, when the stage is connected, the 
        positions = self.pidevice.qPOS(self.pidevice.axes)
        
        for axis in self.pidevice.axes:
            print('position of axis {} = {:.2f}'.format(axis, positions[axis]))
            print('stage connected')
        
        return self.pidevice

    def compute(self):
        #Move the number of steps equal to the difference between the initial position
        #and the desired final position
        self.pidevice.MOV(self.pidevice.axes, int(self.input_angle))
        print('stage moves to target position')
        pitools.waitontarget(self.pidevice)
    

if __name__ == '__main__':
    # To see what is going on in the background you can remove the following
    # two hashtags. Then debug messages are shown. This can be helpful if
    # there are any issues.

    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    X = StageCode()
    X.main()
