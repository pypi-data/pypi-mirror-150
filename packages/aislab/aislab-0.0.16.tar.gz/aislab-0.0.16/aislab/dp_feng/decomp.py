"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
"""
import numpy as np
from aislab.gnrl.sf import *
####################################################################################
# def trnd():
####################################################################################
def prd(x, w=None, T=7, n=None, x0=0, met='blk', ltv=False):
    
    if w is None: w = ones(x.shape)
    N = len(x)
    T = int(T)
    n = int(n)
    l = int(np.floor(N/T))
    h = np.ceil(N/T).astype(int)*T - N
    S = x[:l*T].reshape(l, T)
    W = w[:l*T].reshape(l, T)
    if N > l*T:
        ss = nans((1, h))
        S = np.vstack((S, np.hstack((x[l*T:].T, ss))))
        W = np.vstack((W, np.hstack((w[l*T:].T, ss))))

    if met == 'blk':
        Nw = np.nancumsum(W, axis=0).astype(float)
        Nw[n:, :] = Nw[n:, :] - Nw[:-n, :]
        Nw[Nw == 0] = 1e-6
        pm = np.nancumsum(S*W, axis=0)
        pm[n:, :] = pm[n:, :] - pm[:-n, :]
        pm = pm/Nw
        # pm[:np.min([N0, T])] # default: N0=9
        # ind = T if len(x) % T == 0 else len(x) % T
        ind = len(x) % T
        pm = c_(pm.flatten()[:-h])
    elif met == 'rec':
        Nw = np.nansum(W, axis=0).astype(float)
        Nw[Nw == 0] = 1e-6
        pm = np.nansum(S*W, axis=0)/Nw
        ind = T if len(x) % T == 0 else len(x) % T
        pm = np.roll(pm, -ind)
    return pm
####################################################################################
# 	T determination = f(Rxx), f(fft), ...
