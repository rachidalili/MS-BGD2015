import pandas as pandas
import numpy as numpy
from datetime import datetime


time = 'O8-10-1998'
b = datetime.strptime(time, '%d-%m-%y')
print b.year
