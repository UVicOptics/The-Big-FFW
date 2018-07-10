##########################################################
##########################################################
#  UVic's FiTS Team (Farbod Jahandar, Stephanie Monty and Jooyoung Lee) -- Last update: April - 2018
#  Univeristy of Victoria
#  contact info:
#  Farbod Jahandar <farbodj@uvic.ca>, <farbod.jahandar@gmail.com>
#  Stephanie Monty <montys@uvic.ca>
#  Jooyoung Lee <jylee928@uvic.ca>
#  Please find the references section after the last part
#  of the script for more details.
##########################################################
##########################################################





#
#The following libraries are essential for image post-processing
#

from Tkinter import *
import ttk

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import *
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import sys

from PIL import ImageTk, Image
import os 
import Tkinter as tk
from PIL import ImageTk, Image
from matplotlib.figure import Figure
import sys
import subprocess

###
# The following code imports required functions from Displayer.py
###

from Big_FFW import BigFFW

'''
from Displayer_v3 import disp, slice, peakfinder, fwhm_shower, calibrate, comparison, all_analyzer, Center_Finder, SF_Finder
from CC import printBuildInfo as PyCapVersion
from CC import CameraV as CameraVersion
from CC import Capture
'''



##################################################
# The following functions, uses different functions
# in Displayer.py in order to do the needed calculation
# or determinations for each buttun
##################################################


def command1(*args):
    BFFW = BigFFW()
    value1_2=[]
    value1_4=[]
    Uvalue1=[]
    value1_1=[]
    value1_3=[]
    try:
        value1 = list(list_angles.get())
        value2 = int(rot_angles.get())
        value3 = int(gain.get())
        value4 = int(n_images.get())
        value5 = "\Users\UVIC\Desktop\Test\Images"#str(image_path.get())
        value6 = "\Users\UVIC\Desktop\Test\Results"#str(output_path.get())
        for i in range(len(value1)-1):
            if value1[i] != "," and value1[i+1] !=",":
                value1_1 = int(value1[i+1])+10
            value1_2.append(value1_1)
        for i in range(len(value1)-1):
            if value1[i] != "," and value1[i+1] == ",":
                value1_3 = int(value1[i])
            value1_4.append(value1_3)        
        value1_f = np.concatenate((value1_2,value1_4))
        for x in value1_f:
            if x not in Uvalue1 and x>0:
                Uvalue1.append(x)
        Sort = sorted(Uvalue1)
        Final = [x for x in Sort if x != []]
#        result1.set(BFFW.main(value1,value2,value3,value4,value5,value6))
        result1.set(BFFW.main(Final,value2,value3,value4,value5,value6))
    except ValueError:
        pass




##################################################
# The following scripts will define the input window
# (i.e. its size in pixels, its color etc...) 
##################################################


    
root = Tk()
root.title("Camera Controller")


#root.geometry('1050x450')
#root.geometry('1398x600')
root.geometry('1440x900')
#root.configure(bg='#008000')
#root.configure(bg='#857436')
#root.configure(bg='#357970')
root.configure(bg='#104E8B')

mainframe = ttk.Frame(root,style='My.TFrame')
mainframe.grid(column=1, row=1)#, sticky=(N, W, E, S))

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)



path = "Logo.jpg"
path2 = "Logo2.jpg"
#img = ImageTk.PhotoImage(Image.open(path))
#panel = tk.Label(root, image = img)
#panel.pack(side = "bottom", fill = "both", expand = "no")

#img2 = ImageTk.PhotoImage(Image.open(path2))
#panel = tk.Label(root, image = img2)
#panel.pack(side = "top", fill = "both", expand = "no")

##################################################
# Defining type of each variable
##################################################


#exp = StringVar()
#gain = StringVar()


list_angles = StringVar()
rot_angles = StringVar()
gain = StringVar()
n_images = StringVar()
image_path = StringVar()
output_path = StringVar()


result1 = StringVar()


##################################################
# The following generates space for each entry
##################################################


list_angles_entry = ttk.Entry(mainframe, width=7, textvariable=list_angles)
list_angles_entry.grid(column=2, row=1, sticky=(W, E))

rot_angles_entry = ttk.Entry(mainframe, width=7, textvariable=rot_angles)
rot_angles_entry.grid(column=2, row=2, sticky=(W, E))

gain_entry = ttk.Entry(mainframe, width=7, textvariable=gain)
gain_entry.grid(column=2, row=3, sticky=(W, E))

n_images_entry = ttk.Entry(mainframe, width=7, textvariable=n_images)
n_images_entry.grid(column=2, row=4, sticky=(W, E))

image_path_entry = ttk.Entry(mainframe, width=7, textvariable=image_path)
image_path_entry.grid(column=2, row=5, sticky=(W, E))

output_path_entry = ttk.Entry(mainframe, width=7, textvariable=output_path)
output_path_entry.grid(column=2, row=6, sticky=(W, E))



##################################################
# The following generates each button for each function
##################################################

ttk.Button(mainframe, text="RUN!", style='My.TButton',command=command1).grid(column=5, row=1, sticky=W)
#ttk.Button(mainframe, text="Where to save the image?", style='My.TButton',command=command2).grid(column=5, row=2, sticky=W)
#ttk.Button(mainframe, text="Live Feed?", style='My.TButton',command=command3).grid(column=5, row=3, sticky=W)


##################################################
# The following generates labels for each empty box
##################################################


#ttk.Label(mainframe, text="Take a picture!").grid(column=3, row=2, sticky=W)

#ttk.Label(mainframe, textvariable=result1).grid(column=3, row=1, sticky=W)
#ttk.Label(mainframe, textvariable=result2).grid(column=3, row=2, sticky=W)
ttk.Label(mainframe, text="Degree Range").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Rotational angles").grid(column=3, row=2, sticky=W)
ttk.Label(mainframe, text="Gain").grid(column=3, row=3, sticky=W)
ttk.Label(mainframe, text="Number of Images").grid(column=3, row=4, sticky=W)
ttk.Label(mainframe, text="Image path").grid(column=3, row=5, sticky=W)
ttk.Label(mainframe, text="Output path").grid(column=3, row=6, sticky=W)
#ttk.Label(mainframe, text="Enter the gain value").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#size1_entry.focus()


#root.bind('<Return>', command1)

root.mainloop()

##  end



#######################################
#
#
#REFERENCES
#
#
#######################################
#
# The general structure of this python script is influenced  http://www.tkdocs.com/tutorial/firstexample.html
#
#######################################



