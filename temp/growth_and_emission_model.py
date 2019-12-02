# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 11:04:50 2019

@author: Andrea Nistad
"""

import pandas as pd
import matplotlib as plt
#reading in the growth model 
filename = "C:/Users/Andrea Nistad/OneDrive - NTNU/Attachments/Masteroppgave/RAS model/growth.xlsx"

#Using case 1 to start with 
df = pd.read_excel(filename, sheet_name=1)
print(df.head())


#plotting the growth curve from 5 g to 5000 g - this is based on the growth model developed by SINTEF
#the model is obtained from Morefish
df['weight beginning of week'].plot()


#setting the number of fish assumed
number_of_tanks = 1
number_of_fish_start = 300000*number_of_tanks#pieces
max_specific_density = 60 #kg per m3
max_weight = df['weight end of week'].iloc[-1]/1000 #g to kg - final weight is 5 kg 
#Volume of the last department
volume = (number_of_fish_start*max_weight)/max_specific_density



#have to add dødelighet here later, but no assume no dødelighet - so equal number of fish 
df['total weight'] = df['weight beginning of week']*number_of_fish_start/1000 #in kg 

#total feed amount per week
df['total feed'] = df['feed']*number_of_fish_start


#all values in kg
df['TSS'] = 0.25*df['total feed']
df['co2'] = 0.409*df['total feed']
df['TAN'] = 0.54*0.095*df['total feed']
df['oxygen'] = df['oxygen']*number_of_fish_start

ax1 = df['TSS'].plot()
df['co2'].plot(ax=ax1)
df['TAN'].plot(ax=ax1)
df['oxygen'].plot(ax=ax1)
ax1.legend()

df['sludge at 90'] = df['total feed']*0.144

df['sludge at 10'] = df['total feed']*1.28


#Calculating all necessary flows
HRT = 40
salinity = 0.012 #12 permille in post-smolt department
Q_recirc = volume/HRT*60 #m3/h

recirc_degree = 0.985
Q_in  = (Q_recirc-recirc_degree*Q_recirc)/recirc_degree #m3/h

runfile("defined_functions.py")

fw_share, sw_share = flow_intake_share_salinity(0.012)
Q_in_fw = fw_share*Q_in 
Q_in_sw = sw_share*Q_in