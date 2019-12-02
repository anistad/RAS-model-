# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 09:29:41 2019

@author: Andrea Nistad
"""

# -*- coding: utf-8 -*-
'''This script calculates a volume and the associated power use and plots it against the data 
available from RAS plants in operation'''


#Calculating the maximum number of fish 
from IPython import get_ipython
get_ipython().magic('reset -sf') 

#def return_flow_power(a, scale):
    
import numpy as np
import seaborn as sns

import pandas as pd 
import matplotlib as plt 
import numpy as np

water_temp = 6

fish_produced = 250000

def run_power(scale):
    global RAS, RAS_test

    runfile("classes.py")
    ## Specifying the departments to add 
    '''The number of tanks required in each department is calculated by dividing 
    the final weight by the specific density in each department '''
    
    
    ## Specifying the fish size and number 
    start_weight_department1 = 5
    end_weight_department1 = 30 #g 
    start_weight_department2 = 30 #kg 
    end_weight_department2 = 100 #g
    start_weight_department3 = 100 #g
    end_weight_department3 = 168#g 
    
    SD_department1 = 40 
    SD_department2 = 50 
    SD_department3 = 60
    
    
    department1_dict = {'number tanks': 1, 'diameter': 8, 'HRT': 40, 'specific density': SD_department1, 'salinity': 0.003, 'recirc degree': 0.985}
    department2_dict = {'number tanks': 1, 'diameter': 8, 'HRT': 40, 'specific density': SD_department2, 'salinity': 0.003, 'recirc degree': 0.985}
    department3_dict = {'number tanks': 1, 'diameter': 14, 'HRT': 40, 'specific density': SD_department3, 'salinity': 0.003, 'recirc degree': 0.985}
    
    
    
    RAS_test = RAS([department1_dict, department2_dict, department3_dict])
    
    def number_tanks(list_of_end_weights, list_of_spec_density, list_of_tank_volumes ): 
        return [((list_of_end_weights[i]/1000)/list_of_spec_density[i]*fish_produced)/list_of_tank_volumes[i] for i in np.arange(len(list_of_end_weights))]
    
    
    number_tanks = number_tanks([end_weight_department1, end_weight_department2, end_weight_department3], 
                               [SD_department1, SD_department2, SD_department3],
                               [RAS_test.department1.volume_tanks, RAS_test.department2.volume_tanks, RAS_test.department3.volume_tanks])
    
    department1_dict = {'number tanks': number_tanks[0]*scale, 'diameter': 8, 'HRT': 40, 'specific density': SD_department1, 'salinity': 0.003, 'recirc degree': 0.985}
    department2_dict = {'number tanks': number_tanks[1]*scale, 'diameter': 8, 'HRT': 40, 'specific density': SD_department2, 'salinity': 0.003, 'recirc degree': 0.985}
    department3_dict = {'number tanks': number_tanks[2]*scale, 'diameter': 14, 'HRT': 40, 'specific density': SD_department3, 'salinity': 0.003, 'recirc degree': 0.985}
    
    RAS = RAS([department1_dict, department2_dict, department3_dict])
    
    
    filename = "C:/Users/Andrea Nistad/OneDrive - NTNU/Attachments/Masteroppgave/RAS model/growth.xlsx"
    sheet = 0 
    fish1 = Fish(return_fish_dataframe(start_weight_department1, end_weight_department1, filename, sheet),fish_produced)
    fish2 = Fish(return_fish_dataframe(start_weight_department2, end_weight_department2, filename, sheet),fish_produced)
    fish3 = Fish(return_fish_dataframe(start_weight_department3, end_weight_department3, filename, sheet),fish_produced)
    
    ## Calculating specific density in each department 
    SD_department3 = (fish3.end_total_weight.iloc[-1]/(RAS.department3.volume_tanks*RAS.department3.number_tanks))
    SD_department2 = (fish2.end_total_weight.iloc[-1]/(RAS.department2.volume_tanks*RAS.department2.number_tanks))
    SD_department1 = (fish1.end_total_weight.iloc[-1]/(RAS.department1.volume_tanks*RAS.department1.number_tanks))
    
    RAS.department1.fish = fish1
    RAS.department2.fish = fish2 
    RAS.department3.fish = fish3
    
    
    
    biomass_production = RAS.department3.fish.end_weight.iloc[-1]*fish_produced
    
    SEC = abs(RAS.total_energy_use())/(biomass_production)
    
    print("SEC:")
    print(SEC)
    
    
    #print(SD_department4)
    print(SD_department3)
    print(SD_department2)
    print(SD_department1)
    
    return (RAS.department1.volume_tanks*RAS.department1.number_tanks + RAS.department2.volume_tanks*RAS.department2.number_tanks + RAS.department3.volume_tanks*RAS.department3.number_tanks), RAS.total_power() 


total_volume = list() #m3/min
total_average_power = list() #kW

for i in [1,3,5,7,9,11,13,15,17]: 
    a,b = run_power(i)
    total_volume.append(a)
    total_average_power.append(b)
    
sns.set()   
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(1,1,1)
ax.scatter(total_volume, total_average_power, label = 'Model', color='g')

## The available data from the plants 
#flow_recirc_data = [315,	315,	488.8888889,	297.7777778,	375,	305.5666667,	144.8275862,	150,	235, 400,	235]
volume_data = [12600,	12600	,22000,	13400	,15000,	11352,	7000,	6000,	9832,	13200,	9800]
average_power_data = [779.2303434,	880.9232117,	1819.405423,	1197.370719,	1302.476173,	742.0150685,	412.2605784,	861.677213	,782.1403963,	782.4247354	,670.5547877]
ax.scatter(volume_data, average_power_data, label='Data', color='black', alpha=0.7)
ax.scatter(23964,	3424.684932, marker = "^",color='black')
ax.scatter(3700, 237.6229055, marker = "^", color="black")
ax.set_ylabel('Average power (kW)', fontsize=14)
ax.set_xlabel('Volume  (m$^3$)', fontsize=14)
ax.legend(frameon=False, fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=13)
fig.tight_layout()

fig.savefig('Model_data_flow_rate_power.png')
