# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:25:50 2015

@author: Kopipan
"""

import requests
from bs4 import BeautifulSoup
import urllib2, base64
import operator
import json
import pandas as pd
import numpy as np
from Tkinter import *

#Importation du csv#

dataset = pd.read_csv("C:\Users\Kopipan\MS-BGD2015\Lessons-Exercices/villes.csv")
#use google client#
