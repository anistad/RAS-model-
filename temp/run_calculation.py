# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 13:31:47 2019

@author: Andrea Nistad
"""

runfile('defined_functions.py')
runfile('input_data.py')




# Power consumption of recirculation pump 
H = 6 #m
eff = 0.8 
recirculation_pump = power_consumption_pump(H, eff, Q_recirc)



# Power consumption of seawater pump 
H = 60 #m 
eff = 0.8 
seawater_intake_share = 0.34 #from salinity = 12 and related share of saltwater
seawater_pump = power_consumption_pump(H, eff, Q_in*seawater_intake_share)
