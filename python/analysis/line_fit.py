import numpy as np
import scipy as sp

def var(xs, errs=None):
    if errs is None:
        wgt=None
    else:
        wgt = np.power(errs, -2)

    meanX2 = np.average(np.power(xs, 2), weights=wgt)
    meanX = np.average(xs, weights=wgt)
    return meanX2 - np.power(meanX, 2)


def covar(xs, ys, errs=None):
    xys = [x*y for (x, y) in zip(xs, ys)]
    
    if errs is None:
        wgt=None
    else:
        wgt = np.power(errs, -2)

    xymean = np.average(xys, weights=wgt)
    xmean = np.average(xs, weights=wgt)
    ymean = np.average(ys, weights=wgt)

    return xymean - xmean*ymean


def fit(xs, ys, errs=None):
    N = len(xs) # number of datapoints
    
    if errs is None:
        wgt=None
    else:
        wgt = np.power(errs, -2)

    m = covar(xs, ys, errs) / var(xs, errs)

    xmean = np.average(xs, weights=wgt)
    ymean = np.average(ys, weights=wgt)
    c = ymean - m * xmean

    squares = [(y-(m*x+c))**2 for (x, y) in zip(xs, ys)]
    sigsq = np.average(squares, weights=wgt)/(N-2)

    sigm = np.sqrt(sigsq / N / var(xs, errs))
    meanX2 = np.average(np.power(xs, 2), weights=wgt)
    sigc = sigm * np.sqrt(meanX2)

    return ((m, c), (sigm, sigc))
