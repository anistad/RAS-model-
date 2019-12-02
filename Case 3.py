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

#Calculating the maximum number of fish 
from IPython import get_ipython
get_ipython().magic('reset -sf') 
runfile("classes.py")

water_temp = 6

fish_produced = 250000


## Specifying the departments to add 

department1_dict = {'number tanks': 0.83, 'diameter': 8, 'HRT': 40, 'specific density': 40, 'salinity': 0.003, 'recirc degree': 0.985}
department2_dict = {'number tanks': 2.49, 'diameter': 8, 'HRT': 40, 'specific density': 50, 'salinity': 0.003, 'recirc degree': 0.985}
department3_dict = {'number tanks': 0.91, 'diameter': 14, 'HRT': 40, 'specific density': 60, 'salinity': 0.003, 'recirc degree': 0.985}
#department4_dict = {'number tanks': 16.24, 'diameter': 14, 'HRT': 40, 'specific density': 70, 'salinity': 0.012, 'recirc degree': 0.985}
department_specifications = [department1_dict, department2_dict, department3_dict]
RAS = RAS(department_specifications)
RAS.department1.print_dimensions()
RAS.department2.print_dimensions()
RAS.department3.print_dimensions()
#RAS.department4.print_dimensions()


## Specifying the fish size and number 
start_weight_department1 = 5
end_weight_department1 = 30 #g 
start_weight_department2 = 30 #kg 
end_weight_department2 = 100 #g
start_weight_department3 = 100 #g
end_weight_department3 = 168#g 
#start_weight_department4 = 500
#end_weight_department4 = 3000


filename = "C:/Users/Andrea Nistad/OneDrive - NTNU/Attachments/Masteroppgave/RAS model/growth.xlsx"
sheet = 0 
fish1 = Fish(return_fish_dataframe(start_weight_department1, end_weight_department1, filename, sheet),fish_produced)
fish2 = Fish(return_fish_dataframe(start_weight_department2, end_weight_department2, filename, sheet),fish_produced)
fish3 = Fish(return_fish_dataframe(start_weight_department3, end_weight_department3, filename, sheet),fish_produced)
#fish4 = Fish(return_fish_dataframe(start_weight_department4, end_weight_department4, filename, sheet),fish_produced)
fish1.plot_fish()

## Calculating specific density in each department 
#SD_department4 = (fish4.end_total_weight.iloc[-1]/(RAS.department4.volume_tanks*RAS.department4.number_tanks))
SD_department3 = (fish3.end_total_weight.iloc[-1]/(RAS.department3.volume_tanks*RAS.department3.number_tanks))
SD_department2 = (fish2.end_total_weight.iloc[-1]/(RAS.department2.volume_tanks*RAS.department2.number_tanks))
SD_department1 = (fish1.end_total_weight.iloc[-1]/(RAS.department1.volume_tanks*RAS.department1.number_tanks))

RAS.department1.fish = fish1
RAS.department2.fish = fish2 
RAS.department3.fish = fish3
#RAS.department4.fish = fish4


biomass_production = RAS.department3.fish.end_weight.iloc[-1]*fish_produced

SEC = abs(RAS.total_energy_use())/(biomass_production)

print("SEC:")
print(SEC)


#print(SD_department4)
print(SD_department3)
print(SD_department2)
print(SD_department1)


print(RAS.department1.volume_tanks*RAS.department1.number_tanks)
print(RAS.department2.volume_tanks*RAS.department2.number_tanks)

print(RAS.department3.volume_tanks*RAS.department3.number_tanks)
#print(RAS.department4.volume_tanks*RAS.department4.number_tanks)

'''
print("distribution")
print(RAS.energy_distribution())
print("specific power")
print(RAS.specific_power())'''



