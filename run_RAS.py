# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 15:05:23 2019

@author: Andrea Nistad
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:51:31 2019

@author: Andrea Nistad
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:15:51 2019

@author: Andrea Nistad
"""

#Calculating the maximum number of fish 
from IPython import get_ipython
get_ipython().magic('reset -sf') 

#def return_flow_power(a, scale):
    
import numpy as np
import seaborn as sns
import random 


import pandas as pd 
import matplotlib as plt 
import numpy as np


''' This scripts simulate the RAS described in the Master's Thesis report. The batch size is 150 000
    based on the stocking density, the dimensions of the system is calculated - and it is thereafter checked that 
    the stocking density is within the specificed limits. Then energy use is calculated in each department, and finally for the 
    total RAS over the production period from start weight to the final weight '''

fish_produced=150000


def calculate_SEC(end_weight,list_spec_dens, list_recirc_deg, list_HRT):
    global RAS, RAS_test

    runfile("classes.py")
    filename = "growth.xlsx"
    sheet = 0 
   

    ## Specifying the departments to add 
    '''The number of tanks required in each department is calculated by dividing 
    the final weight by the specific density in each department '''
    
    
    ## Specifying the fish size and number 
    start_weight_department1 = 5
    end_weight_department1 = 30 #g 
    start_weight_department2 = 30 #kg 
    end_weight_department2 = 100 #g
    start_weight_department3 = 100 #g
    
    if end_weight > 175:
        salinity_department3 = 0.012
    else: 
        salinity_department3 =0.003 
    
    department1_dict = {'number tanks': 1, 'diameter': 8, 'HRT': list_HRT[0], 'specific density': list_spec_dens[0], 'salinity': 0.003, 'recirc degree': list_recirc_deg[0]}
    department2_dict = {'number tanks': 1, 'diameter': 8, 'HRT': list_HRT[1], 'specific density': list_spec_dens[1], 'salinity': 0.003, 'recirc degree': list_recirc_deg[1]}
    department3_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[2], 'specific density': list_spec_dens[2], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[2]}
    
    if end_weight <= 500: 
        end_weight_department3 = end_weight
        RAS_test = RAS([department1_dict, department2_dict, department3_dict])
        
        #Calculating the number of tanks needed in order to produce the fish with the specified specific density 
        no_tanks = number_tanks([end_weight_department1, end_weight_department2, end_weight_department3], 
                               list_spec_dens,
                               [RAS_test.department1.volume_tanks, RAS_test.department2.volume_tanks, RAS_test.department3.volume_tanks], fish_produced)
        
        department1_dict = {'number tanks': no_tanks[0], 'diameter': 8, 'HRT': list_HRT[0], 'specific density': list_spec_dens[0], 'salinity': 0.003, 'recirc degree': list_recirc_deg[0]}
        department2_dict = {'number tanks': no_tanks[1], 'diameter': 8, 'HRT': list_HRT[1], 'specific density': list_spec_dens[1], 'salinity': 0.003, 'recirc degree': list_recirc_deg[1]}
        department3_dict = {'number tanks': no_tanks[2], 'diameter': 14, 'HRT': list_HRT[2], 'specific density': list_spec_dens[2], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[2]}
    
        RAS = RAS([department1_dict, department2_dict, department3_dict])

        fish1 = Fish(return_fish_dataframe(start_weight_department1, end_weight_department1, filename, sheet),fish_produced)
        fish2 = Fish(return_fish_dataframe(start_weight_department2, end_weight_department2, filename, sheet),fish_produced)
        fish3 = Fish(return_fish_dataframe(start_weight_department3, end_weight_department3, filename, sheet),fish_produced)

        ## Calculating specific density in each department 
        SD_department3 = (fish3.end_total_weight.iloc[-1]/(RAS.department3.volume_tanks*RAS.department3.number_tanks))
        SD_department2 = (fish2.end_total_weight.iloc[-1]/(RAS.department2.volume_tanks*RAS.department2.number_tanks))
        SD_department1 = (fish1.end_total_weight.iloc[-1]/(RAS.department1.volume_tanks*RAS.department1.number_tanks))

        # Check if the specific density is within bounds
        if SD_department3 < list_spec_dens[2]-5 or SD_department3 > list_spec_dens[2] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department2 < list_spec_dens[1]-5 or SD_department2 > list_spec_dens[1] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department1 < list_spec_dens[0]-5 or SD_department1 > list_spec_dens[0] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        
        else: 
            RAS.department1.fish = fish1
            RAS.department2.fish = fish2 
            RAS.department3.fish = fish3
        
        biomass_production = RAS.departments[-1].fish.end_weight.iloc[-1]*fish_produced
    
        return abs(RAS.total_energy_use())/biomass_production
                
    if 500 < end_weight <=1500: 
        end_weight_department3 = 500
        start_weight_department4 = 500
        end_weight_department4 = end_weight 
        
        department1_dict = {'number tanks': 1, 'diameter': 8, 'HRT': list_HRT[0], 'specific density': list_spec_dens[0], 'salinity': 0.003, 'recirc degree': list_recirc_deg[0]}
        department2_dict = {'number tanks': 1, 'diameter': 8, 'HRT': list_HRT[1], 'specific density': list_spec_dens[1], 'salinity': 0.003, 'recirc degree': list_recirc_deg[1]}
        department3_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[2], 'specific density': list_spec_dens[2], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[2]}
        department4_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[3], 'specific density': list_spec_dens[3], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[3]}
            
        RAS_test = RAS([department1_dict, department2_dict, department3_dict, department4_dict])
            
        no_tanks = number_tanks([end_weight_department1, end_weight_department2, end_weight_department3, end_weight_department4], 
                                    list_spec_dens,
                                    [RAS_test.department1.volume_tanks, RAS_test.department2.volume_tanks, RAS_test.department3.volume_tanks, RAS_test.department4.volume_tanks], fish_produced)
          
        department1_dict = {'number tanks': no_tanks[0], 'diameter': 8, 'HRT': list_HRT[0], 'specific density': list_spec_dens[0], 'salinity': 0.003, 'recirc degree': list_recirc_deg[0]}
        department2_dict = {'number tanks': no_tanks[1], 'diameter': 8, 'HRT': list_HRT[1], 'specific density': list_spec_dens[1], 'salinity': 0.003, 'recirc degree': list_recirc_deg[1]}
        department3_dict = {'number tanks': no_tanks[2], 'diameter': 14, 'HRT': list_HRT[2], 'specific density': list_spec_dens[2], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[2]}
        department4_dict = {'number tanks': no_tanks[3], 'diameter': 14, 'HRT': list_HRT[3], 'specific density': list_spec_dens[3], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[3]}
        
        
        RAS = RAS([department1_dict, department2_dict, department3_dict, department4_dict])
        
        fish1 = Fish(return_fish_dataframe(start_weight_department1, end_weight_department1, filename, sheet),fish_produced)
        fish2 = Fish(return_fish_dataframe(start_weight_department2, end_weight_department2, filename, sheet),fish_produced)
        fish3 = Fish(return_fish_dataframe(start_weight_department3, end_weight_department3, filename, sheet),fish_produced)
        fish4 = Fish(return_fish_dataframe(start_weight_department4, end_weight_department4, filename, sheet),fish_produced)
    
        ## Calculating specific density in each department 
        SD_department4 = (fish4.end_total_weight.iloc[-1]/(RAS.department4.volume_tanks*RAS.department4.number_tanks))
        SD_department3 = (fish3.end_total_weight.iloc[-1]/(RAS.department3.volume_tanks*RAS.department3.number_tanks))
        SD_department2 = (fish2.end_total_weight.iloc[-1]/(RAS.department2.volume_tanks*RAS.department2.number_tanks))
        SD_department1 = (fish1.end_total_weight.iloc[-1]/(RAS.department1.volume_tanks*RAS.department1.number_tanks))
       
        # Check if the specific density is within bounds
        if SD_department4 < list_spec_dens[3]-7 or SD_department4 > list_spec_dens[3] + 7: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
            
        if SD_department3 < list_spec_dens[2]-7 or SD_department3 > list_spec_dens[2] + 7: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department2 < list_spec_dens[1]-5 or SD_department2 > list_spec_dens[1] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department1 < list_spec_dens[0]-5 or SD_department1 > list_spec_dens[0] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        
        else: 
            RAS.department1.fish = fish1
            RAS.department2.fish = fish2 
            RAS.department3.fish = fish3
            RAS.department4.fish = fish4
            
        
        biomass_production = RAS.departments[-1].fish.end_weight.iloc[-1]*fish_produced
    
        return abs(RAS.total_energy_use())/biomass_production

    if 1500 < end_weight <= 2500: 
        end_weight_department3 = 500
        start_weight_department4 = 500
        end_weight_department4 = 1500
        start_weight_department5 = 1500
        end_weight_department5 = end_weight
        
        department1_dict = {'number tanks': 1, 'diameter': 8, 'HRT': list_HRT[0], 'specific density': list_spec_dens[0], 'salinity': 0.003, 'recirc degree': list_recirc_deg[0]}
        department2_dict = {'number tanks': 1, 'diameter': 8, 'HRT': list_HRT[1], 'specific density': list_spec_dens[1], 'salinity': 0.003, 'recirc degree': list_recirc_deg[1]}
        department3_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[2], 'specific density': list_spec_dens[2], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[2]}
        department4_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[3], 'specific density': list_spec_dens[3], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[3]}
        department5_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[4], 'specific density': list_spec_dens[4], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[4]}
           
        RAS_test = RAS([department1_dict, department2_dict, department3_dict, department4_dict, department5_dict])
            
        no_tanks = number_tanks([end_weight_department1, end_weight_department2, end_weight_department3, end_weight_department4, end_weight_department5], 
                                    list_spec_dens,
                                    [RAS_test.department1.volume_tanks, RAS_test.department2.volume_tanks, RAS_test.department3.volume_tanks, RAS_test.department4.volume_tanks, RAS_test.department5.volume_tanks], fish_produced)
          
        department1_dict = {'number tanks': no_tanks[0], 'diameter': 8, 'HRT': list_HRT[0], 'specific density': list_spec_dens[0], 'salinity': 0.003, 'recirc degree': list_recirc_deg[0]}
        department2_dict = {'number tanks': no_tanks[1], 'diameter': 8, 'HRT': list_HRT[1], 'specific density': list_spec_dens[1], 'salinity': 0.003, 'recirc degree': list_recirc_deg[1]}
        department3_dict = {'number tanks': no_tanks[2], 'diameter': 14, 'HRT': list_HRT[2], 'specific density': list_spec_dens[2], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[2]}
        department4_dict = {'number tanks': no_tanks[3], 'diameter': 14, 'HRT': list_HRT[3], 'specific density': list_spec_dens[3], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[3]}
        department5_dict = {'number tanks': no_tanks[4], 'diameter': 14, 'HRT': list_HRT[4], 'specific density': list_spec_dens[4], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[4]}

        
        RAS = RAS([department1_dict, department2_dict, department3_dict, department4_dict, department5_dict])
        
        fish1 = Fish(return_fish_dataframe(start_weight_department1, end_weight_department1, filename, sheet),fish_produced)
        fish2 = Fish(return_fish_dataframe(start_weight_department2, end_weight_department2, filename, sheet),fish_produced)
        fish3 = Fish(return_fish_dataframe(start_weight_department3, end_weight_department3, filename, sheet),fish_produced)
        fish4 = Fish(return_fish_dataframe(start_weight_department4, end_weight_department4, filename, sheet),fish_produced)
        fish5 = Fish(return_fish_dataframe(start_weight_department5, end_weight_department5, filename, sheet),fish_produced)
    
        
        ## Calculating specific density in each department 
        SD_department5 = (fish5.end_total_weight.iloc[-1]/(RAS.department5.volume_tanks*RAS.department5.number_tanks))
        SD_department4 = (fish4.end_total_weight.iloc[-1]/(RAS.department4.volume_tanks*RAS.department4.number_tanks))
        SD_department3 = (fish3.end_total_weight.iloc[-1]/(RAS.department3.volume_tanks*RAS.department3.number_tanks))
        SD_department2 = (fish2.end_total_weight.iloc[-1]/(RAS.department2.volume_tanks*RAS.department2.number_tanks))
        SD_department1 = (fish1.end_total_weight.iloc[-1]/(RAS.department1.volume_tanks*RAS.department1.number_tanks))
    
        # Check if the specific density is within bounds
        if SD_department5 < list_spec_dens[4]-10 or SD_department4 > list_spec_dens[4] + 10: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department4 < list_spec_dens[3]-5 or SD_department4 > list_spec_dens[3] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
            
        if SD_department3 < list_spec_dens[2]-5 or SD_department3 > list_spec_dens[2] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department2 < list_spec_dens[1]-5 or SD_department2 > list_spec_dens[1] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department1 < list_spec_dens[0]-5 or SD_department1 > list_spec_dens[0] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        
        else: 
            RAS.department1.fish = fish1
            RAS.department2.fish = fish2 
            RAS.department3.fish = fish3
            RAS.department4.fish = fish4
            RAS.department5.fish = fish5
            
        biomass_production = RAS.departments[-1].fish.end_weight.iloc[-1]*fish_produced
    
        return abs(RAS.total_energy_use())/biomass_production
    
    if end_weight > 2500: 
        end_weight_department3 = 500
        start_weight_department4 = 500
        end_weight_department4 = 1500
        start_weight_department5 = 1500
        end_weight_department5 = 2500
        start_weight_department6 = 2500
        end_weight_department6 = end_weight
        
        department1_dict = {'number tanks': 1, 'diameter': 8, 'HRT': list_HRT[0], 'specific density': list_spec_dens[0], 'salinity': 0.003, 'recirc degree': list_recirc_deg[0]}
        department2_dict = {'number tanks': 1, 'diameter': 8, 'HRT': list_HRT[1], 'specific density': list_spec_dens[1], 'salinity': 0.003, 'recirc degree': list_recirc_deg[1]}
        department3_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[2], 'specific density': list_spec_dens[2], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[2]}
        department4_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[3], 'specific density': list_spec_dens[3], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[3]}
        department5_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[4], 'specific density': list_spec_dens[4], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[4]}
        department6_dict = {'number tanks': 1, 'diameter': 14, 'HRT': list_HRT[5], 'specific density': list_spec_dens[5], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[5]}
        
        RAS_test = RAS([department1_dict, department2_dict, department3_dict, department4_dict, department5_dict, department6_dict])
            
        no_tanks = number_tanks([end_weight_department1, end_weight_department2, end_weight_department3, end_weight_department4, end_weight_department5, end_weight_department6], 
                                    list_spec_dens,
                                    [RAS_test.department1.volume_tanks, RAS_test.department2.volume_tanks, RAS_test.department3.volume_tanks, RAS_test.department4.volume_tanks, RAS_test.department5.volume_tanks, RAS_test.department6.volume_tanks], fish_produced)
          
        department1_dict = {'number tanks': no_tanks[0], 'diameter': 8, 'HRT': list_HRT[0], 'specific density': list_spec_dens[0], 'salinity': 0.003, 'recirc degree': list_recirc_deg[0]}
        department2_dict = {'number tanks': no_tanks[1], 'diameter': 8, 'HRT': list_HRT[1], 'specific density': list_spec_dens[1], 'salinity': 0.003, 'recirc degree': list_recirc_deg[1]}
        department3_dict = {'number tanks': no_tanks[2], 'diameter': 14, 'HRT': list_HRT[2], 'specific density': list_spec_dens[2], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[2]}
        department4_dict = {'number tanks': no_tanks[3], 'diameter': 14, 'HRT': list_HRT[3], 'specific density': list_spec_dens[3], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[3]}
        department5_dict = {'number tanks': no_tanks[4], 'diameter': 14, 'HRT': list_HRT[4], 'specific density': list_spec_dens[4], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[4]}
        department6_dict = {'number tanks': no_tanks[5], 'diameter': 14, 'HRT': list_HRT[5], 'specific density': list_spec_dens[5], 'salinity': salinity_department3, 'recirc degree': list_recirc_deg[5]}

        
        RAS = RAS([department1_dict, department2_dict, department3_dict, department4_dict, department5_dict, department6_dict])
        
        fish1 = Fish(return_fish_dataframe(start_weight_department1, end_weight_department1, filename, sheet),fish_produced)
        fish2 = Fish(return_fish_dataframe(start_weight_department2, end_weight_department2, filename, sheet),fish_produced)
        fish3 = Fish(return_fish_dataframe(start_weight_department3, end_weight_department3, filename, sheet),fish_produced)
        fish4 = Fish(return_fish_dataframe(start_weight_department4, end_weight_department4, filename, sheet),fish_produced)
        fish5 = Fish(return_fish_dataframe(start_weight_department5, end_weight_department5, filename, sheet),fish_produced)
        fish6 = Fish(return_fish_dataframe(start_weight_department6, end_weight_department6, filename, sheet),fish_produced)
    
        
        ## Calculating specific density in each department 
        SD_department6 = (fish6.end_total_weight.iloc[-1]/(RAS.department6.volume_tanks*RAS.department6.number_tanks))
        SD_department5 = (fish5.end_total_weight.iloc[-1]/(RAS.department5.volume_tanks*RAS.department5.number_tanks))
        SD_department4 = (fish4.end_total_weight.iloc[-1]/(RAS.department4.volume_tanks*RAS.department4.number_tanks))
        SD_department3 = (fish3.end_total_weight.iloc[-1]/(RAS.department3.volume_tanks*RAS.department3.number_tanks))
        SD_department2 = (fish2.end_total_weight.iloc[-1]/(RAS.department2.volume_tanks*RAS.department2.number_tanks))
        SD_department1 = (fish1.end_total_weight.iloc[-1]/(RAS.department1.volume_tanks*RAS.department1.number_tanks))
        
                
        # Check if the specific density is within bounds
        if SD_department6 < list_spec_dens[5]-5 or SD_department6 > list_spec_dens[5] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0          
        if SD_department5 < list_spec_dens[4]-10 or SD_department5 > list_spec_dens[4] + 10: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department4 < list_spec_dens[3]-5 or SD_department4 > list_spec_dens[3] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
            
        if SD_department3 < list_spec_dens[2]-5 or SD_department3 > list_spec_dens[2] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department2 < list_spec_dens[1]-5 or SD_department2 > list_spec_dens[1] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        if SD_department1 < list_spec_dens[0]-5 or SD_department1 > list_spec_dens[0] + 5: 
            print("Something wrong in calculation of number of tanks/specific density")
            return 0
        
        else: 
            RAS.department1.fish = fish1
            RAS.department2.fish = fish2 
            RAS.department3.fish = fish3
            RAS.department4.fish = fish4
            RAS.department5.fish = fish5
            RAS.department6.fish = fish6
            
        biomass_production = RAS.departments[-1].fish.end_weight.iloc[-1]*fish_produced

        return abs(RAS.total_energy_use())/biomass_production
    
    
    
    
    
all_results = list()

## The resulting SEC is calculated for the following fish end weight 
weight = [171, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500,2750,3000,3250,3500,3750, 4000]
weight=[4000]

# This command ensures that the same random numbers are picked each time
random.seed(3) 
# The number of samples to run 
num_samples = 100
results_HRT = list()
results_SD = list()
results_recirc_degree = list()
for i in np.arange(num_samples): 
    results = list()
    
    # The water temperature is set to vary uniformly between 4 and 10 C 
    water_temp = random.uniform(4,10)
    
    # Defining the maximum stocking density in each department 
    SD1 = [45,50,65]
   # SD1 = [65,65,65]
    # The reciruclation degree is set to vary uniformly between 97.% % and 99.8% 
    recirc_degree1 = [random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998)]
    
    # Defining HRT in each department 
    HRT1 = [40,40,40]
    
    SD2 = [45,50,65,65]
    #SD2 = [45,50,65,50]
    #SD2 = [45,50,85,85]
    recirc_degree2 = [random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998)]
    
    HRT2 = [40,40,40,30]
    
    SD3 = [45,50,65,65,65]
    #SD3 = [45,50,85,85,85]
   # SD3 = [33,33,33,33,33]
    recirc_degree3 = [random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998)]
    
    HRT3 = [40,40,40,30,30]
    
    #SD4 = [33,33,33,33,33,33]
    SD4 = [45,50,65,65,65,65]
    #SD4 = [45,50,75,85,85,85]
    recirc_degree4 = [random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998),random.uniform(0.975,0.998)]
    HRT4 = [40,40,40,30,30,30]
    
    
    for w in weight:
        if w <= 500: 
            results.append(calculate_SEC(w, SD1, recirc_degree1, HRT1))  
            results_HRT.append(HRT1)
            results_recirc_degree.append(recirc_degree1)
        if w > 500 and w <= 1500:    
            results.append(calculate_SEC(w, SD2, recirc_degree2, HRT2))
            results_HRT.append(HRT2)
            results_recirc_degree.append(recirc_degree2)
        if w > 1500 and w <=2500: 
            results.append(calculate_SEC(w, SD3, recirc_degree3, HRT3))
            results_HRT.append(HRT3)
            results_recirc_degree.append(recirc_degree3)
        if w > 2500: 
            results.append(calculate_SEC(w,SD4,recirc_degree4,HRT4))
            results_HRT.append(HRT4)
            results_recirc_degree.append(recirc_degree4)
        
                
    all_results.append(results)
    
    
# Returns the SEC for all weights 
df = pd.DataFrame(all_results).T

    
    
