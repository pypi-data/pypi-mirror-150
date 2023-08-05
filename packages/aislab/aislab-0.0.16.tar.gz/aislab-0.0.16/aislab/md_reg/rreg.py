"""
author: OPEN-MAT
date: 	14.12.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems"""
import numpy as np
from aislab.gnrl.sf import *
from aislab.md_reg.linest import *

# rlspm
# rlspv
# relspv
# relspm
# rmlpm
# rmlpv
# rpepm
# rpepv
#######################################################################################
# function [pm, fi, P, par] = rls(yk, uk, pm, fi, P, par)
def rls(U, Y, pm, P,
        par={},
        na=None,
        nb=None,
        pm0=None,
        mod=None,
        se=None,
        rvmin=None,
        rv=None,
        a=None,
        rc=None,
        trPmin=None,
        s=None
        ):

    if type(U) != np.ndarray:       U = np.array([U])
    if type(Y) != np.ndarray:       Y = np.array([Y])
    m = U.shape[1]
    r = Y.shape[1]
    if (np.array([na == None])).any():
        if 'na' in par:     na = par['na']
        else:               na = np.zeros((r, r))
    if (np.array([nb == None])).any():
        if 'nb' in par:     nb = par['nb']
        else:               nb = np.zeros((r, m))
    if (np.array([pm0 == None])).any():
        if 'pm0' in par:    pm0 = par['pm0']
        else:               pm0 = np.zeros((r, 1))
    if mod == None and 'mod' in par:       mod = par['mod']
    else:                                  mod = 'non'
    if (np.array([se == None])).any() and 'se' in par:          se = par['se']
    if (np.array([rvmin == None])).any() and 'rvmin' in par:    rvmin = par['rvmin']
    if (np.array([rv == None])).any():
        if 'rv' in par:                    rv = par['rv']
        else:                              rv = np.ones([r])
    
    if a == None and 'a' in par:           a = par['a']
    if rc == None and 'rc' in par:         rc = par['rc']
    if trPmin == None and 'rePmin' in par: trPmin = par['trPmin']
    if s == None and 's' in par:           s = par['s']
    if type(pm) != np.ndarray:      pm = np.array([pm])
    if type(P) != np.ndarray:       P = np.array([P])
    if type(na) != np.ndarray:      na = np.array([na])
    if type(nb) != np.ndarray:      nb = np.array([nb])
    if type(pm0) != np.ndarray:     pm0 = np.array([pm0])
    if type(se) != np.ndarray:      se = np.array([se])
    if type(rvmin) != np.ndarray:   rvmin = np.array([rvmin])
    if type(rv) != np.ndarray:      rv = np.array([rv])

    yk = c_(Y[-1, :])
    fi = dmpv(U, Y, na=na, nb=nb, pm0=pm0).T
    pm = c_(pm)
    nn = np.sum(np.hstack((na, nb, pm0)), axis=1).astype(int)

    # residual update
    e = yk - fi.T@pm
    # Kalman gain (K) & Covariance matrix (P) update
    if mod == 'non':
        M = np.eye(r) + fi.T@P@fi
        rcM = 1/np.linalg.cond(M)  # todo: calc condition number in a function in sf
        if rcM < 1e-6: K = P@fi@nsinv(M)
        else:          K = P@fi@np.linalg.inv(M)
        P = P - K@fi.T@P
    elif mod == 'ctr':
        trP = par['trP']
        M = np.eye(r) + fi.T@P@fi
        rcM = 1/np.linalg.cond(M)  # todo: calc condition number in a function in sf
        if rcM < 1e-6: K = P@fi@nsinv(M)
        else:          K = P@fi@np.linalg.inv(M)
        trPk = np.trace(P - K@fi.T@P)/trP;
        P = (P - K@fi.T@P)/trPk
    elif mod == 'ccm':
        P = par['P']
        M = np.eye(r) + fi.T@P@fi
        rcM = 1/np.linalg.cond(M)  # todo: calc condition number in a function in sf
        if rcM < 1e-6: K = P@fi@nsinv(M)
        else:          K = P@fi@np.linalg.inv(M)
    elif mod == 'pdm':
            trPmin = par['trPmin']
            s = par['s']
            M = np.eye(r) + fi.T@P@fi;
            rcM = 1/np.linalg.cond(M)  # todo: calc condition number in a function in sf
            if rcM < 1e-6: K = P@fi@nsinv(M)
            else:          K = P@fi@np.linalg.inv(M)
            P = P - K@fi.T@P
            if np.trace(P) < trPmin: P = P + s*np.eye(len(pm))
    elif mod == 'cff':
#        K = P*fi@np.linalg.inv(rc*np.eye(r) + fi.T@P@fi)
#        P = rc ^ -1@(P - K@fi.T@P)
        
        c = np.sqrt(rc)
        C = np.zeros((int(np.sum(nn))))
        for i in range(r):
            n = sum(nn[:i - 1])
            ind = np.arange(n, n + nn[i])
            C[ind] = c[i]
        C1 = np.diag(C**-1)
        M = np.eye(r) + fi.T@C1@P@C1@fi
        rcM = 1/np.linalg.cond(M)  # todo: calc condition number in a function in sf
        if rcM < 1e-6: K = P@C1@fi@nsinv(M)
        else:          K = P@C1@fi@np.linalg.inv(M)
        P = C1@(P - K@fi.T@C1@P)@C1 # (A + B*C*D)^?1 = A^?1 ? A^?1*B(C^?1 + D*A^?1*B)^?1*D*A^?1
    elif mod == 'vff':
        # se = (se*np.max([1, k - nn - 2])*1 + e**2)/np.max([1, k - nn - 1])
        nn = np.sum(np.hstack((na, nb, pm0)), axis=1).astype(int)
        c = np.sqrt(rv)
        C = np.zeros((int(np.sum(nn))))
        for i in range(r):
            n = sum(nn[:i - 1])
            ind = np.arange(n, n + nn[i])
            C[ind] = c[i]
        C1 = np.diag(C**-1)
        
        M = np.eye(r) + fi.T@C1@P@C1@fi
        rcM = 1/np.linalg.cond(M)  # todo: calc condition number in a function in sf
        if rcM < 1e-6: K = P@C1@fi@nsinv(M)
        else:          K = P@C1@fi@np.linalg.inv(M)
        P = C1@(P - K@fi.T@C1@P)@C1

        # rv = np.max(np.hstack((1 - (1 - fi.T@K)@(e**2)/(se*Ne), rvmin.reshape(-1, 1))), axis=1)
        rv = np.max(np.hstack((1 - (1 - fi.T@K)@e**2/se, rvmin.reshape(-1, 1))), axis=1)
        par['rv'] = rv
        par['se'] = se

    # model parameters (pm) update
    pm = pm + K@e
    return pm, P, par

    # TODO: if time for the model update is critical, then rls() can be split into rlsp() - predictor and rlsc() - corrector
    # E.g. for RLS:
    #    pm = rlsp(...)
    #       e = yk - fi*pm;
    #       K = P*fi'/(1 + fi*P*fi');
    #       pm = pm + K*e;
    #    [P, fi] = rlsc(...)
    #       P = P - K*fi*P;
    #       fi = [-yk fi(1:na - 1) uk fi(na + 1:end - 1)];
