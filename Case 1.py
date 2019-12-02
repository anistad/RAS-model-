# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 13:58:38 2019

@author: Andrea Nistad
"""

#Calculating the maximum number of fish 

from IPython import get_ipython
get_ipython().magic('reset -sf') 
runfile("classes.py")


water_temp = 6
## Specifying the departments to add 

department1_dict = {'number tanks': 1, 'diameter': 9, 'HRT': 40, 'specific density': 50, 'salinity': 0.003, 'recirc degree': 0.985}
department2_dict = {'number tanks': 1, 'diameter': 14, 'HRT': 40, 'specific density': 60, 'salinity': 0.003, 'recirc degree': 0.985}
#department2_dict = {'number tanks': 1, 'diameter': 14, 'HRT': 40, 'specific density': 60, 'salinity': 0.03, 'recirc degree': 0.985}
department_specifications = [department1_dict, department2_dict]
RAS = RAS(department_specifications)
RAS.department1.print_dimensions()
RAS.department2.print_dimensions()
#RAS.department3.print_dimensions()

## Specifying the fish size and number 
start_weight_department1 = 5
end_weight_department1 = 50 #g 
start_weight_department2 = 50 #kg 
end_weight_department2 = 168 #g
filename = "C:/Users/Andrea Nistad/OneDrive - NTNU/Attachments/Masteroppgave/RAS model/growth.xlsx"
sheet = 0 
no_fish = 1
fish1 = Fish(return_fish_dataframe(start_weight_department1, end_weight_department1, filename, sheet),no_fish)
fish2 = Fish(return_fish_dataframe(start_weight_department2, end_weight_department2, filename, sheet),no_fish)

fish1.plot_fish()

## Calculating the maximum number of fish in each department
max_fish_dep1 = max_number_of_fish(fish1,end_weight_department1, RAS.department1) 
max_fish_dep2 = max_number_of_fish(fish2,end_weight_department2, RAS.department2)

if (max_fish_dep2/max_fish_dep1) <= 0.8: 
    print("HAVE TO ADD SOME TANKS TO THE LAST DEPARTMENTS??")
    
    
fish_produced = max_fish_dep2

RAS.department1.fish = Fish(return_fish_dataframe(start_weight_department1, end_weight_department1, filename, sheet),fish_produced)
RAS.department2.fish = Fish(return_fish_dataframe(start_weight_department2, end_weight_department2, filename, sheet),fish_produced)
#RAS.department3.fish = Fish(filename,2,fish_produced)

biomass_production = RAS.department2.fish.end_weight.iloc[-1]*fish_produced

SEC = RAS.total_energy_use()/biomass_production

print("SEC:")
print(SEC)
'''
print("distribution")
print(RAS.energy_distribution())
print("specific power")
print(RAS.specific_power()'''




