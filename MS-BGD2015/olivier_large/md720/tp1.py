# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from mpl_toolkits.mplot3d import Axes3D

color_blind_list = sns.color_palette("colorblind", 8)
my_orange = color_blind_list[2]
my_green = color_blind_list[1]

data = pd.read_csv('http://www.math.uah.edu/stat/data/Galton.txt ',delimiter='\t')
data["MeanParents"] = 0.5 * (data["Father"] + 1.08*data["Mother"])
print(data["MeanParents"])
#
#data.append("MeanParents")
#print(data["MeanParents"])
y = data['Height']
X = data[['MeanParents']]
xlabels = 'MeanParents'
ylabels = 'Height'

fig1 = plt.figure(figsize=(8, 6))
plt.xlabel(xlabels)
plt.ylabel(ylabels)
plt.title('Raw data')
plt.plot(X, y, 'o', label="Data", markeredgecolor='k', markeredgewidth=1)
axes = plt.gca()

plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display
plt.tight_layout()
#plt.show()

###################################################

skl_linmod = linear_model.LinearRegression()
skl_linmod.fit(X, y)



fig = plt.figure(figsize=(8, 6))
plt.plot(X, y, 'o', label="Data", markeredgecolor='k', markeredgewidth=1)
X_to_predict = np.linspace(62.0, 76.0, num=50).reshape(50, 1)
X_to_predict = pd.DataFrame(X_to_predict, columns=['MeanParents'])

plt.plot(X_to_predict, skl_linmod.predict(X_to_predict),
         linewidth=3, label="OLS-sklearn-no-inter")
plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display
plt.xlabel(xlabels), plt.ylabel(ylabels)
plt.title('Raw data and fitted')
plt.tight_layout()
#plt.show()

print "teta1 : %.2f" % skl_linmod.intercept_
print "teta0 : %.2f" % skl_linmod.coef_ 
teta1 = skl_linmod.coef_ 
teta0 = skl_linmod.intercept_
#################################################
#Histograme des résidus

fig = plt.figure(figsize=(8, 6))
plt.xlim(xmin=62, xmax=77)
plt.ylim(ymin=-13, ymax=13)

plt.xlabel(xlabels), plt.ylabel(ylabels)
legend_names = ['positive', 'negative']

plots = []
proxies = []

resdidual = y - skl_linmod.predict(X)

positive_res = resdidual > 0
negative_res = resdidual <= 0

markerline, stemlines, baseline = plt.stem(X[positive_res],
                                           resdidual[positive_res])
plt.setp(baseline, 'color', 'r', 'linewidth', 0)
plots.append((markerline, stemlines, baseline))
plt.setp(stemlines, linewidth=2, color=my_green)   # set stems colors
plt.setp(markerline, 'markerfacecolor', my_green, markeredgecolor='k',
         markeredgewidth=1)    # make points green
h, = plt.plot(1, 1, color=my_green)
proxies.append(h)
plt.legend(proxies, legend_names, numpoints=1, loc=2)


markerline, stemlines, baseline = plt.stem(X[negative_res],
                                           resdidual[negative_res])
plots.append((markerline, stemlines, baseline))
plt.setp(stemlines, linewidth=2, color=my_orange)   # set stems colors
plt.setp(markerline, 'markerfacecolor', my_orange, markeredgecolor='k',
         markeredgewidth=1)    # make points orange

plt.setp(baseline, 'color', 'r', 'linewidth', 0)

h, = plt.plot(1, 1, color=my_orange)
proxies.append(h)
plt.legend(proxies, legend_names, numpoints=1, loc=2)
plt.title('Residuals')
plt.axhline(y=0, ls='-', color='k')
plt.tight_layout()
#plt.show()

fig = plt.figure(figsize=(8, 6))
plt.hist(resdidual, bins=10, normed=True, align='mid')
sns.kdeplot(resdidual)
plt.title('Residual Histogram/ KDE')
ax = plt.gca()
ax.legend_ = None
plt.xlabel('Residual value'), plt.ylabel('Frequency')
plt.tight_layout()
#plt.show()

################################################
###################################################
X = data[['Height']]
y = data['MeanParents']
ylabels = 'MeanParents'
xlabels = 'Height'

skl_linmod = linear_model.LinearRegression()
skl_linmod.fit(X, y)



fig = plt.figure(figsize=(8, 6))
plt.plot(X, y, 'o', label="Data", markeredgecolor='k', markeredgewidth=1)
X_to_predict = np.linspace(62.0, 76.0, num=50).reshape(50, 1)
X_to_predict = pd.DataFrame(X_to_predict, columns=['Height'])

plt.plot(X_to_predict, skl_linmod.predict(X_to_predict),
         linewidth=3, label="OLS-sklearn-no-inter")
plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display
plt.xlabel(xlabels), plt.ylabel(ylabels)
plt.title('Raw data and fitted')
plt.tight_layout()
#plt.show()
print "alpha0 obs : %.2f" % skl_linmod.intercept_
print "alpha1 obs : %.2f" % skl_linmod.coef_ 


#################################################
#Histograme des résidus
#Histograme des résidus

fig = plt.figure(figsize=(8, 6))
plt.xlim(xmin=62, xmax=77)
plt.ylim(ymin=-13, ymax=13)

plt.xlabel(xlabels), plt.ylabel(ylabels)
legend_names = ['positive', 'negative']

plots = []
proxies = []

resdidual = y - skl_linmod.predict(X)

positive_res = resdidual > 0
negative_res = resdidual <= 0

markerline, stemlines, baseline = plt.stem(X[positive_res],
                                           resdidual[positive_res])
plt.setp(baseline, 'color', 'r', 'linewidth', 0)
plots.append((markerline, stemlines, baseline))
plt.setp(stemlines, linewidth=2, color=my_green)   # set stems colors
plt.setp(markerline, 'markerfacecolor', my_green, markeredgecolor='k',
         markeredgewidth=1)    # make points green
h, = plt.plot(1, 1, color=my_green)
proxies.append(h)
plt.legend(proxies, legend_names, numpoints=1, loc=2)


markerline, stemlines, baseline = plt.stem(X[negative_res],
                                           resdidual[negative_res])
plots.append((markerline, stemlines, baseline))
plt.setp(stemlines, linewidth=2, color=my_orange)   # set stems colors
plt.setp(markerline, 'markerfacecolor', my_orange, markeredgecolor='k',
         markeredgewidth=1)    # make points orange

plt.setp(baseline, 'color', 'r', 'linewidth', 0)

h, = plt.plot(1, 1, color=my_orange)
proxies.append(h)
plt.legend(proxies, legend_names, numpoints=1, loc=2)
plt.title('Residuals')
plt.axhline(y=0, ls='-', color='k')
plt.tight_layout()
#plt.show()

fig = plt.figure(figsize=(8, 6))
plt.hist(resdidual, bins=10, normed=True, align='mid')
sns.kdeplot(resdidual)
plt.title('Residual Histogram/ KDE')
ax = plt.gca()
ax.legend_ = None
plt.xlabel('Residual value'), plt.ylabel('Frequency')
plt.tight_layout()
#plt.show()

#################################
##Vérification
print "calcul alpha"
moyX = pd.DataFrame.mean(data[['MeanParents']])
moyY = pd.DataFrame.mean(data[['Height']])
varX = pd.DataFrame.var(data[['MeanParents']])
varY = pd.DataFrame.var(data[['Height']])
alpha0 = moyX['MeanParents'] + (moyY['Height']/moyX['MeanParents'])*(varX['MeanParents']/varY['Height'])*(teta0 - moyY['Height'])
alpha1 = (varX['MeanParents']/varY['Height'])*teta1
print "alpha0 : %.2f" % alpha0 
print "alpha1 : %.2f" % alpha1


#######################################
# Regression linéaire multiple
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