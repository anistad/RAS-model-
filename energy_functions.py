# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 14:45:15 2019

@author: Andrea Nistad
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np 
import matplotlib.pyplot as plt 
import math as math



def power_consumption_pump(height, eff, Q):
    '''This equation calculates the power consumption of a pump using the standard pump equation and returns the power
    consumption in kW'''
    # waterflow given in m3/h
    # height given in m 
    # efficiency - no unit 
       
    ro = 997; #density of water, kg/m3 
    g = 9.81; #gravity, kg/m*s^2
    
    return (ro*g*height*Q)/(60*60*eff*1000) 

def flow_intake_share_salinity(salinity): 
    '''This function calculates the share of freshwater and seawater required to yield 
    the salinity specified'''
    
    salinity_sw = 0.035 #salinity in seawater
    salinity_fw = 0.00 #salinity in freshwater
    
    m_fw = ((salinity-salinity_sw)/(salinity_fw-salinity_sw))
    m_sw = 1-m_fw
    return m_fw, m_sw

def power_consumption_fish_tank(diameter):
    '''This function takes the tank diameter as an argument and calculates the power consumption of 
    the feeder and lights. The number of installed units depends on the tank diameter. The larger 
    tanks need two feeders and a stronger light, while the smaller need one feeder and a smaller light.'''

    installed_power_feeder = 120/1000 #kW
    if diameter <= 10: 
        installed_power_lights = 0.8 #kW
        installed_power_feeder*=1#kW
    if diameter > 10: 
        installed_power_lights = 1.5
        installed_power_feeder*=2
    
    return installed_power_feeder, installed_power_lights
   
    
def find_nearest(array, value):
    ''' This function finds the nearest values in an array and is used by the next function '''
    idx = (np.abs(array-value)).argmin()
    return idx
    

def power_consumption_drumfilter(Q): 
    ''' This function calculates the power consumption of the drum filter and is based on data
    for power consumption required for rotating the drum specified by the Hydrotech filters. In addition
    power is required for the backwashing pump, which is typically five times the rotation power. '''
    
    # Dimensioing parameters
    Q_dim = np.array([8, 22, 44, 50, 66, 99, 132, 176, 220, 264, 308, 385])*60/1000*60 # flow through drum filter, m3/h
    P_rotationdrum_dim = [0.18, 0.25, 0.25, 0.25, 0.37, 0.37, 0.55, 0.55, 0.55, 0.55, 0.55, 1.1] #kW, power for rotating drum 
    
    P_backwash_dim = [x * 5 for x in P_rotationdrum_dim] #five times energy use during backwashing of filter 

    # Finding the index of the water flow in drumfilter specifications closest to Q
    idx = find_nearest(Q_dim, Q)
    
    # Showing power consumption vs. waterflow on a graph 
    '''plt.figure()
    plt.plot(Q_dim, P_rotationdrum_dim)
    plt.plot(Q,P_rotationdrum_dim[idx], 'o')
    plt.ylabel('kW')
    plt.xlabel('m3/h')
    plt.show()'''

    return P_rotationdrum_dim[idx], P_backwash_dim[idx]

def power_consumption_UV(Q):
    '''This function estimates the power needed for UV disinfection of the intake water and is based
    on regression lines from three different suppliers (as described in the project thesis).The average
    of the three regressions lines is returned. Instead of delivering a dose of 150 as assumed in 
    the project thesis a dose of 30 is assumed. '''
    
    # Regression lines from UV suppliers (documentation in the project thesis)
    power_cons_uv1 = 0.0214*Q+0.3818
    power_cons_uv2 = 0.0155*Q+0.5259
    power_cons_uv3 = 0.0157*Q+0.2304
    
    return (power_cons_uv1+power_cons_uv2+power_cons_uv3)/3

def power_biofilter(temp, TAN_end): 
    '''This function calculates the required biofilter volume, as outlined in the project thesis work. 
    The nitrification rates are lower in 
    Thereafter this is multiplied by 15 W/m3, which is the specific power consumptiono per biofilter
    volume. '''
    
    volume_chamber_MBBR=list()
    theta = 1.09
    k_t1 = 0.82
    T1 = 15; 
    T2 = temp.iloc[-1] #temperature of the system
    k_t2 = k_t1*theta**(T2-T1)
    
    n = 0.7
    S_n = [0.9**n, 0.35**n, 0.15**n] 
    
    
    nitrification_rates = [k_t2*x for x in S_n]
    

    medium_volume = 900 

    fill_factor = 0.5 
    C_in_MBBR = 2
    C_out_MBBR = 0.1
    
    for i in np.arange(2): 
        if i == 0: 
            C_in = C_in_MBBR
            C_out = 0.9
        if i == 1: 
            C_in = 0.9
            C_out = 0.35
        if i == 2: 
            C_in = 0.35
            C_out = 0.15
        
        eff = (C_in-C_out)/(C_in_MBBR-C_out_MBBR)
        TAN_max = TAN_end/7
        TAN_removal_rate = (eff*TAN_max*1000)/(eff*TAN_max*1000)/nitrification_rates[i]
        volume_chamber_MBBR.append(eff*TAN_max*1000/nitrification_rates[i]/medium_volume)
        
    total_volume=sum(volume_chamber_MBBR)*(1/fill_factor)
    
    power_factor = 15/1000 #15 W per m3
    return total_volume*power_factor

def power_heat_pump(Q_intake_fw,Q_intake_sw, COP, system_temp, MW_fish, water_temp):
    '''This function calculates the power use by the heat pump, based on water flow, temperature different
    and COP. In addition the heat gain from the fish metabolism is modeled following Smith et al. (1978)'''
    delta_T = system_temp-water_temp
    
    cp = 4.12 #J/kg K
    ro = 1000 #kg/m3
    
    heat_demand = ((Q_intake_fw+Q_intake_sw)/60/60)*ro*cp*delta_T #kW
    
    # This regression line models the heat production per metabolic weight and depends on temperature
    HP = (0.66+0.0339*system_temp)*0.001163 #KWh/kg fish weight/hr

    # The heat production by fish is found 
    heat_gain_fish = HP*MW_fish
    
    # This is the net heat demand 
    net_heat_demand = heat_demand#-heat_gain_fish
 
    return net_heat_demand/COP


def power_oxygenation(Q_recirc,salinity):
    '''This function calculates the power needed for oxygenation in the system. If a freshwater system
    is modeled the oxygen cone oxygenating only 15% of the total flow is used. If not the LHO is used 
    instead.'''
    
    if salinity < 0.012: 
         #This equation is baed on supplier information and can be found in the project thesis appendix 
        
        return 0.0074*(0.15*Q_recirc)*(1/60)*1000 + 0.4155 
    
    else: 
        ## Information taken from AGA calculations decribed in the project thesis
        pressure = 1.1 #mWC
        eff = 0.7 
                
        return power_consumption_pump(pressure, eff, Q_recirc)
    
def power_consumption_degasser_fan(Q_recirc): 
    ''' This should maybe be updated?'''
    '''GL = 5 #gas to liquid ratio
    P_1 = 101*1000 #kPa
    P_2 = 138*1000#kPa
    
    eff = 0.7
    Q_flow = Q_recirc/3600 #converting from m3/h to m3/sek
   
    #return ((GL*(Q_flow)*P_1)/(17.4*eff))*((P_2/P_1)**(0.283)-1)'''
    return  0.0037*Q_recirc
    

def power_consumption_ventilation(tank_diameter, office_area): 
    '''This function calculates the power consumption for ventilation based on the tank diameter and a 
    given office area. The building volume is estimated as following. The are of the tanks etc. is the
    square of the tank diameter, and 35% of the tank area is needed for water treatment. The height of the building is assumed
    to be 4 meters. Further assumptions are explained in the project thesis. ''' 

    # Estimating tank area
    tank_area = tank_diameter*tank_diameter

    building_volume = (tank_area+0.4*tank_area+0.35*tank_area+office_area)*4
    
    #air exchange rate
    e=1.5 
    
    SFP = 1.3
    return SFP*(e*building_volume)/(60*60)

def power_consumption_building_heating(tank_diameter, office_area): 
    '''This function calculates the building heating needed and use specific heating use from 
    a NVE report. The area needing heating is assumed to be the office area and the water treatment 
    area, which is 35 % of the tank area. The water treatment area is assumed to need less heating than 
    offices, only half. The heating demand assumed is 70 kWh/m2^ year '''
    
    # Estimating tank area
    tank_area = tank_diameter*tank_diameter
    
    # Calculate the average power ue for heating over a year 
    return (70/8760)*(office_area)+(70/8760)*(0.35*tank_area)/2

def power_consumption_lightning(tank_diameter, office_area): 
    ''' The function calculates energy use for lightning (not in tanks). As above, specific lightning 
    is taken from the NVE report and equals 35 kWh/m2/year for light industry and office buildings. 
    Lightning is needed in all zones.'''
    
    tank_area = tank_diameter*tank_diameter
    # Calculate the average kw and multiply with the tank area, water treatment area and office area
    return (35/8760)*(tank_area+office_area+0.35*tank_area)
 
    '''These functions are not added yet, but have to be added '''
def sludge_treatment_filtering(feed): #only to DM10
    #sludge_dm10 = 1.5*df['total feed'] #kg sludge at DM10 produced 
    
    #energy factor is 0.035 KWh/DM10 kg - see project thesis
    
    return feed*0.035

def sludge_treatment_drying(): 
    sludge_dm10 = 1.5#kg sludge at DM10 produced 
    return df['total feed']*0.73

def average(lst): 
    return sum(lst) / len(lst) 
    
    
    