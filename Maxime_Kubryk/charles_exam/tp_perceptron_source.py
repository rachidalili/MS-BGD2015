# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 17:50:04 2013

@author: salmon
"""

############################################################################
########                Impoort part                                ########
############################################################################
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


############################################################################
########                Data Generation                             ########
############################################################################
def rand_gauss(n=100, mu=[1, 1], sigma=[0.1, 0.1]):
    """ Sample n points from a Gaussian variable with center mu,
    and std deviation sigma
    """
    d = len(mu)
    res = np.random.randn(n, d)
    return np.array(res * sigma + mu)


def rand_bi_gauss(n1=100, n2=100, mu1=[1, 1], mu2=[-1, -1], sigma1=[0.1, 0.1],
                  sigma2=[0.1, 0.1]):
    """ Sample n1 and n2 points from two Gaussian variables centered in mu1,
    mu2, with std deviation sigma1, sigma2
    """
    ex1 = rand_gauss(n1, mu1, sigma1)
    ex2 = rand_gauss(n2, mu2, sigma2)
    res = np.vstack([np.hstack([ex1, np.ones((n1, 1))]),
                     np.hstack([ex2, -1 * np.ones((n2, 1))])])
    ind = np.arange(res.shape[0])
    np.random.shuffle(ind)
    return np.array(res[ind, :])


def rand_clown(n1=100, n2=100, sigma1=1, sigma2=2):
    """ Sample a dataset clown  with
    n1 points and noise std deviation sigma1 for the first class, and
    n2 points and noise std deviation sigma2 for the second one
    """
    x0 = np.random.randn(n1)
    x1 = x0 * x0 + sigma1 * np.random.randn(n1)
    x2 = np.vstack([sigma2 * np.random.randn(n2),
                    sigma2 * np.random.randn(n2) + 2.])
    res = np.hstack([np.vstack([[x0, x1], np.ones([1, n1])]),
                     np.vstack([x2, -1 * np.ones([1, n2])])]).T
    ind = np.arange(res.shape[0])
    np.random.shuffle(ind)
    return np.array(res[ind, :])


def rand_checkers(n1=100, n2=100, sigma=0.1):
    """ Sample n1 and n2 points from a noisy checker"""
    nbp = int(np.floor(n1 / 8))
    nbn = int(np.floor(n2 / 8))
    xapp = np.reshape(np.random.rand((nbp + nbn) * 16), [(nbp + nbn) * 8, 2])
    yapp = np.ones((nbp + nbn) * 8)
    idx = 0
    for i in xrange(-2, 2):
        for j in xrange(-2, 2):
            if (((i + j) % 2) == 0):
                nb = nbp
            else:
                nb = nbn
                yapp[idx:(idx + nb)] = [-1] * nb

            xapp[idx:(idx + nb), 0] = np.random.rand(nb)
            xapp[idx:(idx + nb), 0] += i + sigma * np.random.randn(nb)
            xapp[idx:(idx + nb), 1] = np.random.rand(nb)
            xapp[idx:(idx + nb), 1] += j + sigma * np.random.randn(nb)
            idx += nb

    ind = np.arange((nbp + nbn) * 8)
    np.random.shuffle(ind)
    res = np.hstack([xapp, yapp[:, np.newaxis]])
    return np.array(res[ind, :])


############################################################################
########            Displaying labeled data                         ########
############################################################################
symlist = ['o', 's', '+', 'x', 'D', '*', 'p', 'v', '-', '^']
collist = ['blue', 'red', 'purple', 'orange', 'salmon', 'black', 'grey',
           'fuchsia']


def plot_2d(data, y=None, w=None, alpha_choice=1):
    """ Plot in 2D the dataset data, colors and symbols according to the
    class given by the vector y (if given); the separating hyperplan w can
    also be displayed if asked"""
    if y != None:
        labs = np.unique(y)
        idxbyclass = [np.where(y == labs[i])[0] for i in xrange(len(labs))]
    else:
        labs = [""]
        idxbyclass = [range(data.shape[0])]
    for i in xrange(len(labs)):
        plt.plot(data[idxbyclass[i], 0], data[idxbyclass[i], 1], '+',
                 color=collist[i % len(collist)], ls='None',
                 marker=symlist[i % len(symlist)])
    plt.ylim([np.min(data[:, 1]), np.max(data[:, 1])])
    plt.xlim([np.min(data[:, 0]), np.max(data[:, 0])])
    mx = np.min(data[:, 0])
    maxx = np.max(data[:, 0])
    if w != None:
        plt.plot([mx, maxx], [mx * -w[1] / w[2] - w[0] / w[2],
                              maxx * -w[1] / w[2] - w[0] / w[2]],
                 "g", alpha=alpha_choice)


############################################################################
########            Displaying tools for the Frontiere              ########
############################################################################


def frontiere(f, data, step=50):
    """ trace la frontiere pour la fonction de decision f"""
    xmin, xmax = data[:, 0].min() - 1., data[:, 0].max() + 1.
    ymin, ymax = data[:, 1].min() - 1., data[:, 1].max() + 1.
    xx, yy = np.meshgrid(np.arange(xmin, xmax, (xmax - xmin) * 1. / step),
                         np.arange(ymin, ymax, (ymax - ymin) * 1. / step))
    z = np.array([f(vec) for vec in np.c_[xx.ravel(), yy.ravel()]])
    z = z.reshape(xx.shape)
    plt.imshow(z, origin='lower', interpolation="nearest",extent=[xmin, xmax, ymin, ymax], cmap=cm.jet)
    plt.colorbar()



def frontiere_3d(f, data, step=20):
    """plot the 3d frontiere for the decision function ff"""
    ax = plt.gca(projection='3d')
    xmin, xmax = data[:, 0].min() - 1., data[:, 0].max() + 1.
    ymin, ymax = data[:, 1].min() - 1., data[:, 1].max() + 1.
    xx, yy = np.meshgrid(np.arange(xmin, xmax, (xmax - xmin) * 1. / step),
                         np.arange(ymin, ymax, (ymax - ymin) * 1. / step))
    z = np.array([f(vec) for vec in np.c_[xx.ravel(), yy.ravel()]])
    z = z.reshape(xx.shape)
    ax.plot_surface(xx, yy, z, rstride=1, cstride=1,
                    linewidth=0., antialiased=False, cmap=cm.jet)


def plot_cout(x, y, lfun, w=None):
    """ Plot the cost function encoded by lfun,
    for data x, and lable y, as a function of the weight parameter.
    W can be used to give a historic path of the weights """
    def _inter(wn):
        ww = np.zeros(3)
        ww[1:] = wn
        return lfun(x, y, ww).mean()
    if w == None:
        datarange = np.array([[-1, -1], [1, 1]], dtype=np.float) * 5.
    else:
        datarange = np.array([[w.min(), w.min()], [w.max(), w.max()]])
    frontiere(_inter, np.array(datarange))
    if w != None:
        plt.plot(w[:, 1], w[:, 2])


def plot_cout3d(x, y, lfun, w=None):
    """ trace le cout de la fonction cout lfun passee en parametre, en x,y,
                                en faisant varier les coordonnees du poids w.W peut
                                etre utilise pour passer un historique de poids"""
    def _inter(wn):
        ww = np.zeros(3)
        ww[1:] = wn
        return lfun(x, y, ww).mean()
    if w == None:
        datarange = np.array([[-1, -1], [1, 1]], dtype=np.float) * 5.
    else:
        datarange = np.array([[w[:, 1].min(), w[:, 2].min()],
                              [w[:, 1].max(), w[:, 2].max()]])
    frontiere_3d(_inter, np.array(datarange))
    plt.plot(w[:, 1], w[:, 2], np.array([_inter(w[i, 1:]) for i in
                                    xrange(w.shape[0])]), 'k-', linewidth=3)

############################################################################
########                Algorithms and functions                    ########
############################################################################


def gradient(x, y, epsilon, niter, w_ini, lfun, gr_lfun, stoch=True):
    """ algorithme de descente du gradient:
        - x : donnees
        - y : label
        - epsilon : facteur multiplicatif de descente
        - niter : nombre d'iterations
        - w_ini
        - lfun : fonction de cout
        - gr_lfun : gradient de la fonction de cout
        - stoch : True : gradient stochastique
        """
    #
    w = np.zeros((niter, w_ini.size))
    w[0] = w_ini
    loss = np.zeros(niter)
    loss[0] = lfun(x, y, w[0]).mean()
    for i in range(1, niter):
        if stoch:
            idx = [np.random.randint(x.shape[0])]
        else:
            idx = np.arange(x.shape[0])
        w[i, :] = w[i - 1, :] - epsilon * gr_lfun(x[idx, :], y[idx], w[i - 1, :])
        loss[i] = lfun(x, y, w[i, :]).mean()
    return w, loss


def plot_gradient(x, y, wh, costh, lfun):
    """ affiche 4 graphiques sur le fonctionnement de la descente de gradient.
    wh : historique des solutions
    costh : historique des couts
    lfun : fonction de couts
    """
    best = np.argmin(costh)
    #plt.figure(figsize=(15,15))
    plt.subplot(221)
    plt.title('Data and hyperplane estimated')
    plot_2d(x, y, wh[best, :])
    plt.subplot(222)
    plt.title('Projection of level line and algorithm path')
    plot_cout(x, y, lfun, wh)
    plt.plot(wh[:, 1], wh[:, 2], 'k-', linewidth=3)
    plt.subplot(223)
    plt.title('Objective function vs iterations')
    plt.plot(range(costh.shape[0]), costh)
    plt.subplot(224, projection='3d')
    plt.title('Level line and algorithm path')
    plot_cout3d(x, y, lfun, wh)


def predict(x, w):
    """ fonction de prediction a partir d'un vecteur directeur"""
    return np.dot(x, w[1:]) + w[0]


def predict_class(x, w):
    """ fonction de prediction de classe a partir d'un vecteur directeur"""
    return np.sign(predict(x, w))


############################################################################
########               Loss functions and their gradient            ########
############################################################################
def zero_one_loss(x, y, w):
    """ fonction de cout 0-1"""
    return abs(y - np.sign(predict(x, w))) / 2.


def hinge_loss(x, y, w):
    """ fonction de cout hinge loss"""
    return np.maximum(0., 1. - y * predict(x, w))


def mse_loss(x, y, w):
    """ fonction de cout moindres carres"""
    return (y - predict(x, w)) ** 2


def norm2(x, y, w):
    """norme carre d'un vecteur"""
    return np.dot(w, w)


def gr_hinge_loss(x, y, w):
    """ (sous-)gradient de la fonction de cout hingeloss"""
    return np.dot(-y * (hinge_loss(x, y, w) > 0.),
                  np.hstack((np.ones((x.shape[0], 1)), x)))


def gr_mse_loss(x, y, w):
    """ gradient de la fonction de cout moindres carres"""
    return -2. * np.dot(y - predict(x, w), np.hstack((np.ones((x.shape[0], 1)), x)))


def gr_norm2(x, y, w):
    """ gradient de la norme carre"""
    return 2. * w


def pen_loss_aux(x, y, w, l):
    """ fonction de cout penalisee"""
    return hinge_loss(x, y, w) + l * norm2(x, y, w)


def gr_pen_loss_aux(x, y, w, l):
    """ gradient fonction de cout penalisee"""
    return gr_hinge_loss(x, y, w) + l * gr_norm2(x, y, w, )


def pen_loss(l):
    return lambda x, y, w: pen_loss_aux(x, y, w, l)


def gr_penLoss(l):
    return lambda x, y, w: gr_pen_loss_aux(x, y, w, l)


############################################################################
########                Polynomial transformations                  ########
############################################################################
def poly2(x):
    if len(x.shape) == 1:
        x = x.reshape(1, x.shape[0])
    nb, d = x.shape
    res = x
    for i in range(0, d):
        for j in range(i, d):
            res = np.hstack((res, x[:, i:i + 1] * x[:, j:j + 1]))
    return res


def poly3(x):
    if len(x.shape) == 1:
        x = x.reshape(1, x.shape[0])
    nb, d = x.shape
    res = poly2(x)
    for i in range(0, d):
        for j in range(i, d):
            for k in range(j, d):
                res = np.hstack(
                    (res, x[:, i:i + 1] * x[:, j:j + 1] * x[:, k:k + 1]))
    return res
