# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 10:38:39 2019

@author: Andrea Nistad
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 13:58:38 2019

@author: Andrea Nistad
"""
''' This script demonstrates how the different departments and the RAS is initiated. Based on this, the total biomass production
    and energy use is calculated '''
    
from IPython import get_ipython
get_ipython().magic('reset -sf') 
runfile("classes.py")


# Need to define the number of fish prodcued, assume 200 000
fish_produced = 200000
# Define the water source temperature 
water_temp = 6


## Specifying the departments to add 
department1_dict = {'number tanks': 1, 'diameter': 8, 'HRT': 40, 'specific density': 40, 'salinity': 0.003, 'recirc degree': 0.985}
department2_dict = {'number tanks': 2, 'diameter': 8, 'HRT': 40, 'specific density': 50, 'salinity': 0.003, 'recirc degree': 0.985}
department3_dict = {'number tanks': 1, 'diameter': 14, 'HRT': 40, 'specific density': 60, 'salinity': 0.003, 'recirc degree': 0.985}

department_specifications = [department1_dict, department2_dict, department3_dict]
RAS = RAS(department_specifications)


## Specifying the start and end weight in each department 
start_weight_department1 = 5
end_weight_department1 = 30 
start_weight_department2 = 30 #kg 
end_weight_department2 = 100 #g
start_weight_department3 = 100 #g
end_weight_department3 = 168#g 


## Specifying the growth rates, feeding, oxygen consumpttion 
filename = "growth.xlsx"
sheet = 0 
fish1 = Fish(return_fish_dataframe(start_weight_department1, end_weight_department1, filename, sheet),fish_produced)
fish2 = Fish(return_fish_dataframe(start_weight_department2, end_weight_department2, filename, sheet),fish_produced)
fish3 = Fish(return_fish_dataframe(start_weight_department3, end_weight_department3, filename, sheet),fish_produced)

fish1.plot_fish()

## Calculating specific density in each department 

SD_department3 = (fish3.end_total_weight.iloc[-1]/(RAS.department3.volume_tanks*RAS.department3.number_tanks))
SD_department2 = (fish2.end_total_weight.iloc[-1]/(RAS.department2.volume_tanks*RAS.department2.number_tanks))
SD_department1 = (fish1.end_total_weight.iloc[-1]/(RAS.department1.volume_tanks*RAS.department1.number_tanks))

RAS.department1.fish = fish1
RAS.department2.fish = fish2 
RAS.department3.fish = fish3


biomass_production = RAS.department3.fish.end_weight.iloc[-1]*fish_produced
total_energy_use = RAS.total_energy_use()

#Calculating the SEC 
SEC = total_energy_use/(biomass_production)

print("SEC:")
print(SEC)



