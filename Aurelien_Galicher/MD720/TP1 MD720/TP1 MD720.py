# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 13:50:20 2015

@author: galicher
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn import linear_model
import seaborn as sns
from os import mkdir, path
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
from sklearn import preprocessing

rc('font', **{'family': 'sans-serif', 'sans-serif': ['Computer Modern Roman']})
params = {'axes.labelsize': 12,
          'font.size': 12,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True,
          'figure.figsize': (8, 6)}
plt.rcParams.update(params)
plt.close("all")

sns.set_context("poster")
sns.set_palette("colorblind")
sns.axes_style()
sns.set_style({'legend.frameon': True})
color_blind_list = sns.color_palette("colorblind", 8)
my_orange = color_blind_list[2]
my_green = color_blind_list[1]

## lecture du fichier et création du datframe
data= pd.read_csv('http://www.math.uah.edu/stat/data/Galton.txt',delimiter='\t')
#print data
#print data[['Father']]
#print data[['Mother']]
#MeanParents= pd.add(data[['Father']],data[['Mother']])

## Création de la variable 'MeanParents'
data.loc[:,'MeanParents']= 0.5*(data['Father']+1.05*data['Mother'])
print data

## Création du graphique

## définition de y et X
y = data['Height']
X = data[['MeanParents']]  # beware dat['speed'].shape = (50,), issue with sklearn
# X = dat.drop(['dist', 'Unnamed: 0'], axis=1)  # also ok
n_sample, _ = X.shape
###############################################################################
# data only

xlabels = 'Height MeanParents'
ylabels = 'Height Kid'

fig1 = plt.figure(figsize=(8, 6))
plt.xlabel(xlabels)
plt.ylabel(ylabels)
plt.title('Raw data')
plt.plot(X, y, 'o', label="Data", markeredgecolor='k', markeredgewidth=1)
axes = plt.gca()
#plt.xlim(xmin=0, xmax=30)
#plt.ylim(ymin=-30, ymax=140)

plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display
plt.tight_layout()
plt.show()

## Régression linéraire
skl_linmod = linear_model.LinearRegression()
skl_linmod.fit(X, y)
print skl_linmod.get_params()
theta1= skl_linmod.coef_
theta0= skl_linmod.intercept_

print 'theta1 : %s' % theta1
print 'theta0 : %s' % theta0

fig = plt.figure(figsize=(8, 6))
#plt.xlim(xmin=0, xmax=30)
#plt.ylim(ymin=-30, ymax=140)
plt.plot(X, y, 'o', label="Data", markeredgecolor='k', markeredgewidth=1)
X_to_predict = np.linspace(62.0, 76.0, num=50).reshape(50, 1)
X_to_predict = pd.DataFrame(X_to_predict, columns=['Height Kid'])

plt.plot(X_to_predict, skl_linmod.predict(X_to_predict),
         linewidth=3, label="OLS-sklearn-with-inter")
plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display
plt.xlabel(xlabels), plt.ylabel(ylabels)
plt.title('Raw data (MeanParents) and fitted')
plt.tight_layout()
plt.show()

## résiduals
fig = plt.figure(figsize=(8, 6))
plt.xlim(xmin=62, xmax=76)
plt.ylim(ymin=-12, ymax=12)

residuals= y - skl_linmod.predict(X)
#print residuals

plt.plot(X, residuals, 'o', label="Data", markeredgecolor='b', markeredgewidth=1)

plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display
plt.xlabel(xlabels), plt.ylabel(ylabels)
plt.title('Raw data and residuals fitted')
ylabels = 'residuals'
plt.tight_layout()
plt.show()

###histogram résiduals
#
#plt.hist(residuals['Height'])
#plt.title("Residual Histogram")
#plt.show()

###############################################################################
# Histogram residuals

fig = plt.figure(figsize=(8, 6))
plt.hist(residuals, bins=50, normed=True, align='mid')
sns.kdeplot(residuals)
plt.title('Residual Histogram/ KDE (y=f(X))')
ax = plt.gca()
ax.legend_ = None
plt.xlabel('Residual value'), plt.ylabel('Frequency')
plt.tight_layout()
plt.show()


#question 7
y = data['MeanParents']
X = data[['Height']]
xlabels = 'Height Kid'
ylabels = 'Height MeanParents'
skl_linmodinv = linear_model.LinearRegression()
skl_linmodinv.fit(X, y)
print skl_linmodinv.get_params()
alpha1= skl_linmodinv.coef_
alpha0= skl_linmodinv.intercept_

print 'alpha1 : %s' % alpha1
print 'alpha0 : %s' % alpha0

fig = plt.figure(figsize=(8, 6))
#plt.xlim(xmin=0, xmax=30)
#plt.ylim(ymin=-30, ymax=140)
plt.plot(X, y, 'o', label="Data", markeredgecolor='k', markeredgewidth=1)
X_to_predict = np.linspace(62.0, 76.0, num=50).reshape(50, 1)
X_to_predict = pd.DataFrame(X_to_predict, columns=['MeanParents'])

plt.plot(X_to_predict, skl_linmodinv.predict(X_to_predict),
         linewidth=3, label="OLS-sklearn-with-inter")
plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display
plt.xlabel(xlabels), plt.ylabel(ylabels)
plt.title('Raw data and fitted')
plt.tight_layout()
plt.show()

## résiduals
fig = plt.figure(figsize=(8, 6))
plt.xlim(xmin=62, xmax=76)
plt.ylim(ymin=-12, ymax=12)

residuals= y - skl_linmodinv.predict(X)
#print residuals

plt.plot(X, residuals, 'o', label="Data", markeredgecolor='b', markeredgewidth=1)

plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display
plt.xlabel(xlabels), plt.ylabel(ylabels)
plt.title('Raw data and residuals fitted')
ylabels = 'residuals'
plt.tight_layout()
plt.show()

###histogram résiduals
#
#plt.hist(residuals['Height'])
#plt.title("Residual Histogram")
#plt.show()

###############################################################################
# Histogram residuals

fig = plt.figure(figsize=(8, 6))
plt.hist(residuals, bins=50, normed=True, align='mid')
sns.kdeplot(residuals)
plt.title('Residual Histogram/ KDE X = f(y)')
ax = plt.gca()
ax.legend_ = None
plt.xlabel('Residual value'), plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

### comparaison numérique
y = data['Height']
X = data[['MeanParents']]
#print theta0[0]
testalpha0= np.mean(X['MeanParents']) + np.mean(y)/np.mean(X['MeanParents'])*np.var(X['MeanParents'])/np.var(y)*(theta0-np.mean(y))
testalpha1= np.var(X['MeanParents'])/np.var(y)*theta1[0]
print ('alpha0: %s and testaplpha0: %s' % (alpha0,testalpha0))
print ('alpha1: %s and testalpha1: %s' % (alpha1[0], testalpha1))

#question 8
## définition de y et X
y = data['Height']
X = data[['Father','Mother']]  # beware dat['speed'].shape = (50,), issue with sklearn
# X = dat.drop(['dist', 'Unnamed: 0'], axis=1)  # also ok
n_sample, _ = X.shape
###############################################################################
# data only

xlabels = 'Height MeanParents'
ylabels = 'Height Kid'

fig1 = plt.figure(figsize=(8, 6))
plt.xlabel(xlabels)
plt.ylabel(ylabels)
plt.title('Raw data')
plt.plot(X, y, 'o', label="Data", markeredgecolor='k', markeredgewidth=1)
axes = plt.gca()
#plt.xlim(xmin=0, xmax=30)
#plt.ylim(ymin=-30, ymax=140)

plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display
plt.tight_layout()
plt.show()

## Régression linéraire
skl_linmod = linear_model.LinearRegression()
skl_linmod.fit(X, y)
print skl_linmod.get_params()
alpha1= skl_linmod.coef_
aplha0= skl_linmod.intercept_
print 'alpha1 : %s' % alpha1
print 'alpha0 : %s' % alpha0

#3D plot

XX = np.arange(55, 80, 0.5)
YY = np.arange(55, 80, 0.5)
xx, yy = np.meshgrid(XX, YY)
zz = alpha1[0] * xx + alpha1[1]* yy + alpha0
#print zz
#
#
fig = plt.figure()
sns.set_context("poster")
sns.set_palette("colorblind")
ax = Axes3D(fig)
#
ax.plot(X['Father'], X['Mother'], y, 'o')
ax.set_zlim(55, 80)
ax.set_xlabel('Height Father')
ax.set_ylabel('Height Mother')
ax.set_zlabel('Height Kids')

#
#
#
ax.plot_wireframe(xx, yy, zz, rstride=10, cstride=10, alpha=0.3)
plt.show()
##residuals
residuals= y-skl_linmod.predict(X)
norm_au_carre= np.linalg.norm(residuals)**2
print norm_au_carre

# Histogram residuals

fig = plt.figure(figsize=(8, 6))
plt.hist(residuals, bins=50, normed=True, align='mid')
sns.kdeplot(residuals) # --> estimateur à noyau
plt.title('Residual Histogram/ KDE')
ax = plt.gca()
ax.legend_ = None
plt.xlabel('Residual value'), plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

#question 11
cov_Y_Father= np.cov(y,X['Father'])
print cov_Y_Father
cov_Y_Mother = np.cov(y,X['Mother'])
print cov_Y_Mother

#normailsatoin
X_scale= preprocessing.scale(X)
y_scale= preprocessing.scale(y)

#print X_scale[:,1]
cov_Y_Father= np.cov(y_scale,X_scale[:,0])
print cov_Y_Father
cov_Y_Mother = np.cov(y_scale,X_scale[:,1])
print cov_Y_Mother
