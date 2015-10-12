# -*- coding: utf-8 -*-
"""
Created on Fri Oct 02 14:32:13 2015

@author: kim
"""
import pylab as P
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import seaborn as sns
import statsmodels.api as sm
import matplotlib.animation as animation
import time


###################################################################################
# Plot initialization
dirname="../srcimages/"
imageformat='.svg'
from matplotlib import rc
rc('font', **{'family':'sans-serif', 'sans-serif':['Computer Modern Roman']})
params = {'axes.labelsize': 12,
          'text.fontsize': 12,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True,
          'figure.figsize': (10,8)}
plt.rcParams.update(params)


###################################################################################
## 3D case drawing
plt.close("all")

#plt.interactive(True)
plt.ion()

# Load data
url = 'http://vincentarelbundock.github.io/Rdatasets/csv/datasets/trees.csv'
dat3 = pd.read_csv(url)

# Fit regression model
X=dat3[['Girth','Height']]
X = sm.add_constant(X)
y=dat3['Volume']
#results = sm.OLS(y,X).fit().params


XX = np.arange(8, 22, 0.5)
YY = np.arange(64, 90, 0.5)
xx, yy = np.meshgrid(XX, YY)
#zz = results[1]*xx +results[2]*yy+results[0]


fig = plt.figure()
sns.set_context("poster")
sns.set_palette("colorblind")
#ax = fig.add_subplot(111, projection='3d')
ax=Axes3D(fig)
#ax.surface(xx, yy, zz, rstride=10, cstride=10)

ax.plot(X['Girth'],X['Height'],y,'o')
ax.set_zlim(5, 80)
ax.set_xlabel('Girth')
ax.set_ylabel('Height')
ax.set_zlabel('Volume')


#P.figure(fig.number)

################################################################################
######################## Model calculation and display #########################
# A plane equation is T1*xx+T2*yy+T3*z+T0=0, T(T0,T1,T2,T3)est le vecteur normal au plan recherché
#can also be writen as  z = -T0/T3 -T2/T3yy -T1/T3xx
#In our model Teta = (Teta0, Teta1, Teta2) where Teta0 = -T0/T3 , Teta1 =-T1/T3, Teta2 = -T2/T3  

#Calcualtion of Teta with gradient descent method
#Set alpha which is the step of the descent
X = X.as_matrix()
X = X[1:,:]
Xt = X.T #transposée de X
y = y.as_matrix()
y =y[1:]
Teta = np.asarray([0,0,0]) #initialisation de Teta
alpha = 0.0001
Iterations = 8
m = len(y)
residus = np.dot(X,np.transpose(Teta)) - y
z = Teta[0] + Teta[1]*xx + Teta[2]*yy
plt3d = fig.gca(projection='3d')


def data_gen(z,Teta,p):
    for i in range(1, p*400):  
        grad = np.dot((np.dot(X,np.transpose(Teta)) - y),X)
        Teta =  Teta-(alpha/m)*grad       
    z = Teta[0] + Teta[1]*xx + Teta[2]*yy    
    #plt3d.clear()
    ax.plot(X[:,1],X[:,2],y,'o')
    plot = plt3d.plot_surface(xx, yy, z,rstride=1, cstride=1, cmap=cm.winter,alpha=0.5,linewidth=.1)     
    #plt.figure(fig.number)
    return plot,Teta

for p in range(1,Iterations):       
    plot , Teta = data_gen(z,Teta,p)
    time.sleep(1)
    plt.draw()    
    residus = np.dot(X,np.transpose(Teta)) - y
    print("Coordonnees du vecteur de parametres Teta" ,Teta , "  Somme normee des residus:", np.sqrt(np.sum(residus**2)))

#pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(z,plot,Teta), frames=50, interval=30, blit=True)
#pam_ani.save('test.mp4')
residus = np.dot(X,np.transpose(Teta)) - y
plt.ioff()

# plot the surface
#P.show()