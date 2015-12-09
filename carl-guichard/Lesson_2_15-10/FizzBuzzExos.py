# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:43:51 2015

@author: Carl
"""

def fizbuzz():
    for i in range (1,101):
        if i%3 == 0 and i%5 == 0:
            print ("fizzbuzz")
        elif i%3 == 0:
            print ("fizz")
        elif i%5 == 0:
            print("buzz")
        else:
            print (i)
    return
    
    
fizbuzz()