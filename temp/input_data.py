# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 12:41:49 2019

@author: Andrea Nistad
"""

import numpy as np

runfile("growth_and_emission_model.py")
runfile("energy_functions.py")



#drumfilter calculation
P_rotation, P_backwash  = power_consumption_drumfilter(Q_recirc) #kW

#main pump

#HAVE TO ADJUST THE HEAD OF THE SYSTEM 
diameter = math.sqrt((2.5*volume)/3.14**2)
height_tank = diameter/2.5
head = height_tank
P_main_pump = power_consumption_pump(head,0.8,Q_recirc) + power_consumption_pump(2,0.8,Q_recirc)

#degasser
P_fan_degasser = power_consumption_degasser_fan(Q_recirc)

#feeder and light in tank
P_feeder,P_lights = power_consumption_fish_tank(number_of_tanks)

#biofilter
P_biofilter = power_biofilter()

#oxygenation 
P_oxygenation = power_oxygenation(Q_recirc,"partial")

#intake water 
#pump
P_pump_intake = power_consumption_pump(60,0.8,Q_in_sw)
#UV
P_UV = power_consumption_UV(Q_in_sw+Q_in_fw) #kW
#mech filter inlet 
P_rotation_inlet, P_backwash_inlet = power_consumption_drumfilter(Q_in_sw+Q_in_fw) #kW
#HP
COP = 10 #defining the COP of the heat/cooling system
P_heat_pump, energy_use_HP = power_heat_pump(Q_in_fw, Q_in_sw, COP)

#ventilation
P_ventilation = power_consumption_ventilation()
P_heating_offices = power_consumption_building_heating()
P_lightning = power_consumption_lightning()

#energy use for sludge treatment filtering per week 
energy_use_filtering_sludge_per_week = sludge_treatment_filtering()
#energy_use_drying_sludge_per_week = sludge_treatment_drying()

total_power = [P_rotation+P_backwash, P_main_pump, P_feeder, P_lights, P_biofilter, P_pump_intake, P_UV, P_rotation_inlet +P_backwash_inlet, P_oxygenation, P_fan_degasser, P_ventilation, P_heating_offices, P_lightning]
energy_use_by_unit = [x*len(df)*7*24 for x in total_power]
energy_use_by_unit.append(energy_use_HP)
energy_use_by_unit.append(sum(energy_use_filtering_sludge_per_week))
#energy_use_by_unit.append(sum(energy_use_drying_sludge_per_week))
units = ["mech filter", "punp", "feeder", "lights", "biofilter", "pump intake", "UV intake", "mech intake", "oxygenation", "degassser fan", "ventilation", "building heating", "lightning","heat pump", "sludge filtering", "sludge drying"]

SEC =  sum(energy_use_by_unit)/(number_of_fish_start*df['weight end of week'].iloc[-1]/1000)

distribution = pd.DataFrame(list(zip(units,[x/sum(energy_use_by_unit)*100 for x in energy_use_by_unit])))
print(distribution)
