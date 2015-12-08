# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:48:21 2015

@author: florian
"""

import pandas as pd

def pays(campaign):
    if "US" in campaign:
        return "USA"
    if "BR" in campaign:
        return "BRESIL" 
    if "UK" in campaign:
        return "Grande Bretagne"
        
#mkt = pd.read_excel("exo.xls",skiprows=[0,1,2,3,4,5,6,7,8,9,10])
#mkt['campaign']=mkt['campaign'].str.replace(r'','')
        
        

