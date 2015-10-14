#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import seaborn
import sklearn
import matplotlib
import matplotlib.pyplot as plt
from sklearn import linear_model
from mpl_toolkits.mplot3d import Axes3D

# 1
dataset = pd.read_csv('http://www.math.uah.edu/stat/data/Galton.txt', delimiter="\t");

print list(dataset.columns.values)

# A2
dataset['MeanParent'] = ((dataset['Father'] + dataset['Mother'] * 1.08)/2.0)

# 3
dataset.plot(kind='scatter', x='MeanParent', y='Height')


# 4
x_train = []
for e in dataset['MeanParent']:
	x_train.append([e])
y_train = []
for e in dataset['Height']:
	y_train.append([e])
linear = linear_model.LinearRegression()
linear.fit(x_train, y_train)
linear.score(x_train, y_train)

# 5
plt.figure()
plt.plot(x_train, linear.predict(x_train), label='Prediction')
plt.plot(x_train, x_train*linear.coef_ + linear.intercept_, label='Coef')
plt.scatter(dataset['MeanParent'], dataset['Height'])
plt.legend()



# 6
plt.figure()
residus = y_train - linear.predict(x_train)
plt.hist(residus)



# 7
linearBis = linear_model.LinearRegression()
linearBis.fit(y_train, x_train)
plt.figure()
plt.plot(y_train, linearBis.predict(y_train), label='Prediction')
plt.plot(x_train, linear.predict(x_train), label='Prediction')

# Les droites sont symétriques par rapport à la bissectrice

var_x = dataset['MeanParent'].var(axis=1)
var_y = dataset['Height'].var(axis=1)
mean_x = dataset['MeanParent'].mean(axis=1)
mean_y = dataset['Height'].mean(axis=1)

other_alpha0 = mean_x + (mean_y * var_x * (linear.intercept_ - mean_y)) / (mean_x * var_y)
print "Check for alpha0 and theta0 : " + str(other_alpha0) + "," + str(linearBis.intercept_)

other_alpha1 = var_x * linear.coef_ / var_y
print "Check for alpha1 and theta1 : " + str(other_alpha1) + "," + str(linearBis.coef_)



# 8
print "\n\n========== Linear Multiple ==========\n"
x_train = dataset[['Father','Mother']]
linearMult = linear_model.LinearRegression()
linearMult.fit(x_train, y_train)
print "Theta0 : " + str(linearMult.intercept_[0]) + ", theta1 : " + str(linearMult.coef_[0][0]) + ", theta2 : " + str(linearMult.coef_[0][1])

# 9
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(dataset['Father'], dataset['Mother'], y_train)

# Pour un plan 3D : On doit créer une grille de référence à afficher pour les X et Y, puis calculer le Z en fonction
XX = np.arange(50, 80, 0.5)
YY = np.arange(50, 80, 0.5)
xx, yy = np.meshgrid(XX, YY)
dataTmp = np.column_stack((xx, yy))
zz = linearMult.intercept_[0] + linearMult.coef_[0][0] * xx + linearMult.coef_[0][1] * yy
zz = linearMult.predict(dataTmp)
ax.plot_wireframe(xx, yy, zz, rstride=10, cstride=10, alpha=0.3)
plt.show()


# 10
residus = y_train - linearMult.predict(x_train)
print "Norme des résidus : " + str(np.linalg.norm(residus))
plt.figure()
plt.hist(residus)
plt.show()


# 11
print "Covariance Father/Height : " + str(np.cov(dataset['Father'], dataset['Height'])[0][1])
print "Covariance Mother/Height : " + str(np.cov(dataset['Mother'], dataset['Height'])[0][1])
datasetNormalized = {}
datasetNormalized['Father'] = sklearn.preprocessing.scale(dataset['Father']) # It's like : (dataset['Father'] - dataset['Father'].mean(axis=1)) / np.sqrt(dataset['Father'].var(axis=1))
datasetNormalized['Mother'] = sklearn.preprocessing.scale(dataset['Mother'])
datasetNormalized['Height'] = sklearn.preprocessing.scale(dataset['Height'])
print "Covariance FatherNormalized/Height : " + str(np.cov(datasetNormalized['Father'], datasetNormalized['Height'])[0][1])
print "Covariance MotherNormalized/Height : " + str(np.cov(datasetNormalized['Mother'], datasetNormalized['Height'])[0][1])
