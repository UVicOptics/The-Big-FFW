# The Big FFW
This system allows for the testing of optical fibres for a fully automated optomechanical test facility. Each fibres are individually tested using the ring test method.

 
They have been tested with python-2.7, some dependencies are not python-3 ready yet.

## Required packages:

- matplotlib
- numpy
- sys
- PIL
- os
- Tkinter
- ttk
- subprocess
- skimage
- cv2
- astropy
- scipy
- pylab
- lmfit
- random
- imutils
- PyCapture2 (for FLIR cameras)
- time
- pipython (for PI controller)


This software is compatible with Linux (preferred Ubuntu), Mac OS (10.11<, preferred High Sierra) and Windows (preferred Windows 10)

All those packages can be installed with Pip.

```
pip install <package>...<package>
```
If you have the Python anaconda distribution, you can (except for `vos`) also install the packages not already installed with
```
conda install <package>...<package>
```

Note: You can install Pip on Windows with:

```
curl https://bootstrap.pypa.io/ez_setup.py | python
```
```
curl https://bootstrap.pypa.io/get-pip.py | python
```

You can then clone this repository:
```
git clone https://github.com/UVicOptics/The-Big-FFW.git
cd The-Big-FFW
```

## Hardware:

- An optical fibre
- Pointgrey Camera
-- Specs: 
--- Model: Grasshoper 2
--- Resolution 2448 x 2048
--- Megapixels: 5.0 MP

![](Camera.png=600x600)

- PC (with an appropriate operating systemm)
- Source of light (ideally an LED)
- A collimator
- Multiple mounts and rotating stages

- PI MicroController

 
# The big FFW GUI:

![](GUI.jpg)
.
.
.
.
.
.
Below is a description of the built-in layers of the Big FFW:

![](FFW.jpg)
.
.
.
.
.
.
.

- FiTS Analyzer
- Stage Code
- Camera Code
- RAPID
Ring Analyzer Python Interface for ring-test Data (RAPID)
  
  
# RAPID
Ring Analyzer Python Interface for ring-test Data (RAPID)
 
 # Motivation
 Ring test analysis is an essential way of checking efficiency and quality of optical fibers but the process can be very time consuming. By RAPID graphical user interface, you can analyze and visualize the output ring images of the fiber by only inputting the output image of the test.
 



# There are 5 variables in the main page of the interface:
* Name = Name of the image file

* Dim1 and Dim2 = The x and y dimensions that cover the diameter of the circle [for the test data in "All" directory, you can use 600 pix and 610 pix to cover the diameter]

* Angle = Rotates the input image with respect to the angle the user enters

* Angle_Num = Rotates the image this many times with respect to the random angles

# There are 7 functions in the main page of the interface:
* Display: Displays the input image as a whole and also a slice of it based on the Dim1 and Dim2 values.

* Slice: Plots Intensity Vs Pixel number graph based in the chosen slice (from Dim1 and Dim2).

* Comparison: Compares the raw data with the smoothed version of it.

* Peak Finer: Finds peaks of the plot generated from Slice functions.

* FWHM, Diameter, FRD Finder: Determines the diameter of the circle (in pixels), fits a spline polynomial to the gaussians and calculates the Full Width Half Maximum (FWHM) and also the Focal Ratio Degradation (FRD) of the ring. 

* Calibrate - FWHM, Radius, FRD Finder: Rotates the image several times with random angles and determines FWHM, Diameter and FRD Finder of the system (this time with standard deviation from several measurments).

* Show All - Determines FRD of multiple rings in multiple files and plots a graph of FRD Vs angle of all rings (note that for this function, name of the directory should be entered in the corresponding space).

# Run the code
         -python RingTest.py

# Output

![](Fig0.png)

* Different functions are as following:

"Display":

![](FIG1.png)

![](FIG2.png)

"Slice":

![](FIG3.png)

"Comparison":

![](FIG4.png)

"Peak Finder":

![](FIG5.png)

"FWHM, Radius, FRD Finder":

![](FIG6.png)

"Calibrate - FWHM, Radius, FRD Finder":

![](FIG7.png)

"Show All":

![](fig8.png)

