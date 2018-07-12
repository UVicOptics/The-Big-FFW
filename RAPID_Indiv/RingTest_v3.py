##########################################################
##########################################################
#  Farbod Jahandar -- Last update: Feb - 2018
#  Univeristy of Victoria
#  contact: farbodj@uvic.ca, farbod.jahandar@gmail.com
#
#  Please find the references section after the last part
#  of the script for more details.
##########################################################
##########################################################





#
#The following libraries are essential for image post-processing
#

from tkinter import *
from tkinter import ttk

import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import *
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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

from Displayer_v3 import disp, slice, peakfinder, fwhm_shower, calibrate, comparison, all_analyzer, Center_Finder, SF_Finder


##################################################
# The following functions, uses different functions
# in Displayer.py in order to do the needed calculation
# or determinations for each buttun
##################################################


def command1(*args):
    try:
        value0 = str(name.get())
        value1 = int(size1.get())
        value2 = int(size2.get())
        value3 = int(angle.get())
        result1.set(disp(value0,value1,value2,value3))


    except ValueError:
        pass

def command2(*args):
    try:
        value0 = str(name.get())
        value1 = int(size1.get())
        value2 = int(size2.get())
        value3 = int(angle.get())
        result2.set(slice(value0,value1,value2,value3))


    except ValueError:
        pass

def command3(*args):
    try:
        value0 = str(name.get())
        value1 = int(size1.get())
        value2 = int(size2.get())
        value3 = int(angle.get())
        value4 = int(S_Factor.get())
        result3.set(peakfinder(value0,value1,value2,value3,value4))


    except ValueError:
        pass


def command4(*args):
    try:
        value0 = str(name.get())
        value1 = int(size1.get())
        value2 = int(size2.get())
        value3 = int(angle.get())
        value4 = int(S_Factor.get())
        result4.set(fwhm_shower(value0,value1,value2,value3,value4))


    except ValueError:
        pass


def command5(*args):
    try:
        value0 = str(name.get())
        value1 = int(size1.get())
        value2 = int(size2.get())
        value3 = int(Angle_Num.get())
        value4 = int(S_Factor.get())
        result5.set(calibrate(value0,value1,value2,value3,value4))


    except ValueError:
        pass


def command6(*args):
    try:
        value0 = str(name.get())
        value1 = int(size1.get())
        value2 = int(size2.get())
        value3 = int(angle.get())
        value4 = int(S_Factor.get())
        result6.set(comparison(value0,value1,value2,value3,value4))


    except ValueError:
        pass


def command7(*args):
    try:
        value0 = str(name.get())
        value1 = int(size1.get())
        value2 = int(size2.get())
        value3 = int(S_Factor.get())
        result7.set(all_analyzer(value0,value1,value2,value3))


    except ValueError:
        pass



def command8(*args):
    try:
        value0 = str(name.get())
        result8.set(Center_Finder(value0))


    except ValueError:
        pass



def command9(*args):
    try:
        value0 = str(name.get())
        value1 = int(size1.get())
        value2 = int(size2.get())
        value3 = int(angle.get())
        value4 = int(S_Factor.get())
        result9.set(SF_Finder(value0,value1,value2,value3,value4))


    except ValueError:
        pass




##################################################
# The following scripts will define the input window
# (i.e. its size in pixels, its color etc...) 
##################################################


    
root = Tk()
root.title("Ring Test")


root.geometry('1050x450')
root.configure(bg='#008000')
#root.configure(bg='#857436')
#root.configure(bg='#457970')

mainframe = ttk.Frame(root,style='My.TFrame')
mainframe.grid(column=1, row=1)#, sticky=(N, W, E, S))

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)


##################################################
# Defining type of each variable
##################################################


name = StringVar()
size1 = StringVar()
size2 = StringVar()
angle = StringVar()
Angle_Num = StringVar()
S_Factor = StringVar()
result1 = StringVar()
result2 = StringVar()
result3 = StringVar()
result4 = StringVar()
result5 = StringVar()
result6 = StringVar()
result7 = StringVar()
result8 = StringVar()
result9 = StringVar()


##################################################
# The following generates space for each entry
##################################################


name_entry = ttk.Entry(mainframe, width=7, textvariable=name)
name_entry.grid(column=2, row=2, sticky=(W, E))

size1_entry = ttk.Entry(mainframe, width=7, textvariable=size1)
size1_entry.grid(column=2, row=3, sticky=(W, E))

size2_entry = ttk.Entry(mainframe, width=7, textvariable=size2)
size2_entry.grid(column=2, row=4, sticky=(W, E))
'''
S_Factor_entry = ttk.Entry(mainframe, width=7, textvariable=S_Factor)
S_Factor_entry.grid(column=2, row=5, sticky=(W, E))
'''
angle_entry = ttk.Entry(mainframe, width=7, textvariable=angle)
angle_entry.grid(column=2, row=7, sticky=(W, E))

Angle_Num_entry = ttk.Entry(mainframe, width=7, textvariable=Angle_Num)
Angle_Num_entry.grid(column=2, row=8, sticky=(W, E))



##################################################
# The following generates each button for each function
##################################################

#ttk.Button(mainframe, text="Find centre of the circle!", style='My.TButton',command=command8).grid(column=5, row=1, sticky=W)
ttk.Button(mainframe, text="Display", style='My.TButton',command=command1).grid(column=5, row=2, sticky=W)
ttk.Button(mainframe, text="Slice", style='My.TButton',command=command2).grid(column=5, row=3, sticky=W)
ttk.Button(mainframe, text="Comparison", style='My.TButton',command=command6).grid(column=5, row=4, sticky=W)
#ttk.Button(mainframe, text="SF Finder", style='My.TButton',command=command9).grid(column=5, row=6, sticky=W)
ttk.Button(mainframe, text="Peak Finder", style='My.TButton',command=command3).grid(column=5, row=7, sticky=W)
ttk.Button(mainframe, text="FWHM,Radius,FRD Finder", style='My.TButton',command=command4).grid(column=5, row=8, sticky=W)
ttk.Button(mainframe, text="Calibrate - FWHM,Radius,FRD Finder", style='My.TButton',command=command5).grid(column=5, row=9, sticky=W)
ttk.Button(mainframe, text="Show All", style='My.TButton',command=command7).grid(column=5, row=10, sticky=W)

##################################################
# The following generates labels for each empty box
##################################################

ttk.Label(mainframe, textvariable=result8).grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Name").grid(column=3, row=2, sticky=W)
ttk.Label(mainframe, text="Dim 1 (use the second dimension from above -10 pix)").grid(column=3, row=3, sticky=W)
ttk.Label(mainframe, text="Dim 2 (use the second dimension from above +10 pix)").grid(column=3, row=4, sticky=W)
#ttk.Label(mainframe, text="Smoothing Factor (this value will be added or subtracted from default value of 20)").grid(column=3, row=5, sticky=W)
#ttk.Label(mainframe, textvariable=result9).grid(column=3, row=6, sticky=W)
ttk.Label(mainframe, text="Angle").grid(column=3, row=7, sticky=W)
ttk.Label(mainframe, text="Angle_Num").grid(column=3, row=8, sticky=W)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

size1_entry.focus()


root.bind('<Return>', command1)

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



