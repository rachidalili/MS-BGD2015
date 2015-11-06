import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import seaborn as sns
from binning import *
from pandas.tools.plotting import radviz, scatter_matrix


#============================================================================================

def plot_pcolor(xbins, ybins, bins, **kwargs):
    """ pcolor plot z particules associated to values x and y, are put in xbins and ybins"""

    opt = {'power': 1.0,
           'vmin': None,
           'vmax': None,
           'bar_label': 'Number',
           'fsize': 20,
           'cmap': 'jet',
           'scale': 'lin',
           'bar_orient': 'vertical',
           'position': 'center',
           'invalid': nan
           }

    opt.update(kwargs)
    print(opt)

    if opt['invalid'] != np.nan:
        bins[bins == opt['invalid']] = np.nan

    bins = ma.masked_invalid(bins)
    cmap = plt.get_cmap(opt['cmap'])
    cmap.set_bad(color='w', alpha=1.)

    def func(x, y):
        return bins[x, y]

    I = range(len(xbins))
    J = range(len(ybins))
    X, Y = np.meshgrid(I, J)

    Z = func(X, Y)**(opt['power'])

    if opt['vmin'] == None:
        vmin = Z.min()
    else:
        vmin = opt['vmin']

    if opt['vmax'] == None:
        vmax = Z.max()
    else:
        vmax = opt['vmax']

    if opt['position'] == 'center':
        x_offset = 0.5 * (xbins[1] - xbins[0])
        y_offset = 0.5 * (ybins[1] - ybins[0])
    else:
        x_offset = 0.
        y_offset = 0.

    if opt['scale'] == 'log':

        PP = plt.pcolor(xbins[X] - x_offset, ybins[Y] - x_offset, Z,
                        norm=LogNorm(vmin=1.0, vmax=vmax), cmap=cmap)  # , vmin=0.0 ,v)

    else:

        # PP = pcolor(xbins[X] - x_offset , ybins[Y] - x_offset , Z, vmin=vmin,
        # vmax=vmax , cmap = cmap )#, vmin=0.0 ,v)
        PP = plt.pcolor(xbins[X], ybins[Y], Z, vmin=vmin, vmax=vmax, cmap=cmap)  # , vmin=0.0 ,v)

    cb = plt.colorbar(PP, orientation=opt['bar_orient'])
    cb.set_label(r'$\bf ' + opt['bar_label'] + ' $', fontsize=opt['fsize'])

    plt.xlim(xbins[0], xbins[-1])
    plt.ylim(ybins[0], ybins[-1])


def binning():
    spec_bins = sorted(df['num_spec'].unique() - 0.5)
    dep_bins = sorted(df['num_dep'].unique() - 0.5)

    print(spec_bins)
    print(dep_bins)

    bins = binning_2D(spec_bins, dat['num_spec'].values, 5, 2, dep_bins, dat[
                      'num_dep'].values, 5, 3, dat['DEPASSEMENTS (euros)'].values)

    for i in range(len(bins[0, :])):
        bins[:, i] = bins[:, i] / sum(bins[:, i])

    I = range(len(spec_bins))
    J = range(len(dep_bins))
    X, Y = np.meshgrid(I, J)

    def func(x, y):
        return bins[x, y]

    Z = func(X, Y)

    plt.figure()
    plt.matshow(bins)


def ploting():
    # ploting the results
    plt.style.use('ggplot')
    fig, axes = plt.subplots(ncols=2, nrows=3, figsize=(15, 15))
    axs = axes.ravel()

    i = 0
    for name, group in groups:
        x = group['num_dep'].values
        y = group['num_spec'].values
        axs[i].scatter(x, y, c='b', marker='o', lw=0, s=50, label=name)
        axs[i].set_xlabel('departement')
        axs[i].set_ylabel('code specialite')
        axs[i].legend(loc='best', frameon=True)
        i += 1


def format_data():
    path = "data/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2013.xls"

    data = pd.read_excel(path, sheetname=[1, 2, 3, 4, 5, 6])

    df = data[2]
    df = df.replace('nc', np.nan).dropna()
    df = df[df['DEPARTEMENT'].str.contains('- ')]
    df = df[df['SPECIALISTES'].str.contains('- ')]
    df = df[df['EFFECTIFS'] > 0]

    dep = pd.DataFrame([[x] + x.split('- ') for x in df['DEPARTEMENT']],
                       columns=['DEPARTEMENT', 'num_dep', 'name_dep'])

    spec = pd.DataFrame([[x] + x.split('- ') for x in df['SPECIALISTES']],
                        columns=['SPECIALISTES', 'num_spec', 'name_spec'])

    df = pd.concat([df, dep, spec], axis=1, join='inner')

    df['num_dep'] = df['num_dep'].str.replace('^0', '').str.replace(
        'B', '.5').str.replace('A', '.25').astype('float')

    df['num_spec'] = df['num_spec'].replace('^0', '').astype('float')
    df['DEPASSEMENTS (euros)'] = df['DEPASSEMENTS (euros)'].astype('float')

    print(df.head())

    df['NOMBRE DE DEPASSEMENTS (/medecin)'] = df['NOMBRE DE DEPASSEMENTS'] / df['EFFECTIFS']
    df['DEPASSEMENTS (euros/medecin)'] = df['DEPASSEMENTS (euros)'] / df['EFFECTIFS']
    #df['DEPASSEMENT MOYEN (euros/medecin)'] = df['DEPASSEMENT MOYEN (euros)'] / df['EFFECTIFS']

    #------------ histograme 'DEPASSEMENTS (euros)' -------------------------------
    plt.figure()
    plt.title('on considere les DEPASSEMENTS totaux > 5e6€ comme outliers (on le retire)')
    df['DEPASSEMENTS (euros)'].plot(kind='hist', stacked=True, bins=100)
    plt.xlim(0, 6e6)

    #df = df[df['DEPASSEMENTS (euros)'] <= 5.e6]

    #--------------scatter_matrix -------------------------------------------
    dat = df[['num_spec', 'NOMBRE DE DEPASSEMENTS',
              'DEPASSEMENT MOYEN (euros)', 'DEPASSEMENTS (euros)', 'EFFECTIFS']]
    scatter_matrix(dat, diagonal='kde')

    # ---------- corrélations entre les variables, par numero de spécialité --------------
    dat = df[['num_spec', 'NOMBRE DE DEPASSEMENTS',
              'DEPASSEMENT MOYEN (euros)', 'DEPASSEMENTS (euros)', 'EFFECTIFS']]
    corr_mat = dat.corr()

    plt.figure()
    sns.heatmap(corr_mat, square=True)

    plt.figure()
    plt.title('Sans prendre en compte le departement.\n Un EFFECTIF plus faible semble corrélé  à des\n' +
              ' NOMBRE DE DEPASSEMENTS et DEPASSEMENTS (totaux) plus elevés.\n' + 'Il semble également que' +
              " les EFFECTIFS soient mal repartis d'une specialite à l'autre.")
    radviz(dat, 'num_spec')

    print(df.head())

    return df

    # seaborn.set(font="monospace")
    # plt.figure()
    # seaborn.heatmap(dat)

    # plt.figure()
    # seaborn.clustermap(dat)
    #dep_groups = df.groupby('DEPARTEMENT')

    # for name, group in dep_groups:
    #    print(name)
    #    print(group.head())
