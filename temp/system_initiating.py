# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:55:48 2019

@author: Andrea Nistad
"""


import pandas as pd 
import matplotlib as plt 
import numpy as np
#Defining the system dimensions 
runfile("energy_functions.py")

class RAS(): 
    def __init__(self):
        number_of_departments = 2#len(list_of_dict)
        i=0
        self.departments = list()
        
        self.flow_intake=0
        self.flow_intake_freshwater=0
        self.flow_intake_seawater=0
        if i <= number_of_departments: 
            self.department1 = self.Department(1,9,40,50, 0.003)
            self.department1.set_dimensions()
            self.department1.set_intake_water_flows()
            #self.departments.append(self.department1)
            i+=1
            self.flow_intake+=self.department1.flow_intake
            self.flow_intake_seawater = self.department1.flow_seawater
            self.flow_intake_freshwater = self.department1.flow_seawater
        
        if i <= number_of_departments:
            self.department2 = self.Department(1,14,40,60, 0.003)
            self.department2.set_dimensions()
            self.department2.set_intake_water_flows()
            self.flow_intake+=self.department2.flow_intake
            self.flow_intake_seawater = self.department2.flow_seawater
            self.flow_intake_freshwater = self.department2.flow_seawater
            i+=1
    
        '''if i <= number_of_departments: 
            self.department3 = self.Department(1,14,40,60, 0.003)
            #self.department3.set_dimensions()
            #self.department3.set_intake_water_flows()
            self.departments.append(self.department3)
            i+=1
        
        if i <= number_of_departments:
            self.department4 = self.Department(1,14,40,60, 0.003)
            #self.department4.set_dimensions()
            #self.department4.set_intake_water_flows()
            self.departments.append(self.department4)
            i+=1'''
                
        
    class Department(): 
        def __init__(self, number_tanks, diameter_tanks, HRT, specific_density, salinity): 
            self.number_tanks = number_tanks
            self.diameter_tanks = diameter_tanks
            self.HRT = HRT
            self.specific_denisty = specific_density
            self.salinity = salinity
            self.recirc_degree = 0.985
        
    #height_tanks = (1/2.5)*self.diameter_tanks
    #volume_tanks = height_tanks*(diameter_tanks/2)**2*3.14
    
        def set_dimensions(self):
            if self.diameter_tanks >= 10:
                ratio = 2.8
            if self.diameter_tanks < 10:
                ratio = 2
            self.height_tanks = (1/ratio)*self.diameter_tanks
            self.volume_tanks = self.height_tanks*(self.diameter_tanks/2)**2*3.14
            self.flow_recirc = self.volume_tanks/self.HRT*60
        
        
        def print_dimensions(self): 
            print('height tank')
            print(self.height_tanks)
            print('volume tank')
            print(self.volume_tanks)
            print('flow tank')
            print(self.flow_recirc)
            

        def set_intake_water_flows(self): 
            self.flow_intake = (self.flow_recirc-self.recirc_degree*self.flow_recirc)/(self.recirc_degree)
            self.flow_seawater = flow_intake_share_salinity(self.salinity)[1]*self.flow_intake
            self.flow_freshwater = flow_intake_share_salinity(self.salinity)[0]*self.flow_intake
        
        
        def flow_intake_share_salinity(salinity): 
            salinity_sw = 0.035
            salinity_fw = 0.00
    
            m_fw = ((salinity-salinity_sw)/(salinity_fw-salinity_sw))
            m_sw = 1-m_fw
            return m_fw, m_sw
                
    def calculate_power_consumption_by_unit_and_department(self): 
        for department in [self.department1, self.department2]: 
    
            #Drumfilter calculation
            department.mechfilter_rotation = power_consumption_drumfilter(department.flow_recirc)[0]
            department.mechfilter_backwash = power_consumption_drumfilter(department.flow_recirc)[1]
    
    
    
            #Main pump
            #height of tanks, but have to 
            head_friction_losses = 0.125*department.height_tanks
            department.main_pump = power_consumption_pump(department.height_tanks+head_friction_losses,0.8,department.flow_recirc)
   
    
            #Degasser
            department.degasser = power_consumption_degasser_fan(department.flow_recirc)
    
            #Feeder and lights in tank
            department.feeder = power_consumption_fish_tank(department.number_tanks, department.diameter_tanks)[0]
            department.tank_light = power_consumption_fish_tank(department.number_tanks, department.diameter_tanks)[1]

            #Biofilter - add so that the volume of the biofilter is returned too
            department.biofilter = power_biofilter(department.fish.system_temp,department.fish.TAN.iloc[-1])


            #Oxygenation 
            #assume a partial oxygenation cone in both departments... 
            department.oxygenation = power_oxygenation(department.flow_recirc,"partial")
    
    
    
            #Intake water
            ## Seawater pump
            department.pump_intake = power_consumption_pump(60,0.8,department.flow_seawater) + power_consumption_pump(4,0.8, department.flow_freshwater)
    
            ## Freshwater pump
    
            ## UV
            department.UV = power_consumption_UV(department.flow_intake)

            ## Mechanical filter
            department.mechfilter_inlet = power_consumption_drumfilter(department.flow_intake)[0] + power_consumption_drumfilter(department.flow_intake)[1] 
    
            ## Heat pump 
            COP = 10
            department.heat_pump = power_heat_pump(department.flow_freshwater, department.flow_seawater, COP, department.fish.system_temp, department.fish.MW)
    
            #Building - should this maybe be added to the system instead?? 
            ## Ventilation
            department.ventilation = power_consumption_ventilation(department.diameter_tanks)
    
    
            ## Heating offices ++
            department.building_heating = power_consumption_building_heating(department.diameter_tanks)
    
            ## Heating lightning 
            department.lightning = power_consumption_lightning(department.diameter_tanks)
    
    
            ## Sludge treatment
            department.total_power = list()
            department.total_power.append(department.mechfilter_rotation + department.mechfilter_backwash)
            department.total_power.append(department.main_pump)
            department.total_power.append(department.degasser)
            department.total_power.append(department.feeder)
            department.total_power.append(department.tank_light)
            department.total_power.append(department.biofilter)
            department.total_power.append(department.oxygenation)
            department.total_power.append(department.pump_intake)
            department.total_power.append(department.UV)
            department.total_power.append(department.mechfilter_inlet)
            department.total_power.append(department.ventilation)
            department.total_power.append(department.building_heating)
            department.total_power.append(department.lightning)
    
            department.energy_use = [x*7*24*len(department.fish.end_weight) for x in department.total_power]
            department.energy_use.append(sum([x*7*24 for x in department.heat_pump]))
            units = ["mechanical filtration", "pump", "degasser", "feeder", "tank light", "biofilter", "oxygenation", "pump intak", "UV", "mechanical filtration inlet", "ventilation", "building heating", "lighting", "heat pump"]
            department.distribution = pd.DataFrame(list(zip(units,[x/sum(department.energy_use)*100 for x in department.energy_use])))
            
            print(department.distribution)
            
    def calculate_energy_consumption_by_unit(self): 
        units = ["mechanical filtration", "pump", "degasser", "feeder", "tank light", "biofilter", "oxygenation", "pump intak", "UV", "mechanical filtration inlet", "ventilation", "building heating", "lighting", "heat pump", "other"]
        self.calculate_power_consumption_by_unit_and_department()
        
        # adding 20 % of energy use for other purposes
        share_other = 0.19
        list_power = [self.department1.energy_use[i] + self.department2.energy_use[i] for i in np.arange(len(self.department2.energy_use))]
        list_power.append(sum(list_power)*share_other)
        self.energy_use = pd.DataFrame(list(zip(units,list_power))).set_index(0)
        
        return self.energy_use
    
    def energy_distribution(self):
        units = ["mechanical filtration", "pump", "degasser", "feeder", "tank light", "biofilter", "oxygenation", "pump intak", "UV", "mechanical filtration inlet", "ventilation", "building heating", "lighting", "heat pump", "other"]
        self.distribution = self.energy_use/self.energy_use.sum().iloc[-1]*100

        return self.distribution
    
    def total_energy_use(self):
        self.calculate_energy_consumption_by_unit()
        return self.energy_use.sum().iloc[-1]
    
    def total_power(self): 
        return sum(self.department1.total_power) + sum(self.department2.total_power)
    
    def specific_power(self): 
        return (sum(self.department1.total_power) + sum(self.department2.total_power))/(self.department1.volume_tanks + self.department2.volume_tanks)
    

class Fish(): 
    def __init__(self, filename, sheet_name, number_of_fish): 
        df = pd.read_excel(filename, sheet_name=sheet_name)
        self.start_weight = df['weight beginning of week']/1000 #convert to kg
        self.end_weight = df['weight end of week']/1000 #convert to kg 

        self.system_temp = df['Temp']
        self.FCR = df['FCR']
        self.feed = df['feed']
        
        self.start_total_weight = self.start_weight*number_of_fish
        self.end_total_weight = self.end_weight*number_of_fish
        
        self.oxygen = df['oxygen']*number_of_fish
        self.TSS = 0.25*df['feed']*number_of_fish
        #self.co2 = 0.409*df['feed']*number_of_fish #co2 from project thesis
        self.co2 = 0.81*df['oxygen']*number_of_fish #RQ from AGA 
        self.TAN = 0.54*0.095*df['feed']*number_of_fish #already in kg
        self.MW = number_of_fish*self.end_weight**0.63

    def plot_fish(self):
        #ax = self.start_weight.plot(secondary_y=True, label='fish weight')
        ax = self.feed.plot(label='feed')
        self.oxygen.plot(ax=ax, label='o2')
        self.TSS.plot(ax=ax, label = 'tss')
        self.co2.plot(ax=ax, label = 'co2')
        self.TAN.plot(ax=ax, label='tan')
   
        ax.legend()  

#Calculating the maximum number of fish 
        
RAS = RAS()
RAS.department1.print_dimensions()
RAS.department2.print_dimensions()


filename = "C:/Users/Andrea Nistad/OneDrive - NTNU/Attachments/Masteroppgave/RAS model/growth.xlsx"
fish1 = Fish(filename,1,1)
fish2 = Fish(filename,2,1)

max_fish_dep2 = (RAS.department2.specific_denisty * RAS.department2.volume_tanks*RAS.department2.number_tanks)/fish2.end_weight.iloc[-1]

max_fish_dep1 = (RAS.department1.specific_denisty * RAS.department1.volume_tanks*RAS.department1.number_tanks)/fish1.end_weight.iloc[-1]

if max_fish_dep2 <= (max_fish_dep1-max_fish_dep1*0.1): 
    print('Have to add more tanks/volume to second department!!')
  

fish_produced = max_fish_dep2
RAS.department1.fish = Fish(filename,1,fish_produced)
RAS.department2.fish = Fish(filename,2,fish_produced)


biomass_production = RAS.department2.fish.end_weight.iloc[-1]*fish_produced

SEC = RAS.total_energy_use()/biomass_production

print("SEC:")
print(SEC)
print("distribution")
print(RAS.energy_distribution())
print("specific power")
print(RAS.specific_power())



