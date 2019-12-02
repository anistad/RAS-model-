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
    def __init__(self,list_of_dict):
        number_of_departments = len(list_of_dict)
        i=0
        self.departments = list()
        
        self.flow_intake=0.00
        self.flow_intake_freshwater=0.00
        self.flow_intake_seawater=0.00
        self.volume = 0
        
        ## The office area is assumed to equal 35% of the area in the first and second department only
        self.office_area = 0
        if i < number_of_departments: 
            spec = list_of_dict[i]
            self.department1 = self.Department(spec['number tanks'],spec['diameter'],spec['HRT'], spec['specific density'], spec['salinity'], spec['recirc degree'])
            self.department1.set_dimensions()
            self.department1.set_intake_water_flows()
            self.departments.append(self.department1)
            i+=1
            self.flow_intake+=self.department1.flow_intake*self.department1.number_tanks
            self.flow_intake_seawater+=self.department1.flow_seawater*self.department1.number_tanks
            self.flow_intake_freshwater+= self.department1.flow_seawater*self.department1.number_tanks
            self.volume+=self.department1.volume_tanks*self.department1.number_tanks
            self.office_area+=self.department1.diameter_tanks**2*0.35
        
        if i < number_of_departments:
            spec = list_of_dict[i]
            self.department2 = self.Department(spec['number tanks'],spec['diameter'],spec['HRT'], spec['specific density'], spec['salinity'], spec['recirc degree'])
            self.department2.set_dimensions()
            self.department2.set_intake_water_flows()
            self.departments.append(self.department1)
            self.flow_intake+=self.department2.flow_intake*self.department2.number_tanks
            self.flow_intake_seawater+= self.department2.flow_seawater*self.department2.number_tanks
            self.flow_intake_freshwater+= self.department2.flow_seawater*self.department2.number_tanks
            self.volume+=self.department2.volume_tanks*self.department2.number_tanks
            self.office_area+=self.department2.diameter_tanks**2*0.35
            i+=1
    
        if i < number_of_departments: 
            spec = list_of_dict[i]
            self.department3 = self.Department(spec['number tanks'],spec['diameter'],spec['HRT'], spec['specific density'], spec['salinity'], spec['recirc degree'])
            self.department3.set_dimensions()
            self.department3.set_intake_water_flows()
            self.departments.append(self.department3)
            self.flow_intake+= self.department3.flow_intake*self.department3.number_tanks
            self.flow_intake_seawater+= self.department3.flow_seawater*self.department3.number_tanks
            self.flow_intake_freshwater+= self.department3.flow_seawater*self.department3.number_tanks
            self.volume+=self.department3.volume_tanks*self.department3.number_tanks

            i+=1
        
        if i < number_of_departments:
            spec = list_of_dict[i]
            self.department4 = self.Department(spec['number tanks'],spec['diameter'],spec['HRT'], spec['specific density'], spec['salinity'], spec['recirc degree'])
            self.department4.set_dimensions()
            self.department4.set_intake_water_flows()
            self.departments.append(self.department4)
            self.flow_intake+= self.department4.flow_intake*self.department4.number_tanks
            self.flow_intake_seawater+= self.department4.flow_seawater*self.department4.number_tanks
            self.flow_intake_freshwater+= self.department4.flow_seawater*self.department4.number_tanks
            self.volume+=self.department4.volume_tanks*self.department4.number_tanks
            

            i+=1
                
        
    class Department(): 
        def __init__(self, number_tanks, diameter_tanks, HRT, specific_density, salinity, recirc_degree): 
            self.number_tanks = number_tanks
            self.diameter_tanks = diameter_tanks
            self.HRT = HRT
            self.specific_denisty = specific_density
            self.salinity = salinity
            self.recirc_degree = recirc_degree
        
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
    
                #Drumfilter calculation
                self.mechfilter_rotation = power_consumption_drumfilter(self.flow_recirc)[0]
                #assume that the backwashing pump only operates 50 % of the time 
                self.mechfilter_backwash = power_consumption_drumfilter(self.flow_recirc)[1]*0.5
                
    

                #Main pump
                #height of tanks, but have to 
                head_friction_losses = 0.125*self.height_tanks
                self.main_pump = power_consumption_pump(self.height_tanks+head_friction_losses,0.8,self.flow_recirc)
   
    
                #Degasser
                self.degasser = power_consumption_degasser_fan(self.flow_recirc)
    
                #Feeder and lights in tank
                self.feeder = power_consumption_fish_tank(self.diameter_tanks)[0]
                self.tank_light = power_consumption_fish_tank(self.diameter_tanks)[1]

                #Biofilter - add so that the volume of the biofilter is returned too
                self.biofilter = power_biofilter(self.fish.system_temp,self.fish.TAN.iloc[-1])


                #Oxygenation 
                #assume a partial oxygenation cone in both departments... 
                self.oxygenation = power_oxygenation(self.flow_recirc,self.salinity)
    
    
    
                #Intake water
                ## Seawater pump
                self.pump_intake = power_consumption_pump(60,0.8,self.flow_seawater) + power_consumption_pump(4,0.8, self.flow_freshwater)
    
                ## Freshwater pump
    
                ## UV
                self.UV = power_consumption_UV(self.flow_intake)

                ## Mechanical filter
                self.mechfilter_inlet = power_consumption_drumfilter(self.flow_intake)[0] + power_consumption_drumfilter(self.flow_intake)[1] 
    
                ## Heat pump 
                COP = 10
                self.heat_pump = power_heat_pump(self.flow_freshwater, self.flow_seawater, COP, self.fish.system_temp, self.fish.MW, water_temp)
    
                #Building - should this maybe be added to the system instead?? 
                ## Ventilation
                self.ventilation = power_consumption_ventilation(self.diameter_tanks, RAS.office_area)
    
    
                ## Heating offices ++
                self.building_heating = power_consumption_building_heating(self.diameter_tanks,RAS.office_area)
    
                ## Heating lightning 
                self.lightning = power_consumption_lightning(self.diameter_tanks, RAS.office_area)
    
    
                ## Sludge treatment
                self.sludge_filtering = average(sludge_treatment_filtering(self.fish.feed/(7*24)))
                
                self.total_power = list()
                self.total_power.append(self.mechfilter_rotation*self.number_tanks + self.mechfilter_backwash*self.number_tanks)
                self.total_power.append(self.main_pump*self.number_tanks)
                self.total_power.append(self.degasser*self.number_tanks)
                self.total_power.append(self.feeder*self.number_tanks)
                self.total_power.append(self.tank_light*self.number_tanks)
                self.total_power.append(self.biofilter*self.number_tanks)
                self.total_power.append(self.oxygenation*self.number_tanks)
                self.total_power.append(self.pump_intake*self.number_tanks)
                self.total_power.append(self.UV*self.number_tanks)
                self.total_power.append(self.mechfilter_inlet*self.number_tanks)
                self.total_power.append(self.ventilation*self.number_tanks)
                self.total_power.append(self.building_heating*self.number_tanks)
                self.total_power.append(self.lightning*self.number_tanks)
                self.total_power.append(self.sludge_filtering)
                
                
                
                self.energy_use = [x*7*24*len(self.fish.end_weight) for x in self.total_power]
                self.energy_use.append(sum([abs(x)*7*24*self.number_tanks for x in self.heat_pump]))
                units = ["mechanical filtration", "pump", "degasser", "feeder", "tank light", "biofilter", "oxygenation", "pump intak", "UV", "mechanical filtration inlet", "ventilation", "building heating", "lighting", "sludge", "heat pump"]
                self.distribution = pd.DataFrame(list(zip(units,[x/sum(self.energy_use)*100 for x in self.energy_use])))
                
                print(self.distribution)
                
    def calculate_energy_consumption_by_unit(self): 
        units = ["mechanical filtration", "pump", "degasser", "feeder", "tank light", "biofilter", "oxygenation", "pump intak", "UV", "mechanical filtration inlet", "ventilation", "building heating", "lighting", "sludge filtering", "heat pump",  "other"]
        if len(self.departments) == 1: 
            self.department1.calculate_power_consumption_by_unit_and_department()
            list_power = [self.department1.energy_use[i] for i in np.arange(len(self.department1.energy_use))]
        if len(self.departments) == 2: 
            self.department1.calculate_power_consumption_by_unit_and_department()
            self.department2.calculate_power_consumption_by_unit_and_department()
            list_power = [self.department1.energy_use[i] + self.department2.energy_use[i] for i in np.arange(len(self.department2.energy_use))]
        if len(self.departments) == 3: 
            self.department1.calculate_power_consumption_by_unit_and_department()
            self.department2.calculate_power_consumption_by_unit_and_department()
            self.department3.calculate_power_consumption_by_unit_and_department()
            list_power = [self.department1.energy_use[i] + self.department2.energy_use[i] + self.department3.energy_use[i] for i in np.arange(len(self.department3.energy_use))]

        if len(self.departments) == 4: 
            self.department1.calculate_power_consumption_by_unit_and_department()
            self.department2.calculate_power_consumption_by_unit_and_department()
            self.department3.calculate_power_consumption_by_unit_and_department()
            self.department4.calculate_power_consumption_by_unit_and_department()
            list_power = [self.department1.energy_use[i] + self.department2.energy_use[i] + self.department3.energy_use[i] + self.department4.energy_use[i]for i in np.arange(len(self.department4.energy_use))]
            
            
        # adding 20 % of energy use for other purposes
        share_other = 0.19
       
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
        if len(self.departments) == 1: 
            return sum(self.department1.total_power)
        if len(self.departments) == 2: 
            return sum(self.department1.total_power) + sum(self.department2.total_power)
        if len(self.departments) == 3: 
            return sum(self.department1.total_power) + sum(self.department2.total_power) + sum(self.department3.total_power)
        if len(self.departments) == 4: 
            return sum(self.department1.total_power) + sum(self.department2.total_power) + sum(self.department3.total_power) + sum(self.department4.total_power)

    
    def specific_power(self):
        share_other = 0.2
        return (self.total_power()+share_other*self.total_power())/self.volume
    

class Fish(): 
    def __init__(self, df, number_of_fish): 
        self.start_weight = df['weight beginning of week']/1000 #convert to kg
        self.end_weight = df['weight end of week']/1000 #convert to kg 

        self.system_temp = df['Temp']
        self.FCR = df['FCR']
        self.feed = df['feed']*number_of_fish
        
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

def return_fish_dataframe(start_weight,end_weight, filename, sheetname): 
    df = pd.read_excel(filename, sheet_name=sheetname)
    df.set_index(df['week'], inplace =True)
    end_idx = df.iloc[(df['weight end of week']-end_weight).abs().argsort()[:1]]['weight end of week'].index.values[0]
    start_idx = df.iloc[(df['weight beginning of week']-start_weight).abs().argsort()[:1]]['weight beginning of week'].index.values[0] 

    return df.iloc[start_idx-1:end_idx,:]


def max_number_of_fish(fish,end_weight, last_department): 
    return (last_department.specific_denisty * last_department.volume_tanks*last_department.number_tanks)/fish.end_weight.iloc[-1]
    


