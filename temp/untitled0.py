# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:25:10 2019

@author: Andrea Nistad
"""

import pandas as pd 





df = pd.read_excel(filename, sheet_name=0)


    

#df = return_fish_dataframe(5,150,"C:/Users/Andrea Nistad/OneDrive - NTNU/Attachments/Masteroppgave/RAS model/growth.xlsx",0)
    
    
'''def find_neighbours(value):
    exactmatch=df[df.num==value]
    if !exactmatch.empty:
        return exactmatch.index[0]
    else:
        lowerneighbour_ind = df[df.num<value].idxmax()
        upperneighbour_ind = df[df.num>value].idxmin()
        return lowerneighbour_ind, upperneighbour_ind'''