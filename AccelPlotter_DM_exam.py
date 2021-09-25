# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 17:52:45 2021

@author: Brodney
"""
##Imported libraries
#import pySerial
#import ConfigParser
#import MySQLdb
#from datetime import timedelta as td
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

#import matplotlib.animation as animation
from matplotlib import style

##Serial communications with Arduino (not explored & tested - No available hardware)
# ser = serial.Serial('Com3',9600, timeout=1)         #to consider accel 1 and 2 

# ser.close()
# ser.open()

# while True:
#     data = ser.readline()   
#     print(data.decode())
#     x.append(i)
#     y.append(data.code())
    
#     plt.scatter(i, float(data.decode))
#     i+=1
#     plt.show()
#     plt.pause(0.0001) #gaano kabilis magnext data



##Import CSV files <alternate for arduino set-up; idea is to have csv local database that updates when new .txt file is sent from BT;
##                     problem is bluetooth file not saved automatically on local DB and issue on conversion of .txt due to config. HEX not explored>

##Parse TXT file <not done, no local DB>
# cfg = ConfigParser.ConfigParser ()
# cfg.read ('bluetooth_data.txt') 

with open("PseudoRealTimeData.csv", "r") as d:           #mano-mano converted .txt to .csv
    rawdata = list(csv.reader(d,delimiter = ","))
    

datasample = np.array(rawdata[1:],dtype=np.float)        #kasama sa parsed data yung timestamp pero nahirapan din sa index using datetime, di na ginawa

##Define constants 
seg_len = 1

xa = datasample[:,1]    #di magkakasama huhu
ya = datasample[:,2]
za = datasample[:,3]

# def node1_readings (xa,ya,za):
#     xa,ya,za = np.array(datasample[::2, 1:3],dtype=np.float)  #pangit, mano-mano din, wala na time to define each reading :(

#     return xa, ya, za

# def node2_reading (xa,ya,za):
#     xa,ya,za = np.array(datasample[1::2, 1:3],dtype=np.float)

#     return xa, ya, za


        
##Define Functions
def accel_to_lin_xz_xy(seg_len,xa,ya,za):

    #DESCRIPTION
    #converts accelerometer data (xa,ya,za) to corresponding tilt expressed as horizontal linear displacements values, (xz, xy)
    
    #INPUTS
    #seg_len; float; length of individual column segment
    #xa,ya,za; array of integers; accelerometer data (ideally, -1024 to 1024)
    
    #OUTPUTS
    #xz, xy; array of floats; horizontal linear displacements along the planes defined by xa-za and xa-ya, respectively; units similar to seg_len

    theta_xz = np.arctan2(za,(np.sqrt(xa**2 + ya**2)))
    theta_xy = np.arctan2(ya,(np.sqrt(xa**2 + za**2)))
    xz = seg_len * np.sin(theta_xz)
    xy = seg_len * np.sin(theta_xy)
    
    return xz, xy

##List x-y values

node1_accelread1 = accel_to_lin_xz_xy(seg_len,xa[0],ya[0],za[0])
node2_accelread2 = accel_to_lin_xz_xy(seg_len,xa[1],ya[1],za[1])

downslope = list((node1_accelread1[0], node2_accelread2[0]))
acrossslope = list((node1_accelread1[1], node2_accelread2[1]))
node_pos = (1,2)


##Plotting downslope and across slope
fig, ax = plt.subplots(1,2)
x1 = downslope
x2 = acrossslope
y = node_pos

style.use('seaborn')

#ax[0].clear()
ax[0].plot(x1,y)
ax[0].set_title('Downslope')
ax[0].set_xlabel('Displacement (m)')
ax[0].set_ylabel('Depth (m)')
#ax[0].set_xlim(-0.5,0.5)

#ax[1].clear()
ax[1].plot(x2,y)
ax[1].set_title('Across Slope')
ax[1].set_xlabel('Displacement (m)')
ax[1].set_ylabel('Depth (m)')
#ax[1].set_xlim(0.5,1)

#plot animate as alternate for real time plot <di na natapos>
# def animate(i):
#      graph_data = exampledata.read
#      xa = []
#      ya = []
#      za = []
#    
#      for line in lines:
#          if len(line)>1:
#           xa.append
#           ya.append
#           za.append
#          
          

#ipapasa ko nalang ng ganito huhuhaha di pa enough learning ko for 

     
 