# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 10:59:41 2015

@author: Kopipan
"""

import pandas as pd
import numpy as np


read = pd.read_csv("C:/Users/Kopipan/MS-BGD2015/Lessons-Exercices/base-cc-rev-fisc-loc-menage-10.csv")
data = pd.DataFrame(read).dropna()


"COURS SUR PANDAS
"""
pandas.pivot
pandas.melt
pandas value counts
pandas quantization: qcut pd.cut
set: get unique values from a list



"""