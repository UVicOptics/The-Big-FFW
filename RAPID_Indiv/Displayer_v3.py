##########################################################
##########################################################
#  Farbod Jahandar -- Last update: Feb - 2018
#  Univeristy of Victoria
#  contact: farbodj@uvic.ca, farbod.jahandar@gmail.com
#
#  Displayer python scripts to run RingTest.py
#  Please find the references section after the last part
#  of the script for more details.
##########################################################
##########################################################





#The following libraries are essential for image post-processing


from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from skimage import data, color
from skimage.transform import hough_circle
from skimage.feature import peak_local_max, canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage.io import imread
import os
import cv2
from astropy.convolution import convolve, Box1DKernel
from scipy.interpolate import UnivariateSpline
import pylab as plb
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from lmfit import Model
import numpy as np
from scipy.signal import find_peaks_cwt
from scipy import signal
from pylab import *
import sys
import Tkinter as Tk
from scipy.interpolate import splrep, sproot, splev
from random import randint
import cv2
import imutils
import scipy.interpolate as interp

datadir="All/"
filename = os.listdir(datadir)


##########################################################
# The following funtion find centre of the input shape (i.e. circle)
# and the values can be used for Dim1 and Dim2 values 
##########################################################


def Center_Finder(x):

    image = x

    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# loop over the contours
    for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])

	# draw the contour and center of the shape on the image
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
	cv2.putText(image, "center", (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	return cX,"pix","x", cY,"pix" # -- for Dim 1 and 2 use ", cY, "+/- 10 pix"
	# show the image
#	cv2.imshow("Image", image)
	plt.imshow(image, cmap=plt.cm.coolwarm)
#	cv2.waitKey(0)
	plt.show()


##########################################################
# The following funtion takes four variables, x=name of the image
# size 1 and 2 are for choosing a slice of the image
# angle = orientation of the image; if 0, the original image
# will be analyzed; if not 0, the original image will be rotated
# with respect to the given angle.
##########################################################



def disp(x,size1,size2,angle):

    img = plt.imread(str(x))
    ang=[]
    rows,cols = img.shape

    if angle==0:
            ang=1
    else:
            ang=angle

    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    rot = cv2.warpAffine(img,M,(cols,rows))


    Image = rot[size1:size2] 
    plt.imshow(rot, cmap=plt.cm.coolwarm)

    plt.figure()

    plt.imshow(Image, cmap=plt.cm.coolwarm)
    plt.show()





##########################################################
# The following funtion is for displaying the input image 
# of the ring and it takes four variables, x=name of the
# image size 1 and 2 are for choosing a slice of the image
# angle = orientation of the image; if 0, the original image
# will be analyzed; if not 0, the original image will be rotated
# with respect to the given angle.
##########################################################



def slice(x,size1,size2,angle):
  
        img = plt.imread(str(x))
        ang=[]
        rows,cols = img.shape
        if angle==0:
            ang=1
        else:
            ang=angle

        M = cv2.getRotationMatrix2D((cols/2,rows/2),ang,1)
        rot = cv2.warpAffine(img,M,(cols,rows))

        Image = rot[size1:size2] 

	index = []
	index_s = []
	intensity = []

        x = [0,200,400,600,800,1000,1200]


        for i in range(len(Image)):
             for j in range(0,6):
                 if np.mean(Image[i][x[j]:x[j+1]]) >30:
                     index = i
                     index_s.append(index)
                     intensity.append(Image[i][x[j]:x[j+1]])


	fig = plt.figure()
	for i in index_s:
	    plt.plot(Image[i])
	fig.show()
	Tk.mainloop()


##########################################################
# The following funtion is for finding peaks in the chosen
# slice of the ring. The input and it takes four variables,
# x=name of the image size 1 and 2 are for choosing a slice
# of the image. angle = orientation of the image; if 0, the
# original image will be analyzed; if not 0, the original image
# will be rotated with respect to the given angle. Peak finder
# is useful for finding diameter of the ring.
##########################################################



def peakfinder(x,size1,size2,angle,S_Factor):

        img = plt.imread(str(x))
        ang=[]
        rows,cols = img.shape
        if angle==0:
            ang=1
        else:
            ang=angle

        M = cv2.getRotationMatrix2D((cols/2,rows/2),ang,1)
        rot = cv2.warpAffine(img,M,(cols,rows))

        Image = rot[size1:size2] 

	

	smoothed_S = convolve(Image[0], Box1DKernel(20+S_Factor))
	peakind = signal.find_peaks_cwt(smoothed_S, np.arange(50,150))



	fig = plt.figure()
	plt.plot(smoothed_S)
	plt.plot(np.array(range(len(smoothed_S)))[peakind], smoothed_S[peakind],'o')
	#plt.show

	fig.show()
	Tk.mainloop()


##########################################################
# The following funtion is for determining the FWHM of
# any gaussian-like data. It takes two variables, x=x axis
# of the file and y = y axis of the file.
# 
# After getting the data, it finds the best fit with respect 
# to a spline function and finds the roots of the system.
##########################################################




def fwhm(x, y, k=10):

    class MultiplePeaks(Exception): pass
    class NoPeaksFound(Exception): pass

    half_max = amax(y)/2.0
    s = splrep(x, y - half_max)
    roots = sproot(s)

    if len(roots) < 2:
        raise NoPeaksFound("No clear peaks were found in the image")
    else:
        return abs(roots[1] - roots[0]), roots[1], roots[0]
    
##########################################################
# The following funtion is for showing the fwhm position
# on the chosen slice of the ring. The input and it takes
# four variables, x=name of the image size 1 and 2 are for
# choosing a slice of the image. angle = orientation of the
# image; if 0, the original image will be analyzed; if not 0,
# the original image will be rotated with respect to the
# given angle. Peak finder is useful for finding diameter
# of the ring.
##########################################################


def fwhm_shower(x,size1,size2,angle,S_Factor):

    img = plt.imread(str(x))
    ang=[]
    rows,cols = img.shape
    if angle==0:
        ang=1
    else:
        ang=angle

    M = cv2.getRotationMatrix2D((cols/2,rows/2),ang,1)
    rot = cv2.warpAffine(img,M,(cols,rows))

    Image = rot[size1:size2] 

    smoothed_S = convolve(Image[0], Box1DKernel(20+S_Factor))
    peakind = signal.find_peaks_cwt(smoothed_S, np.arange(50,150))

#    C1=smoothed_S[300:700]
    C1 = smoothed_S
    X =range(len(C1)) 

    X=np.array(X)-10

    FWHM = fwhm(X, C1, k=10)

    F1 = FWHM[1]*1.2
    F2 = FWHM[2]*1.2

    DiffF = np.abs(F2 - F1)

    S1 = FWHM[1]*1.7
    S2 = FWHM[2]*1.7
 
    DiffS = np.abs(S2 - S1)


    j = []
    Peak = []
    for i in range(len(smoothed_S[peakind])):
    #    j=[]
         if smoothed_S[peakind][i]>50:
              j.append(i)

    k=[]
    Peak1Flux=[]
    Peak2Flux=[]
    Peak1=[]
    Peak2=[]

    Peak1Flux = sorted(smoothed_S[peakind],reverse=True)[0]
    Peak2Flux = sorted(smoothed_S[peakind],reverse=True)[1]
#    print peakind  

    S= [S1,S2]
    F= [F1,F2]
    Diameter = np.abs(np.where(smoothed_S == Peak1Flux)[0][0] - np.where(smoothed_S == Peak2Flux)[0][0])
#   Diameter = np.abs(np.array(range(len(smoothed_S)))[peakind][Peak1]-np.array(range(len(smoothed_S)))[peakind][Peak2])

    FRD = []
    e2 = np.abs(S[0]-S[1])
    FRD = e2/Diameter

#    X=np.array(X)-10
    fig = plt.figure()
    plot(X,C1)
    axvspan(FWHM[1], FWHM[2], facecolor='g', alpha=0.2)
    plt.text(2, 100, 'FRD='+str(np.round(FRD,3)))
    plt.text(2, 80, 'FWHM='+str(np.round(FWHM[0],3)))
    plt.text(2, 60, r'$\frac{1}{e}$' +'=' +   str(np.round(DiffF,3)))
    plt.text(2, 40, r'$\frac{1}{e^2}$' + '=' +   str(np.round(DiffS,3)))
    plt.text(2, 20, 'Diameter' + '=' +   str(np.round(Diameter,3)))

    fig.show()
    Tk.mainloop()

##########################################################
# The following funtion is for comparing the smooth version
# of the chosen splice with the raw image of it.
#
# Feel free to change the value of Box1DKernel(20) for different
# smoothing factors
##########################################################


def comparison(x,size1,size2,angle,S_Factor):

    img = plt.imread(str(x))
    ang=[]
    rows,cols = img.shape
    if angle==0:
        ang=1
    else:
        ang=angle

    M = cv2.getRotationMatrix2D((cols/2,rows/2),ang,1)
    rot = cv2.warpAffine(img,M,(cols,rows))

    Image = rot[size1:size2] 


    smoothed_S = convolve(Image[0], Box1DKernel(20+S_Factor))
    peakind = signal.find_peaks_cwt(smoothed_S, np.arange(50,150))

#    C1=smoothed_S[300:700]
#    C1=smoothed_S[300:490]
    C1 = smoothed_S
    X =range(len(C1)) 
    X2=range(len(C1))

    FWHM = fwhm(X, C1, k=10)

    F1 = FWHM[1]*1.2
    F2 = FWHM[2]*1.2

    DiffF = np.abs(F2 - F1)

    S1 = FWHM[1]*1.7
    S2 = FWHM[2]*1.7
 
    DiffS = np.abs(S2 - S1)


    j = []
    Peak = []
    for i in range(len(smoothed_S[peakind])):
    #    j=[]
         if smoothed_S[peakind][i]>50:
              j.append(i)

    k=[]
    Peak1Flux=[]
    Peak2Flux=[]
    Peak1=[]
    Peak2=[]

    Peak1Flux = sorted(smoothed_S[peakind],reverse=True)[0]
    Peak2Flux = sorted(smoothed_S[peakind],reverse=True)[1]

    S= [S1,S2]
    F= [F1,F2]
    Diameter = np.abs(np.where(smoothed_S == Peak1Flux)[0][0] - np.where(smoothed_S == Peak2Flux)[0][0])
   

    FRD = []
    e2 = np.abs(S[0]-S[1])
    FRD = e2/Diameter
    X2 = np.array(X2)-10
    fig = plt.figure()
#    plot(X2,C1)
#    plot(X,Image[0])
    x_axis = len(Image[0])
    x_axis_new = x_axis-10
    plot(C1)
#    plot(x_axis_new,C1)
    plot(Image[0])


    fig.show()
    Tk.mainloop()

##########################################################
# The following funtion is for increasing accuracy of the
# measured Diameter, FRD, FWHM etc... by multi-determination
# of them. For each ring, the system will choose a certain
# number of random angles (i.e. Angle_Num) and rotates the
# image based on that. Then for each rotated image, it 
# determines the Diameter, FRD, FWHM, etc... and finally it 
# gives the average of each + uncertainty for each case 
# which is the standard deviation of them. The function
# takes four variables, x=name of the image, size 1 and 2 are for
# choosing a slice of the image and Angle_Num is number of
# different angles for each ring.
##########################################################



def calibrate(x,size1,size2,Angle_Num,S_Factor):
    AllDiameter=[]
    FRD=[]
    AllFirstFWHM=[]
    AllSecondFWHM=[]
    OneOverE=[]
    OneOverE2=[]
    AllFinalFWHM=[]
    FinalAllFinalFWHM=[]
    C2=[]

    for i in range(Angle_Num):
	    img = plt.imread(str(x))
	    ang=[]
            angle = randint(0, 90)
	    rows,cols = img.shape
	    if angle==0:
	        ang=1
	    else:
	        ang=angle

	    M = cv2.getRotationMatrix2D((cols/2,rows/2),ang,1)
	    rot = cv2.warpAffine(img,M,(cols,rows))

	    Image = rot[size1:size2] 

	    index=[]
	    index_s=[]

	    step = [0,200,400,600,800,1000,1200]
	    for i in range(len(Image)):
	       for j in range(0,6):
	            if np.mean(Image[i][step[j]:step[j+1]]) >30:
	                     index = i
	                     index_s.append(index)

	    smoothed_S = convolve(Image[0], Box1DKernel(20+S_Factor))
	    peakind = signal.find_peaks_cwt(smoothed_S, np.arange(50,150))

#	    C1=smoothed_S[300:700]
	    C1=smoothed_S
	    X =range(len(C1)) 


	    FWHM = fwhm(X, C1, k=10)

	    F1 = FWHM[1]*1.2
	    F2 = FWHM[2]*1.2

	    DiffF = np.abs(F2 - F1)

	    S1 = FWHM[1]*1.7
	    S2 = FWHM[2]*1.7
 
	    DiffS = np.abs(S2 - S1)


	    j = []
	    Peak = []
	    for i in range(len(smoothed_S[peakind])):
	         if smoothed_S[peakind][i]>50:
	              j.append(i)

	    k=[]
	    Peak1Flux=[]
	    Peak2Flux=[]
	    Peak1=[]
	    Peak2=[]
            FinalFWHM=[]
	    Peak1Flux = sorted(smoothed_S[peakind],reverse=True)[0]
	    Peak2Flux = sorted(smoothed_S[peakind],reverse=True)[1]

	    S= [S1,S2]
	    F= [F1,F2]
            e2 = np.abs(S[0]-S[1])
            FinalFWHM = np.abs(FWHM[1] - FWHM[2])


	    Diameter = np.abs(np.where(smoothed_S == Peak1Flux)[0][0] - np.where(smoothed_S == Peak2Flux)[0][0])
            AllDiameter.append(Diameter)   
            AllFirstFWHM.append(FWHM[1])
            AllSecondFWHM.append(FWHM[2])
            FRD.append(e2/Diameter)
            OneOverE.append(np.round(DiffF,3))
            OneOverE2.append(np.round(DiffS,3))
            AllFinalFWHM.append(np.round(FinalFWHM,3))
            C2.append(C1)
            print angle

    X =range(400) 
    X=np.array(X)-10

    FinalAllDiameter = np.mean(AllDiameter)
    FinalAllDiameterStdev = np.std(AllDiameter)
    FinalAllFinalFWHM = np.mean(AllFinalFWHM)
    FinalAllFinalFWHMStdev = np.std(AllFinalFWHM)
    FinalAllFRD = np.mean(FRD)
    FinalAllFRDstd = np.std(FRD)
    FinalAllOneOverE = np.mean(OneOverE)
    FinalAllOneOverEstd = np.std(OneOverE)
    FinalAllOneOverE2 = np.mean(OneOverE2)
    FinalAllOneOverE2std = np.std(OneOverE2)

    fig = plt.figure()
#    plot(X,C2[0])
    plot(C2[0])
#    plt.text(2, 100, 'FRD='+str(np.round(FinalAllFRD,3))+ '+/-' +str(np.round(FinalAllFRDstd,3)))
    plt.text(2, len(C2[0])/10, 'FRD='+str(np.round(FinalAllFRD,3))+ '+/-' +str(np.round(FinalAllFRDstd,3)))
    plt.text(2, 80, 'FWHM='+str(np.round(FinalAllFinalFWHM,3))+ '+/-' +str(np.round(FinalAllFinalFWHMStdev,3)))
    plt.text(2, 60, r'$\frac{1}{e}$' +'=' +   str(np.round(FinalAllOneOverE,3))+ '+/-' +str(np.round(FinalAllOneOverEstd,3)))
    plt.text(2, 40, r'$\frac{1}{e^2}$' + '=' +   str(np.round(FinalAllOneOverE2,3))  + '+/-' +str(np.round(FinalAllOneOverE2std,3))  )
    plt.text(2, 20, 'Diameter' + '=' +   str(np.round(FinalAllDiameter,3)) + '+/-' +str(np.round(FinalAllDiameterStdev,3)))
    plt.xlabel("Pixels number")
    plt.ylabel("Intensity")


    fig.show()
    Tk.mainloop()


##########################################################
# The following funtion is for plotting FRD Vs Angle of
# multiple rings with different angles.
# Please note that the following code only determines FRD of
# each ring. In order to plot FRD Vs Angle, the angles of the
# rings should be added manually (automated way is reading the 
# angle from name of each file but this method requries a single
# format for name of the files. As soon as the format is determined,
# this step can be automated)
# 
# In order to put angles in a right order, print name of them by running
# FileNames.py and then replace values of "angles[14,13,12, etc]" with the
# new angles.
##########################################################




def all_analyzer(x,size1,size2,S_Factor):

    FRDs=[]
    datadir=str(x) + "/"
    filename = os.listdir(datadir)
    print filename

## 
    angles = [14, 8, -8, -12, -6, -4, 4, 6]
    for filename_ in filename:

            im = plt.imread(datadir + filename_)
            Image = im[size1:size2]

	    smoothed_S = convolve(Image[0], Box1DKernel(20+S_Factor))
	    peakind = signal.find_peaks_cwt(smoothed_S, np.arange(50,150))



#	    C1=smoothed_S[300:700]
	    C1=smoothed_S
	    X =range(len(C1)) 

	    X=np.array(X)-10

	    FWHM = fwhm(X, C1, k=10)


	    F1 = FWHM[1]*1.2
	    F2 = FWHM[2]*1.2

	    DiffF = np.abs(F2 - F1)

	    S1 = FWHM[1]*1.7
	    S2 = FWHM[2]*1.7
 
	    DiffS = np.abs(S2 - S1)


	    j = []
	    Peak = []
	    for i in range(len(smoothed_S[peakind])):
	    #    j=[]
	         if smoothed_S[peakind][i]>50:
	              j.append(i)

	    k=[]
	    Peak1Flux=[]
	    Peak2Flux=[]
	    Peak1=[]
	    Peak2=[]

	    Peak1Flux = sorted(smoothed_S[peakind],reverse=True)[0]
	    Peak2Flux = sorted(smoothed_S[peakind],reverse=True)[1]

	    S= [S1,S2]
	    F= [F1,F2]
	    Diameter = np.abs(np.where(smoothed_S == Peak1Flux)[0][0] - np.where(smoothed_S == Peak2Flux)[0][0])
	#   Diameter = np.abs(np.array(range(len(smoothed_S)))[peakind][Peak1]-np.array(range(len(smoothed_S)))[peakind][Peak2])
            print Diameter
	    FRD = []
	    e2 = np.abs(S[0]-S[1])
	    FRD = e2/Diameter

            FRDs.append(FRD)




    fig = plt.figure()
            
    plot(angles,FRDs,'ro')
#    plot(FRDs,'ro')
    plt.xlabel("Angles (deg)")
    plt.ylabel("FRD")
    fig.show()
    Tk.mainloop()





##########################################################
# By this function, the best smoothing factor can be determined. 
# It simply subtracts two gaussians by each other and shows
# the mean value of the graph. When it is minimum, it means
# that you have the right SF
##########################################################



def SF_Finder(x,size1,size2,angle,S_Factor):

    img = plt.imread(str(x))
    ang=[]
    rows,cols = img.shape
    if angle==0:
        ang=1
    else:
        ang=angle

    M = cv2.getRotationMatrix2D((cols/2,rows/2),ang,1)
    rot = cv2.warpAffine(img,M,(cols,rows))

    Image = rot[size1:size2] 


    smoothed_S = convolve(Image[0], Box1DKernel(20+S_Factor))
    peakind = signal.find_peaks_cwt(smoothed_S, np.arange(50,150))

#    C1=smoothed_S[300:700]
#    C1=smoothed_S[300:490]
    C1 = smoothed_S
    X =range(len(C1)) 
    X2=range(len(C1))

    FWHM = fwhm(X, C1, k=10)

    F1 = FWHM[1]*1.2
    F2 = FWHM[2]*1.2

    DiffF = np.abs(F2 - F1)

    S1 = FWHM[1]*1.7
    S2 = FWHM[2]*1.7
 
    DiffS = np.abs(S2 - S1)


    j = []
    Peak = []
    for i in range(len(smoothed_S[peakind])):
    #    j=[]
         if smoothed_S[peakind][i]>50:
              j.append(i)

    k=[]
    Peak1Flux=[]
    Peak2Flux=[]
    Peak1=[]
    Peak2=[]

    Peak1Flux = sorted(smoothed_S[peakind],reverse=True)[0]
    Peak2Flux = sorted(smoothed_S[peakind],reverse=True)[1]

    S= [S1,S2]
    F= [F1,F2]
    Diameter = np.abs(np.where(smoothed_S == Peak1Flux)[0][0] - np.where(smoothed_S == Peak2Flux)[0][0])
   

    FRD = []
    e2 = np.abs(S[0]-S[1])
    FRD = e2/Diameter
    X2 = np.array(X2)-10
    fig = plt.figure()
    x_axis = range(len(C1))
    x_axis2 = range(len(Image[0]))
    x_axis_new = np.array(x_axis2)+10
#    arr_ref = np.array([1, 5, 2, 3, 7, 1])  # shape (6,), reference
#    arr1 = np.array([1, 5, 2, 3, 7, 2, 1])  # shape (7,), to "compress"
#    arr2 = np.array([1, 5, 2, 7, 1])        # shape (5,), to "stretch"
    arr_ref=Image[0]
    arr1 = C1
    arr1_interp = interp.interp1d(np.arange(arr1.size),arr1)
    arr1_compress = arr1_interp(np.linspace(0,arr1.size-1,arr_ref.size))




#    plot(C1[5:1615])
#    plot(Image[0])
#    res = arr1_compress - Image[0]
    res = Image[0] - C1[10:1610]
    mean= np.mean(res)
    return np.round(mean,5)




###
#
# Each of the above functions can be used individually
# by removing "#" from the the following comments
#
###


#fwhm_shower(I,670,690)
#disp('Test.tif',670,690,45)
#slice('Test.tif',670,690,0)
#peakfinder('p2_RT2.tif',670,690,0)
#fwhm_shower('p10_RT5.tif',600,610,0)
#calibrate('p10_RT2.tif',600,610,10)
#comparison('p6_RT5.tif',600,610,0)
#all_analyzer('All',600,610)
#Center_Finder("p10_RT2.tif")

'''
SF_finder('p10_RT.tif',630,650,0,-10)
SF_finder('p10_RT.tif',630,650,0,-7)
SF_finder('p10_RT.tif',630,650,0,-5)
SF_finder('p10_RT.tif',630,650,0,-3)
SF_finder('p10_RT.tif',630,650,0,-2)
SF_finder('p10_RT.tif',630,650,0,0)
'''

#######################################
#
#
#REFERENCES
#
#
#######################################
#
# The FWHM procedure is influenced by https://stackoverflow.com/questions/10582795/finding-the-full-width-half-maximum-of-a-peak
# The Peakfinder function is influenced by https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.find_peaks_cwt.html
# The rot function is influenced by http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
#
#######################################
