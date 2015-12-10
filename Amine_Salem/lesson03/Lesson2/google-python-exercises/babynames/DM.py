import numpy as np
import statsmodels as sm
from statsmodels import datasets
import pandas
import csv
from sklearn import linear_model

data = sm.datasets.get_rdataset(
    'airquality', package="datasets", cache=False)


