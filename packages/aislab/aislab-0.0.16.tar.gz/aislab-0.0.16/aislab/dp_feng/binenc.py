import numpy as np
import pandas as pd  # for enc_int() - transform all categorical variables to int variables
from numpy.matlib import repmat
# import sys
import copy

from aislab.gnrl.measr import * # vaf
from aislab.gnrl.bf import * # c_
from aislab.gnrl.sf import *
from aislab.gnrl.tm import *
from aislab.op_nlopt.ga import *

###################################################################################
def b2dv(bin, x, xtp):
    if xtp == 'nom' or xtp == 'ord':
        dv = np.zeros(x.shape, dtype=int)
        for k in range(len(bin['lb'])):
            if bin['type'] == 'Missing':
                dv1 = np.isnan(x)
            elif bin['type'] == 'Other':
                dv1 = np.zeros(x.size)
            elif bin['type'] == 'Special Value':
                dv1 = x == bin['lb']
            else:
                dv1 = x == bin['lb'][k]
            dv = dv + dv1
    else:
        if bin['type'] == 'Missing':
            dv = np.isnan(x)
        elif bin['type'] == 'Other':
            dv = np.full(x.shape, False)
        elif bin['type'] == 'Special Value':
            dv = x == bin['lb']
        elif bin['lb'] == bin['rb']:
            dv = x == bin['lb']
        else:
            dv = (x >= bin['lb']) & (x < bin['rb'])
    # dv = np.array(dv, dtype=bool)
    return dv


###################################################################################
def best_merge(bns, s, xtp):
    bns2 = copy.deepcopy(bns)
    if isinstance(s, (int, float)): s = m_(s)
    md = len(s)
    i1 = 1
    i2 = 1
    j = 0
    for si in s:
        i2 += si
        if i2 - i1 > 1:
            for i3 in range(i1, i2 - 1):
                bns2 = mrgbns(bns2, i1, xtp=xtp)
        j += 1
        i1 = i2
        i1 -= si - 1
        i2 -= si - 1
    return bns2


###################################################################################
def binMOS(bns, x, w, sv, xtp, y, ytp, yi):
    ii = np.isnan(x)
    if any(ii):
        if len(y) == 0:
            yy = nans((len(x), 1))
        else:
            yy = y[np.where(ii)[0], :]
        bns[len(bns) + 1] = setbin(np.nan, w[ii], xtp, 'Missing', yy, ytp, yi)
    else:
        bns[len(bns) + 1] = setbin(np.nan, [0], xtp, 'Missing', nans((1, len(ytp))), ytp, yi)
        bns[len(bns)]['n'] = 0
    bns[len(bns) + 1] = setbin([], [0], xtp, 'Other', nans((1, len(ytp))), ytp, yi)
    for j in range(len(sv)):
        ii = x == sv[j]
        if any(ii):
            if len(y) == 0:
                yy = nans((len(x), 1))
            else:
                yy = y[ii]
            bns[len(bns) + 1] = setbin(sv[j], w[ii], xtp, 'Special Value', yy, ytp, yi)
        else:
            bns[len(bns) + 1] = setbin(sv[j], [0], xtp, 'Special Value', nans((len(ytp),)), ytp, yi)
    return bns


###################################################################################
def stbnsy(bns, x, y, w, xtp, ytp):
    yi = setyi(y, ytp)
    for h in range(1, len(bns) + 1):
        dv = b2dv(bns[h], x, xtp)
        bns[h]['y'] = {}
        bns[h]['y2'] = {}
        bns[h]['nw'] = {}  # !
        bns[h]['my'] = {}
        bns[h]['woe'] = {}
        bns[h]['int'] = {}
        bns[h] = binst(bns[h], 'stats', y[dv[:, 0]==1, :], w[dv[:, 0]==1, 0], ytp, yi)
        bns[h]['int'] = h
    return bns

###################################################################################
def bns2arr(bns):
    # r = len(bns[1]['y'])
    m = len(bns)
    Luy = 0
    for i in bns[1]['y']:
        Luy = Luy + len(bns[1]['y'][i])
    syy = np.zeros([m, Luy])
    syy2 = np.zeros([m, Luy])
    wy = np.zeros([1, Luy])
    nw = nans((m, 1))
    for i in range(len(bns)): nw[i] = bns[i + 1]['nw']
    n = nans((m, 1))
    for i in range(len(bns)): n[i] = bns[i + 1]['n']
    for i in range(m):
        if len(bns[i + 1]['y']) > 0:
            y = []
            y2 = []
            for j in bns[i + 1]['y']:
                y = np.append(y, bns[i + 1]['y'][j])
                y2 = np.append(y2, bns[i + 1]['y2'][j])
        else:
            y = nans((Luy,))
            y2 = nans((Luy,))
        syy[i] = y
        syy2[i] = y2
    j = [-1]
    wy = []
    for i in bns[1]['y']:
        luy = len(bns[1]['y'][i])
        # j = np.arange(j[len(j)-1] + 1 ,j[len(j)-1]+1+luy)
        wy = np.append(wy, repmat(1/luy, 1, luy))
    return n, nw, syy, syy2, wy


###################################################################################
def binst(bins, mod, y, w, ytp, yi):
    if len(w) and np.any(w):
        bins['n'] = len(w)
        bins['nw'] = np.sum(w)
    else:
        bins['n'] = 0
        bins['nw'] = 0.
    if len(y):
        if y.ndim == 1 and len(ytp) == 1: y = c_(y)
        b = {}
        b2 = {}
        bins['y'] = {}
        bins['y2'] = {}

        for i in range(len(ytp)):
            yh = y[:, i]
            if ytp[i] == 'nom' or ytp[i] == 'ord':
                yii = yi[i]
                c = nans((len(yii),))
                for j in range(len(yii)):
                    jj = list(yh == yii[j])
                    if len(w) == 1 and w[0] == 0:
                        c[j] = 0
                    else:
                        if jj != []:
                            c[j] = np.sum(w[jj])
                        else:
                            c[j] = 0
                bins['y'][i + 1] = c
                bins['y2'][i + 1] = c
                if mod == 'stats':
                    bins['my'][i + 1] = []
                    bins['woe'][i + 1] = []
            else:
                if len(y):
                    b[i + 1] = [np.sum(w*yh)]
                    b2[i + 1] = [np.sum(w*yh**2)]
                else:
                    b[i + 1] = [0]
                    b2[i + 1] = [0]
                bins['y'] = b
                bins['y2'] = b2
                if mod == 'stats':
                    bins['my'][i + 1] = b[i + 1][0]/max(bins['nw'], 1e-12)
                    bins['woe'][i + 1] = []
    return bins


###################################################################################
def cut(x, cuts):
    # Transforms a numeric variable & cut-off values into a variable of int values corresponding to bin index.
    cuts = np.hstack([-np.inf, cuts, np.inf])
    bns = {}
    for i in range(len(cuts) - 1):
        bns[i + 1] = {'type': 'Normal', 'lb': cuts[i], 'rb': cuts[i + 1]}
    bng = {'xtp': 'num',
           'bns': bns,
         'cname': 'var_01'
        }
    xe, _ = enc_apl(bng, x, 'int')
    return xe


###################################################################################
def cnd_gbi(gg, ngg, dGBInd, tolmindGBInd, Dind):
    GBI = gbi(gg, ngg)
    GBI1 = GBI + 200*(GBI < 0)
    dGBI = d_(GBI1)
    # sdGBI = np.sort(dGBI)
    cnd_GBI = np.min(abs(dGBI), axis=0) >= dGBInd - tolmindGBInd*Dind
    return cnd_GBI


###################################################################################
def cnd_trnd(ns, gg, nn, md, mt):
    if mt is not np.nan:
        my = gg/nn
        my[my < 1e-3] = 1e-3
        dmy = d_(my)
        trnd = (np.sum(dmy > 0, axis=0) == md - 1)*1 - (np.sum(dmy < 0, axis=0) == md - 1)
        if mt == 0: cnd_TRND = abs(trnd) == 1
        else:       cnd_TRND = trnd == mt
    else:
        cnd_TRND = np.ones(ns, dtype=bool)
    return cnd_TRND


###################################################################################
# def enc():
#   encoding
#   - met = woe, mdep, ...
###################################################################################
def enc_int(x, cname, xtp, vtp, order, dsp=False, dlm=' '):
    N = x.shape[0]
    xnum = np.full((len(x), len(cname)), np.nan)
    for i in range(len(cname)):
        cnamei = cname[i]
        if dsp: print(i + 1, '/', len(cname), 'Variable: ', cnamei)
        # xi = x[:, i]
        xi = x[cnamei].values
        xtpi = xtp[i]
        if xtpi == 'ord' or xtpi == 'nom':
            vtpi = vtp[i]
            orderi = order[i]
            nulls, = np.where(xi.astype(str) == str(np.nan))
            if xi.dtype == 'int' and len(nulls[0]) > 0: xi = xi.astype(float)
            if xi.dtype == 'float':
                xi[nulls] = np.nan
            elif xi.dtype == 'str' or xi.dtype == 'O':
                xi[nulls] = 'NaN'
                xi = xi.astype(str)

            if xtpi == 'ord' and isinstance(orderi, str):
                orderi = np.array(orderi.split(dlm))  # vtpi - str
                if vtpi == 'int':      orderi = np.array(list(map(int, orderi)))
                if vtpi == 'float':    orderi = np.array(list(map(float, orderi)))
            else:  # np.isnan(orderi)
                orderi = np.unique(xi)
                # if len(nulls) > 0: orderi = np.append(orderi, 'nan')
            v = np.argsort(orderi)
            xi[nulls] = orderi[0]
            if not set(np.unique(xi.astype(str)).tolist()).issubset(set(orderi.astype(str))):
                if dsp: print('ERROR: Variable: ', cnamei,
                              ' - ordered values (in config file) and the unique values in data are not the same...')
                continue
            # xnum[:, i] = v2i1(xi, orderi)
            xnum[:, i] = v2i(xi, v)
            xnum[nulls, i] = np.nan
        elif xtpi == 'num':
            xnum[:, i] = xi

    xnum = pd.DataFrame(xnum, columns=cname)
    cat_var = ((xtp == 'nom') | (xtp == 'ord')).tolist()
    for i in range(0, len(cat_var)):
        if cat_var[i]: xnum[cname[i]] = pd.to_numeric(xnum[cname[i]].values, downcast='integer')
    return xnum


###################################################################################
def v2i1(x, order=None):  # slower version & not work well with nan-s
    if order is None: order = np.unique(x)
    i = 10
    xe = copy.deepcopy(x)
    for xi in order:
        xe[x.flatten() == xi] = i
        i += 1
    return xe.astype(int)


###################################################################################
def v2i(x, v):
    '''
    x - data vector (1d or 2d np.array)
    v - int values (indexes of sorted ordered values that replaces the unique values of x
    '''
    x = x.flatten().astype(str)
    ux = np.unique(x)
    isux = np.argsort(ux)
    ix = np.searchsorted(ux, x, sorter=isux)
    return v[isux][ix]


###################################################################################
def enc_apl(bng, x, met):
    if isinstance(bng, list):
        m = len(bng)
    else:
        m = 1
    N = x.shape[0]
    xenc = np.empty((N, 0))
    ss = []
    for i in range(m):
        if isinstance(x, pd.DataFrame):
            xi = c_(x.iloc[:, i].values)
        else:
            xi = x
        if m == 1:
            bns = bng['bns'];       cname = bng['cname'];       xtp = bng['xtp']
        else:
            bns = bng[i]['bns'];    cname = bng[i]['cname'];    xtp = bng[i]['xtp']

        if met == 'dv':
            mi = len(bns); cname_e = []; j = 0
        else:
            mi = 1
        cnd_st = [None]*mi
        xe = nans((N, mi))
        hh = 0
        for h in range(1, len(bns) + 1):
            if met == 'dv' and not bns[h]['n'] > 0: xe = np.delete(xe, h-1-hh, axis=1); hh += 1; continue
            dv = b2dv(bns[h], xi, xtp)==1
            if met == 'my':      xe[dv] = bns[h]['my'];  cname_e = cname + '_encMY'
            elif met == 'woe':   xe[dv] = bns[h]['woe'];  cname_e = cname + '_encWOE'
            elif met == 'int':   xe[dv] = h - 1;          cname_e = cname + '_encINT'
            elif met == 'dv':    xe[:, j] = dv.flatten()*1; cname_e = cname_e + [cname + '_encDV' + str(j + 1)]; j += 1
        if met == 'dv': xe = xe.astype(int)
        xenc = np.hstack((xenc, xe))
        if isinstance(cname_e, str): ss.append(cname_e)
        else:                        ss = ss + cname_e
    return xenc, ss

###################################################################################
def inv_distr(DistrType, pval, df1, df2, x1, x2, tol):
    ITMAX = 100;
    EPS = 3.0e-7
    a = x1
    b = x2
    c = x2
    d = 0
    e = 0
    cnd = DistrType == 'Fisher'
    if cnd:
        fa = betai(df1, df2, a)[0] - pval
        fb = betai(df1, df2, b)[0] - pval
    else:
        fa = gamq(df2, a)[0] - pval
        fb = gamq(df2, b)[0] - pval
    if fa > 0 and fb > 0 or fa < 0 and fb < 0:
        print('Root must be bracketed in inverse_distr')
        return None
    fc = fb
    it_num = range(0, ITMAX)
    for i in it_num:
        if fb > 0 and fc > 0 or fb < 0 and fc < 0:
            c = a
            fc = fa
            e = b - a
            d = e
        if abs(fc) < abs(fb):
            a = b
            b = c
            c = a
            fa = fb
            fb = fc
            fc = fa
        tol1 = 2*EPS*abs(b) + 0.5*tol
        xm = 0.5*(c - b)
        cnd1 = abs(b) < 1e-10
        if abs(xm) <= tol1 or fb == 0:
            return int(cnd)*(cnd1*1e10 + int(not cnd1)*(1/b - 1)*df1/df2) + int(not cnd)*2*b
        if abs(e) >= tol1 and abs(fa) > abs(fb):
            s = fb/fa
            if a == c:
                p = 2*xm*s
                q = 1 - s
            else:
                q = fa/fc
                r = fb/fc
                p = s*(2*xm*q*(q - r) - (b - a)*(r - 1))
                q = (q - 1)*(r - 1)*(s - 1)
            if p > 0:
                q = -q
            p = abs(p)
            min1 = 3*xm*q - abs(tol1*q)
            min2 = abs(e*q)
            cnd2 = min1 < min2
            if 2*p < (cnd2*min1 + int(not cnd2)*min2):
                e = d
                d = p/q
            else:
                d = xm
                e = d
        else:
            d = xm;
            e = d
        a = b
        fa = fb
        if abs(d) > tol1:
            b = b + d
        else:
            prod = xm*tol1
            if prod == 0:
                sgn = 1
            else:
                sgn = np.sign(prod)
            b = b + sgn*abs(tol1)
        if cnd:
            fb = betai(df1, df2, b)[0] - pval
        else:
            fb = gamq(df2, b)[0] - pval
    cnd1 = abs(b) < 1e-10
    return cnd*(cnd1*1e10 + int(not cnd1)*(1/b - 1)*df1/df2) + int(not cnd)*2*b


###################################################################################
def mdep(syy, nw, wy, w=[]):
    nw[nw < 1e-6] = 1e-6
    if syy.ndim == 1:
        m = 1; [Luy] = syy.shape
    else:
        [m, Luy] = syy.shape
    my = syy/repmat(nw, 1, Luy)
    mmy = my.max(axis=0)
    if not isinstance(mmy, np.ndarray): mmy = np.array([[mmy]])
    mmy[mmy < 1e-6] = 1e-6  # !!! works for ytp = 'bin'
    if len(w) == 0: w = r_(wy/mmy)
    ww = repmat(w, m, 1)
    x = my*ww
    if not isinstance(w, np.ndarray): w = np.array([[w]])
    return x, w


###################################################################################
def minobs(bns, nd, xtp):
    i = 0
    while i < len(bns) - 1:
        i = i + 1
        if bns[i]['nw'] < nd:
            bns = mrgbns(bns, i, xtp=xtp)
            i = i - 1
    if len(bns) <= 1:
        return bns
    if bns[len(bns)]['nw'] < nd:
        bns = mrgbns(bns, len(bns) - 1, xtp=xtp)
    return bns


###################################################################################
def mrgbns(bns, i, j=np.nan, xtp='num'):
    if np.isnan(j): j = i + 1
    if xtp == 'nom' or xtp == 'ord':
        if len(bns[i]['lb']) == 0:
            bns[i]['lb'] = bns[j]['lb']
        else:
            bns[i]['lb'] = num2lst(np.unique(np.append(bns[i]['lb'], bns[j]['lb'])))
    else:
        bns[i]['rb'] = bns[j]['rb']
    bns[i]['nw'] = bns[i]['nw'] + bns[j]['nw']
    bns[i]['n'] = bns[i]['n'] + bns[j]['n']
    if 'y' in bns[i].keys():
        for h in range(len(bns[i]['y'])): bns[i]['y'][h + 1] = sumls(bns[i]['y'][h + 1], bns[j]['y'][h + 1])
        for h in range(len(bns[i]['y2'])): bns[i]['y2'][h + 1] = sumls(bns[i]['y2'][h + 1], bns[j]['y2'][h + 1])
    cnd_i = bns[i]['type'] == 'Other' or bns[i]['type'] == 'Missing' or bns[i]['type'] == 'Special Value'
    cnd_i1 = bns[j]['type'] == 'Other' or bns[j]['type'] == 'Missing' or bns[j]['type'] == 'Special Value'
    if cnd_i and cnd_i1:
        bns[i]['type'] = 'Mixed OMS'
    else:
        bns[i]['type'] = 'Normal'
    for k, l in zip(range(j, len(bns)), range(j + 1, len(bns) + 1)): bns[k] = bns[l]
    del bns[len(bns)]
    return bns


###################################################################################
def nabub(x, w, sv, xtp, ux, y, ytp, yi):
    if isinstance(ytp, str): ytp = [ytp]
    x_not_nan = ~np.isnan(x)
    x = x[x_not_nan.flatten(), 0]
    w = w[x_not_nan.flatten(), 0]
    if len(y): y = y[x_not_nan.flatten(), :]
    if not ux:   ux = np.unique(x)
    for i in sv: ux = list(filter(lambda a: a != i, ux))
    nu = len(ux)
    if nu == 0: bns = []
    cnt = 0
    bns = {}
    if len(y):
        bns[1] = setbin([0], [0], xtp, 'Normal', zeros((1, len(ytp))), ytp, yi)
    else:
        bns[1] = setbin([0], [0], xtp, 'Normal')
    #    bns[nu] = setbin([0], [0], xtp, 'Normal')
    for i in range(nu):
        xi = ux[i]
        ind = x == ux[i]
        cnt = cnt + 1
        if len(y):
            bns[cnt] = setbin(xi, w[ind], xtp, 'Normal', y[ind, :], ytp, yi)
        else:
            bns[cnt] = setbin(xi, w[ind], xtp, 'Normal')
    if cnt == 0: bns = {}
    return bns


###################################################################################
def passCrit(df, df_den, bm12, pt, ytp, ba):
    tol = 1e-3
    df2 = df/2
    df_den2 = df_den/2
    if ytp[0] == 'bin':
        if ba:
            apt = pt/bm12
        else:
            apt = pt
        left = 0
        right = -4*df2*np.log(apt)
        dummy = 1;
        if apt < 1e-200:
            crt_pass = right
        else:
            crt_pass = inv_distr('Chi2', apt, dummy, df2, left, right, tol)
    else:
        left = 0
        right = 1
        crt_pass = inv_distr('Fisher', pt, df_den2, df2, left, right, tol)
    return crt_pass


###################################################################################
def permints(n, m, init=True):
    s = np.array([])
    p = n - m + 1
    if m == 2:
        bng = np.arange(0, p).reshape((p, 1))
        bng_new = np.arange(p - 1, -1, -1).reshape((p, 1))
        s = np.hstack((bng, bng_new))
    if m > 2:
        i_iter = np.arange(0, p)
        for i in i_iter:
            bng = permints(m - 1 + i, m - 1, False)
            bng_new = np.tile(p - 1 - i, bng.shape[0]).reshape((bng.shape[0], 1))
            if s.shape[0] == 0:
                s = np.hstack((bng, bng_new))
            else:
                s = np.vstack((s, np.hstack((bng, bng_new))))
    if init and s.shape[0] != 0: s += 1
    return s


###################################################################################
def reduce_bns1(bns, xtp, ytp, gd=None, bd=None, nd=None):
    my = lambda g, nw: g/max(1, nw)
    cnd_mrg_ybin = lambda g, b, gd, bd, p1: g < gd and g*p1 < 1 or b < bd and b*p1 < 1  # merge condition for ytp = 'bin'
    cnd_mrg_ynum = lambda nw, nd: nw < nd                                               # merge condition for ytp = 'num'

    bng = copy.deepcopy(bns)
    if xtp == 'nom':    bns = sort_bins(config, bns, my, BUS_groups)
    if ytp[0] == 'bin':
        [__, nw, g, __, __] = bns2arr(bns)
        b = nw - g
        try:
            pg = b.sum()/nw.sum()
            p1 = min([pg, 1 - pg])
        except:
            raise Exception('In REDUCE_BNS1(): Bins statistics are wrong.')
    keep_bin = 1
    while keep_bin < len(bns) - 1:
        nwi = bns[keep_bin]['nw']
        drop_bin = keep_bin + 1
        bin_type_drop = bns[drop_bin]['type']
        if bin_type_drop == 'Missing':
            drop_bin = keep_bin - 1
            bin_type_drop = bng[drop_bin]['type']
        if ytp[0] == 'bin':
            gi = bns[keep_bin]['y'][1][0] # y - single output => key is 1
            bi = nwi - gi
            if bin_type_drop != 'Missing' and cnd_mrg_ybin(gi, bi, gd, bd, p1):
                if keep_bin < drop_bin: bns = mrgbns(bns, keep_bin, drop_bin, xtp=xtp)
                else:                   bns = mrgbns(bns, drop_bin, keep_bin, xtp=xtp)
            else:
                keep_bin += 1
        elif ytp[0] == 'num':
            if bin_type_drop != 'Missing' and cnd_mrg_ynum(nwi, nd):
                if keep_bin < drop_bin: bns = mrgbns(bns, keep_bin, drop_bin, xtp=xtp)
                else:                   bns = mrgbns(bns, drop_bin, keep_bin, xtp=xtp)
            else:
                keep_bin += 1
    return bng


###################################################################################
def reduce_bns2(bns, xtp, ytp, md, mar):
    lpm = np.log(1e4)
    kk = np.arange(md + 2, 1e5 + 1)
    kkk = ((kk - 1)*np.log(kk - 1) - (kk - md)*np.log(kk - md) - (md - 1)*np.log(md - 1))[::-1]
    ind = np.arange(len(kkk))[::-1]
    mmax = ind[kkk < lpm].max() + md + 2 + 1
    m = len(bns)
    s = np.ones((m, 1))
    while m > mmax:
        [__, nw, sy, sy2, __] = bns2arr(bns)
        na = nw[:-1]
        nb = nw[1:]

        cnd = list((na == 0) & (nb == 0))
        if any(cnd):
            cnt_max = cnd.index(True)
        else:
            ya = sy[:-1]
            yb = sy[1:]
            y2a = sy2[:-1]
            y2b = sy2[1:]
            dC = (y2a + y2b)/(na + nb) - y2a/na - y2b/nb
            dC[dC > 0] = 0
            cnd = na + nb <= mar
            if np.any(cnd):
                isc = np.arange(1, len(cnd) + 1)[cnd.flatten()]
                __, idCm = max1(dC[cnd])
                cnt_max = isc[idCm]
            else:
                __, idCm = max1(dC)
                cnt_max = idCm + 1

        if cnt_max == len(nw) - 1: cnt_max -= 1
        bns = mrgbns(bns, cnt_max, xtp=xtp)
        s[cnt_max - 1] += s[cnt_max]
        s = np.delete(s, cnt_max)
        m = len(bns)
    [__, nw, sy, sy2, __] = bns2arr(bns)
    s = np.array(s, dtype=int)
    return bns, s, sy, sy2, nw


###################################################################################
def sbng(bng, md=5, crt=None, skip_mos=['m', 'o', 'sv'], met_dist='manh', met='co1y', nmin_uy=[50, 50, 50], mar=np.inf, pt=0.05, ba=0, maxprm=20000, dGBInd=5, tolmindGBInd=5, mt=np.nan, minB=50, tolminB=20, stats=True, dsp=False):
    bng = new(bng)
    if isinstance(bng, list):   m = len(bng)
    else:                       m = 1
    sb = [None]*m
    for i in range(m):
        if dsp: tic5()
        sb[i] = {}
        if m == 1:  bns = bng['bns'];       cname = bng['cname'];       xtp = bng['xtp'];       ytp = bng['ytp']
        else:       bns = bng[i]['bns'];    cname = bng[i]['cname'];    xtp = bng[i]['xtp'];    ytp = bng[i]['ytp']
        if isinstance(ytp, str): ytp = [ytp]
        bns, bns_1 = skipmosbns(bns, skip_mos)
        xtp1 = xtp
        if xtp == 'nom':
            [n, nw, syy, syy2, wy] = bns2arr(bns)
            [x, w] = mdep(syy, nw, wy)
            ix = (x@w.T).argsort(axis=0) + 1
            bins = {}
            for j in range(len(ix)): bins[j + 1] = bns[ix.flatten()[j]]
            bns = bins
            xtp1 = 'ord'
        if met == 'hclust':
            bns, map, D = spih_sb_hclust(bns, xtp1, md, met_dist)
        elif met == 'co1y':
            bd = nmin_uy[0]
            gd = nmin_uy[1]
            nd = nmin_uy[2]
            bns, map, D = spih_sb_co1y(bns, crt, xtp1, ytp, md, gd, bd, nd, mar, pt, ba, dGBInd, tolmindGBInd, mt, minB, tolminB, maxprm, dsp, cname)
        flg = 0
        if bns is None:
            bns = bng[i]['bns']
            for j in range(len(bns), 1, -1):
                if bns[j]['type'] == 'Normal' and bns[j - 1]['type'] == 'Normal':
                    bns = mrgbns(bns, j-1, xtp=xtp)
            sb[i]['bns'] = bns
            sb[i]['map'] = np.hstack((c_(np.arange(len(bns))), ones(len(bns), 1)))
            flg = 1
        else:
            sb[i]['bns'] = bns
            sb[i]['map'] = map
        if not flg:
            for j in range(len(bns_1)): sb[i]['bns'][len(sb[i]['bns']) + 1] = bns_1[j + 1]
        if m == 1:  sb[i]['cname'] = bng['cname']
        else:       sb[i]['cname'] = bng[i]['cname']
        sb[i]['xtp'] = xtp
        sb[i]['ytp'] = ytp
        # sb[i]['st'] = {}
        # if met == 'co1y' and ytp[0] == 'bin':   sb[i]['st']['Chi2'] = D
        # if met == 'co1y' and ytp[0] == 'num':   sb[i]['st']['Fratio'] = D
        # elif met == 'hclust':                   sb[i]['st']['D'] = D
        if stats: sb[i] = stbng('sb', sb[i], xtp, ytp)

    if m == 1:
        return sb[0]
    else:
        return sb


###################################################################################
def setbin(x, w, xtp, btp, y=m_([],0), ytp='', yi=[]):
    bn = {}
    if 'num' in xtp:
        if np.any(np.isnan(x)):
            bn['lb'] = [np.nan]
            bn['rb'] = [np.nan]
        else:
            if (isinstance(x, np.ndarray) or isinstance(x, list)) and len(x) == 0:
                bn['lb'] = []
                bn['rb'] = []
            else:
                bn['lb'] = m_([np.min(x)])
                bn['rb'] = m_([np.max(x)])
    else:
        if ~np.any(np.isnan(x)):
            bn['lb'] = np.unique(x).tolist()
        else:
            bn['lb'] = [np.nan]
        bn['rb'] = []
    bn['type'] = btp

    bn = binst(bn, 'setbin', y, w, ytp, yi)

    # bn['nw'] = np.sum(w)
    # bn['n'] = len(w)
    # if bn['n'] == 1 and not bn['lb']:
    #     bn['n'] = 0
    # if len(y):
    #     ###########
    #     if y.ndim == 1: y = c_(y)
    #     b = {}
    #     b2 = {}
    #     for i in range(len(ytp)):
    #         yh = y[:, i]
    #         if ytp[i] == 'nom' or ytp[i] == 'ord':
    #             if yi != []:  yii = yi[i]
    #             else:         yii = np.unique(y[~np.isnan(y[:, i]), i])
    #             c = nans((1,len(yii)))
    #             for j in range(len(yii)):
    #                 jj = list(yh == yii[j])
    #                 if jj != []:    c[j] = sum(wh[jj])
    #                 else:           c[j] = 0
    #             bn['y'][i + 1] = c
    #             bn['y2'][i + 1] = c
    #         else:
    #             if len(y):
    #                 b[i + 1] = [np.sum(w*yh)]
    #                 b2[i + 1] = [np.sum(w*yh**2)]
    #             else:
    #                 b[i + 1] = [0]
    #                 b2[i + 1] = [0]
    #         bn['y'] = b
    #         bn['y2'] = b2
    #     ###########
    return bn


###################################################################################
def setyi(y, ytp):
    if isinstance(ytp, str): ytp = [ytp]
    r = len(ytp)
    yi = [None]*r
    for i in range(r):
        if ytp[i] == 'num' or ytp[i] == 'bin':
            yi[i] = []
        else:
            yi[i] = np.unique(y[~np.isnan(y[:, i]), i])
    return yi


###################################################################################
def skipmosbns(bns, skip_mos):
    k = 1
    bns_1 = {}
    for i in range(len(bns), 0, -1):
        try:
            if 'Missing' in bns[i]['type'] and 'm' in skip_mos:
                bns_1[k] = bns[i]
                k += 1
                bns = {key: val for key, val in bns.items() if key != i}
        except:
            pass
        try:
            if 'Other' in bns[i]['type'] and 'o' in skip_mos:
                bns_1[k] = bns[i]
                k += 1
                bns = {key: val for key, val in bns.items() if key != i}
        except:
            pass
        try:
            if 'Special Value' in bns[i]['type'] and 'sv' in skip_mos:
                bns_1[k] = bns[i]
                k += 1
                bns = {key: val for key, val in bns.items() if key != i}
        except:
            pass
    return bns, bns_1


###################################################################################
def sort_bins(vname, config, unordered_bins, bin_order_function):
    sorting_criteria = []
    ranking_criteria = []
    for bn in unordered_bins:

        if bn[-1]['type'] != 'missing':
            sorting_criteria.append(bin_order_function(bn[-1]['statistics']))
        elif bn[-1]['type'] == 'missing' and unordered_bins[-1][-1]['statistics']['number_of_records'] >= \
                config['parameters']['fc_mir']:
            pass
        else:
            # Do not use the missings not statistically significant number of NaNs
            if 'Use_NA' in config['variables'][vname]:
                config['variables'][vname].pop('Use_NA')

    sorting_order = np.argsort(sorting_criteria)

    ordered_bins = []
    for s in sorting_order:
        ordered_bins.append(unordered_bins[s])
    ordered_bins.append(unordered_bins[-1])

    return ordered_bins


###################################################################################
def spih(bns, xtp, md, nd, met):
    Nw = 0
    for k in bns: Nw = Nw + bns[k]['nw']
    m = len(bns)
    Nd = Nw/md
    i = 0
    iold = 1
    s = 0
    while m >= i + 2:
        s = s + 1
        i = i + 1
        if xtp == 'num' or xtp == 'ord':
            ni2 = bns[i]['nw'] + bns[i + 1]['nw']
            if ni2 <= Nd or bns[i]['nw'] <= nd:
                bns = mrgbns(bns, i, xtp=xtp)
                i = i - 1
            else:
                d_aft = ni2 - Nd
                d_bef = Nd - bns[i]['nw']
                if d_bef > d_aft:
                    bns = mrgbns(bns, i, xtp=xtp)
        else:
            c = []
            for k in range(len(bns) - i): c.append(bns[i + k + 1]['nw'])
            ni2 = bns[i]['nw'] + c
            imrg = find((ni2 <= Nd) | (bns[i]['nw'] <= nd)) + i + 1
            if any(imrg):
                leng = len(imrg)
                jj = range(0, leng)
                r = rand(l=0, h=leng - 1, tp='int', seed=s)
                bns = mrgbns(bns, i, imrg[jj[r[0, 0]]], xtp=xtp)
                i = i - 1
            else:
                r = rand(l=0, h=len(ni2) - 1, tp='int', seed=s)
                d_aft = ni2[r] - Nd
                d_bef = Nd - bns[i]['nw']
                if d_bef > d_aft:
                    bns = mrgbns(bns, i, r[0, 0] + 1, xtp=xtp)
        m = len(bns)
        if met == 'enr' and iold < i:
            sm = 0
            for k in range(1, i + 1): sm = sm + bns[k]['nw']
            iold = i
            if md == i and m <= md: break

    while m > md:
        if xtp == 'num' or xtp == 'ord':
            ni2 = []
            for k, l in zip(range(1, len(bns)), range(2, len(bns) + 1)):
                ni2.append([bns[k]['nw'] + bns[l]['nw']])
            i = np.argmin(ni2) + 1
            bns = mrgbns(bns, i, xtp=xtp)
        else:
            c = []
            for k in range(len(bns)): c.append(bns[k + 1]['nw'])
            ni2 = np.kron(np.ones((m, 1)), c) + np.kron(np.ones((m, 1)), c).T
            np.fill_diagonal(ni2, float('inf'))
            ij = np.argmin(ni2) + 1
            [i, j] = ind2sub(np.array([m, m]), ij)
            bns = mrgbns(bns, min(np.array([i, j])) + 1, max(np.array([i, j])) + 1, xtp=xtp)
        m = len(bns)
    if bns[len(bns)]['nw'] < nd:
        if xtp == 'num' or xtp == 'ord':
            bns = mrgbns(bns, m - 1, xtp=xtp)
        else:
            c = []
            for k in range(1, len(bns)): c.append(bns[k]['nw'])
            ni2 = bns[len(bns)]['nw'] + c
            i = np.argmin(ni2) + 1
            bns = mrgbns(bns, i, m, xtp=xtp)
    return bns


###################################################################################
def spih_erv(x, w, xtp, md, sv):
    ir = [np.isnan(x)]
    for k in range(len(sv)):
        for l in range(len(ir[0])):
            ir[0][l] = ir[0][l] or x[l] == sv[k]
    x = x[~ir[0]]
    xmin = min(x)
    xmax = max(x)
    s = (xmax - xmin)/md
    b = np.arange(xmin, xmax + s, s)
    b = np.round(b, 4)
    lb = b[0:len(b) - 1]
    rb = b[1:len(b) - 1]
    rb = np.append(rb, float('inf'))
    bns = {}
    for k in range(int(md)):
        bns[k + 1] = setbin([], [], xtp, 'Normal')
    for k in range(int(md)):
        ii = []
        for l in range(len(x)):
            ii.append(x[l] >= lb[k] and x[l] < rb[k])
        bns[k + 1] = setbin(x[ii].tolist(), w[0:len(ii):1][ii].tolist(), xtp, 'Normal')
        bns[k + 1]['lb'] = [lb[k]]
        bns[k + 1]['rb'] = [rb[k]]
    return bns


###################################################################################
def spih_sb_co1y(bns, crt, xtp, ytp, md, gd, bd, nd, mar, pt, ba, dGBInd, tolmindGBInd, mt, minB, tolminB, maxprm, dsp, cname=''):
    if crt is None:
        if ytp[0] == 'bin':     crt = 'chi2'
        elif ytp[0] == 'num':   crt = 'frat'
    if bns is None or len(bns) == 0:
        bns_b = {}
        crit_b = None
        return bns_b, [], crit_b
    map = nans((len(bns), 2))
    bns1 = copy.deepcopy(bns)
    if len(ytp) == 1:
        if ytp[0] == 'bin':     bns1 = reduce_bns1(bns1, xtp, ytp, gd=gd, bd=bd)
        elif ytp[0] == 'num':   bns1 = reduce_bns1(bns1, xtp, ytp, nd=nd)
    else: raise Exception('In SPIH_SB_CO1Y: Single output is expected, but many outputs are identified.')
    mm = range(2, min([len(bns1), md]) + 1)  # number of bins to try
    if ytp[0] == 'bin':
        [__, nw, g, __, __] = bns2arr(bns1)
        Dind = dind(g, nw - g)
    crit_b = nans((md - 1,))
    bns_b = [None]*(md - 1)
    pvalc_b = nans((md - 1,))
    br = 0
    for md in mm:
        bns1 = new(bns1)
        bns1, __, g, g2, nw = reduce_bns2(bns1, xtp, ytp, md, mar)
        m = len(bns1)
        if ba:  pass  # [bm1, bm2] = bonfadj(mp, k, md, xtp)
        else:   bm1 = bm2 = 1
        Nw = sum(nw)
        df = md - 1
        df_den = Nw - md
        CritPass = passCrit(df, df_den, bm1*bm2, pt, ytp, ba)
        s2 = permints(m, md)  # s2 - set of all merges to be investigated
        if s2.shape[0] != 0:
            gg, gg2, nn = stbngs(s2, g, g2, nw)
            if ytp[0] == 'bin':
                ngg = nn - gg
                Crit0 = chi2(gg, ngg)
                cnd_GBI = cnd_gbi(gg, ngg, dGBInd, tolmindGBInd, Dind)
                min_cls = gg; min_cls[ngg < gg] = ngg[ngg < gg]
                cnd_mirc = np.min(min_cls, axis=0) > minB - tolminB*Dind # min records from minority class
                cnd_mar = np.max(nn, axis=0) <= mar
                cnd = cnd_GBI & cnd_mirc & cnd_mar
            else:
                Crit0 = frat(gg, gg2, nn)
                cnd = np.full((gg.shape[1],), True)
            
            Crit = Crit0
            # ii = repmat(0:md:size(gi, 2)*md - 1, md, 1);
            # if critg == 'Gini':         [~, ign] = sort(gi./nwi);  Crit = gini1(gi(ign + ii), ngi(ign + ii))
            # elif critg == 'Chi2'
            #     if ytp[0] == 'bin':     Crit = Crit0
            #     else:                   Crit = chi2(gg, ngg)
            # elif critg == 'Vinf':       Crit = vinf1(gi, ngi)
            # elif critg == 'Twoing':     [~, ign] = sort(gi./nwi); Crit = twoing(gi(ign + ii), ngi(ign + ii))
            # elif critg == 'FRatio':
            #     if ytp[0] == 'num':     Crit = Crit0
            #     else:                   Crit = frat(gg, gg2, nn)[0, :]
            # elif critg == 'InfoStr':    [~, ign] = sort(gi./nwi); Crit = infoStr(gi(ign + ii), ngi(ign + ii))
            # else: raise Exception('In SPIH_SB_CO1V(): Unknown critb.') 
            
            cnd_TRND = cnd_trnd(s2.shape[0], gg, nn, md, mt)
            if crt == 'maxb':
                cnd = cnd_TRND
                if not np.any(np.isnan(Crit)):  Crit = Crit/np.max(Crit) + np.min(d_(gg/nn), axis=0)/np.max([1e-6, np.max(d_(r_(np.min(d_(gg/nn).T, axis=0))))])
                else:                           Crit = ones(Crit.shape)
                Crit[np.isnan(Crit)] = 0
            else:
                cnd_pt = Crit0 >= CritPass
                cnd = cnd & cnd_TRND & cnd_pt
            if np.any(cnd & (~np.isnan(Crit))):
                ib = np.arange(len(cnd))[cnd.flatten()]
                crit_b[br], ic = max1(Crit[cnd.flatten()])
                v = md - 1
                pvalc_b[br] = pvalC(v, crit_b[br])[0, 0]
                ind = ib[ic]
                bns_b[br] = best_merge(bns1, s2[ind,], xtp)
            else:
                crit_b[br] = np.nan
                pvalc_b[br] = np.nan
                bns_b[br] = None
                            
            if dsp: print('Run SB: ', br + 1, '/', m, cname, ',      time: ', toc5(dsp=False))

        else:
            crit_b[br] = np.nan
            pvalc_b[br] = np.nan
            bns_b[br] = None
        br += 1
    if np.any(np.isnan(crit_b) == False):
        # crit_b, ind = max1(crit_b, naskip=True)
        if crt == 'maxb':
            bn = []
            for i in range(len(bns_b)):
                if bns_b[i] == None: continue
                bn.append(len(bns_b[i]))
            _, ind = max1(m_(bn))
            crit_b = crit_b[ind]
            bns_b = bns_b[ind]
        else:
            _, ind = min1(pvalc_b, naskip=True)
            crit_b = crit_b[ind]
            bns_b = bns_b[ind]
    else:
        bns_b = None
        crit_b = np.nan
    #    print('sb: ', round((time.time() - loop_time), 3), 'sec')
    if not bns_b is None:
        for i in range(1, len(bns)+1):
            if xtp == 'num':
                for j in range(1, len(bns_b)+1):
                    if bns[i]['lb'] >= bns_b[j]['lb'] and bns[i]['rb'] < bns_b[j]['rb']:
                        map[i-1, :] = [i, j]
                        continue
            else: # xtp is 'nom' or 'ord'
                for j in range(1, len(bns_b)+1):
                    if np.any(m_(bns[i]['lb']) == m_(bns_b[j]['lb'])):
                        map[i-1, :] = [i, j]
                        continue

    return bns_b, map.astype(int), crit_b


###################################################################################
def spih_sb_hclust(bns, xtp, md, met_dist):
    m = len(bns)
    [n, nw, syy, __, wy] = bns2arr(bns)
    [x, w] = mdep(syy, nw, wy)
    [D, ind] = dist1(x, w, met_dist, xtp)
    ind1 = num2lst(np.arange(m))

    interate = md < m
    x1 = x
    while interate:
        if D.size == 0: ii = [];
        ii = np.argmin(D)
        ind1[min(ind[ii, :])] = [ind1[i] for i in ind[ii, :]]
        del ind1[max(ind[ii, :])]
        bns = mrgbns(bns, min(ind[ii, :]) + 1, xtp=xtp)
        ia = min(ind[ii, :])
        syy[ia, :] = sum(syy[ind[ii, :], :])
        nw[ia] = sum(nw[ind[ii, :]])
        syy = np.delete(syy, max(ind[ii, :]), axis=0)
        nw = np.delete(nw, max(ind[ii, :]), axis=0)
        if syy[ia, :].ndim == 1:
            [xnew] = mdep(syy[ia, :], nw[ia], wy, w=w)[0]
        else:
            [xnew] = mdep(np.sum(syy[ia, :], 1), np.sum(nw[ia]), wy, w)[0]
        x1[ia, :] = xnew
        x1 = np.delete(x1, max(ind[ii, :]), axis=0)
        if ii > 0:     [D[ii - 1]] = dist1(x1[[ia, ia - 1], :], w, met_dist, xtp)[0]
        if ii < m - 2: [D[ii + 1]] = dist1(x1[[ia, ia + 1], :], w, met_dist, xtp)[0]
        D = np.delete(D, ii, axis=0)
        m = m - 1
        if m == md: interate = 0
    return bns, [], D


###################################################################################
def stbng(met, bng, xtp, ytp, x=np.empty((0, 0)), y=np.empty((0, 0)), w=np.empty((0, 0))):
    bns = bng['bns']
    if bns is None: return None, None
    if met == 'ub': bns = stbnsy(bns, x, y, w, xtp, ytp)

    st = {}
    if bns == {}: s = []; return st
    r = len(ytp)
    m = len(bns)
    mn = 0  # number of not empty bins
    Nw = 0
    for h in range(1, m + 1):
        if bns[h]['n'] > 0: mn += 1
        Nw = Nw + bns[h]['nw']
    n = nans((mn,))
    nw = nans((mn,))
    hh = 0
    for h in range(1, m + 1):
        if bns[h]['n'] > 0:
            n[hh] = bns[h]['n']
            nw[hh] = bns[h]['nw']
            hh += 1

    for i in range(r):
        ytpi = ytp[i]
        nyi = len(bns[1]['y'][i + 1])
        if nyi > 1:
            sy = nans((mn, nyi))
            sy2 = nans((mn, nyi))
            hh = 0
            for h in range(1, m + 1):
                # if ytpi == 'nom' or ytpi == 'ord': continue # todo: should collect sy and sy2 also for categorical variables - len(sy) = len(sy2) = len(nyi). Currently len(bns[h + 1]['y'][i + 1]) varies for different h, but should be nyi.
                if bns[h]['n'] > 0:
                    sy[hh] = bns[h + 1]['y'][i + 1]
                    sy2[hh] = bns[h + 1]['y2'][i + 1]
                    hh += 1
        else:
            sy = nans((mn,))
            sy2 = nans((mn,))
            hh = 0
            for h in range(1, m + 1):
                if bns[h]['n'] > 0:
                    sy[hh] = bns[h]['y'][i + 1][0]
                    sy2[hh] = bns[h]['y2'][i + 1][0]
                    hh += 1
            nw = c_(nw)
            sy = c_(sy)
            sy2 = c_(sy2)

        Sy = sy.sum(axis=0)
        s = {}
        if ytpi == 'bin':
            s['sy'] = sy
            syb = np.array(nw - sy)
            s['syb'] = syb
            s['pnw'] = nw/Nw*100
            s['py0'] = np.dot(sy, np.linalg.pinv(Sy[np.newaxis]))*100
            s['py1'] = np.dot(syb, np.linalg.pinv([Nw - Sy]))*100
            temp = s['py0']; temp[np.isnan(temp)] = 0
            s['cp0'] = np.cumsum(temp)
            temp = s['py0']; temp[np.isnan(temp)] = 0
            s['cp1'] = np.cumsum(temp)
            nw1 = nw
            nw1[nw < 1e-12] = 1e-12
            s['my0'] = np.array(syb/nw1)
            s['my1'] = np.array(sy/nw1)
            s['gbind'] = gbi(sy, syb)
            syb1 = syb
            syb1[syb < 1e-12] = 1e-12

            s['odds'] = sy/syb
            s['Gini'] = gini(sy, syb)
            s['WoE'] = woe(sy, syb)
            s['KS'] = ks(sy, syb)
            s['Vin'] = vinf(sy, syb)
            s['D'] = dind(sy, syb)
            #if m == 2: s['twoing'] = twng(sy, syb)
            s['Chi2'] = chi2(sy, syb)
        elif ytpi == 'num':
            s['sy'] = sy
            s['pnw'] = nw/Nw*100
            s['my'] = sy/nw
            eps = 1e-6
            nw1 = copy.deepcopy(nw)
            nw1[(nw - 1) < eps] = eps + 1
            s['vary'] = sy2/nw1
            s['Frat'] = frat(sy, sy2, nw)
        else:
            s = []
        st[i] = s
        hh = 0
        for h in range(1, m + 1):
            if 'WoE' in s and bns[h]['n'] > 0:  bns[h]['woe'] = s['WoE'][hh, 0]
            else:                               bns[h]['woe'] = None
            if 'my1' in s and bns[h]['n'] > 0:  bns[h]['my'] = s['my1'][hh, 0]
            else:                               bns[h]['my'] = None
            if 'my' in s and bns[h]['n'] > 0:   bns[h]['my'] = s['my'][hh, 0]
            else:                               bns[h]['my'] = None
            if bns[h]['n'] > 0: hh += 1
    bng['bns'] = bns
    bng['st'] = st
    return bng
###################################################################################
def stbngs(s, sy, sy2, nw):
    Np, md = s.shape
    SY = nans(md, Np)
    SY2 = nans(md, Np)
    NW = nans(md, Np)
    for i in range(0, Np):
        i1 = 0
        i2 = 0
        j = 0
        for si in s[i]:
            i2 += si
            if i2 - i1 == 1:
                SY[j, i] = sy[i1, 0]
                SY2[j, i] = sy2[i1, 0]
                NW[j, i] = nw[i1, 0]
            else:
                SY[j, i] = sy[i1:i2, 0].sum(0)
                SY2[j, i] = sy2[i1:i2, 0].sum(0)
                NW[j, i] = nw[i1:i2, 0].sum(0)
            j += 1
            i1 = i2
    return SY, SY2, NW
###############################################################################
def ubng(x, xtp, w=None, md=100, prcd=1, nmin=50, met='enr', sv=[], xi_order=[], y=m_([],0), ytp='', yi=[], cnames=None, stats=False, dsp=False):
    m = x.shape[1]
    if cnames is None: cnames = ['var_' + str(i) for i in range(m)]
    if w is None: w = ones(x.shape)
    ub = [None]*m
    if isinstance(xtp, str): xtp = [xtp]*m
    # if isinstance(sv, str): xtps = [sv]*m
    # if isinstance(xi_order, str): xtps = [xi_order]*m
    # if isinstance(mt_order, str): xtps = [mt_order]*m
    for i in range(m):
        if dsp: tic5()
        ub[i] = {}
        if isinstance(x, pd.DataFrame): xi = c_(x.iloc[:, i].values)
        else:                           xi = x
        xtpi = xtp[i]
        if len(y) == 0:
            ytp = ''
            yi = []
        else:
            if len(yi) == 0: yi = setyi(y, ytp)
        if met == 'epp': md = 100/prcd
        N = len(xi)
        if met == 'enr' or met == 'epp' or met == 'svc':
            bns = nabub(xi, w, sv, xtpi, xi_order, y, ytp, yi)
            if not met == 'svc':
                if len(bns) > md: bns = spih(bns, xtpi, md, nmin, met)
                bns = minobs(bns, nmin, xtpi)
        elif met == 'erv':
            if xtpi == 'nom':
                bns = {}
                raise SystemExit('Binning method "Equal Ranges of Values" is not applicable for Nominal variables...')
            bns = spih_erv(xi, w, xtpi, md, sv)
        else:
            raise SystemExit('Unknown binning method...')
        flg = 0
        if len(bns) <= 1: flg = 1
        if not flg and xtpi == 'num':
            for k in range(1, len(bns)): bns[k]['rb'] = bns[k + 1]['lb']
            bns[1]['lb'] = [-np.inf]
            bns[len(bns)]['rb'] = [np.inf]
        if 'bns' in locals() and not bns == 0:
            bns = binMOS(bns, xi, w, sv, xtpi, y, ytp, yi)
        else:
            bns = {}
        ub[i]['bns'] = bns
        ub[i]['cname'] = cnames[i]
        ub[i]['xtp'] = xtpi
        ub[i]['ytp'] = ytp
        
        if stats: ub[i] = stbng('ub', ub[i], xtpi, ytp, x=x, y=y, w=w)
        
        if dsp: print('Run UB: ', i + 1, '/', m, cnames[i], ',      time: ', toc5(dsp=False))

    if m == 1:
        return ub[0]
    else:
        return ub

###################################################################################
# CROSS BINNING
###################################################################################
def cbng(segment, f_obj, x, y, w=None, xtp=None, ytp=None, args=None, tpg='int', mod_indv='seq2', Nind=100, mut_rate=50, mut_strength=2, mut_met='Gauss', mut_stdev=None, pairing_met='Fbest', select_met='Fhalf', itrConstF=10, maxiter=1000, dsp=False):
    args['lb1'] = np.min(x[:, 0])
    args['ub1'] = np.max(x[:, 0])
    args['lb2'] = np.min(x[:, 1])
    args['ub2'] = np.max(x[:, 1])
    args['minx'] = np.min(np.min(x))
    args['maxx'] = np.max(np.max(x))
    args['mod_indv'] = 'seq2'
    n = [args['nc1'], args['nc2']]
    nc1 = args['nc1']
    nc2 = args['nc2']
    lb = [args['lb1'], args['lb2']]
    ub = [args['ub1'], args['ub2']]

    # ub = ubng(x=x, xtp=xtp, md=maxs, prcd=1e-6, nmin=1, met='svc', sv=[], xi_order=xi_order, y=c_(y), ytp=ytp, yi=[], cnames=None, stats=True, dsp=False)  # x - ord
    # sb = sbng(ub, md=maxs, crt='maxb', skip_mos=['m', 'o', 'sv'], met_dist='manh', met='co1y', nmin_uy=m_([0, 0, 1]) * np.min(np.min(w1)) * 1e-3, mar=1, pt=1, ba=0, maxprm=20000, dGBInd=1e-3, tolmindGBInd=1e-3, mt=1, minB=0, tolminB=0, stats=True, dsp=False)  # x - ord

    # ##############################################################################
    if dsp: tic2()
    F_opt, x_opt = genopt(f_obj, args, n=n, lb=lb, ub=ub, tpg=tpg, mod_indv=mod_indv, Nind=Nind, mut_rate=mut_rate, mut_strength=mut_strength, mut_met=mut_met, mut_stdev=mut_stdev, pairing_met=pairing_met, select_met=select_met, itrConstF=itrConstF, maxiter=maxiter, dsp=dsp)
    if dsp: toc2()
    # if segment == 'NewClients':
    #     F_opt = 2091.872486576107
    #     x_opt = np.array([285., 554., 885., 664., -75., 557., 709., 649.])
    # else:
    #     F_opt = 13.451735270013074
    #     x_opt = np.array([ 142.,  726.,  364.,  608., -350.,  326.,  509.,  717.])
    # ##############################################################################
    x1, ss = sort(c_(x_opt[:n[0], ]))
    x2, ss = sort(c_(x_opt[n[0]:, ]))
    x_opt = np.vstack((x1, x2)).flatten()
    # if dsp: print('F_opt:', F_opt, '\nx_opt', x_opt)
    if dsp: print('F_opt:', f_obj(x_opt, args), '\nx_opt', x_opt)
    # ##############################################################################

    cb = qz_best(x_opt, args, dsp)
    cb['cut_offs'] = x_opt
    cb['F_opt'] = F_opt
    return cb

###################################################################################
def cfilnans(crt, dcrt_nan, w_nan=1):
    ii, jj = find(np.isnan(crt))
    if len(ii) == 0: return crt
    crt1 = new(crt)
    w1 = ones(crt.shape)
    for h in range(len(ii)):
        i = ii[h]
        j = jj[h]
        # crt[i,j] --> NaN
        w1[i, j] = w_nan
        if i > j:  # NaN is below diag of crt
            r = find(1 - np.isnan(crt[i, j+1:])) + j + 1
            c = find(1 - np.isnan(crt[:i, j]))
            if len(c):
                max_ic = np.max(c)  # max index on not NaN quadrand in the same column - above currenrt NaN
                crt1[i, j] = crt[max_ic, j] + dcrt_nan*(i - max_ic)
            if len(r):
                min_ir = np.min(r)   # min index on not NaN quadrand in the same row
                if np.isnan(crt1[i, j]): crt1[i, j] = crt[i, min_ir] - dcrt_nan*(min_ir - j)
                else:                    crt1[i, j] = (crt1[i, j]  +  crt[i, min_ir] - dcrt_nan*(min_ir - j))/2
        else:       # NaN is below diag of crt
            r = find(1 - np.isnan(crt[i, :j]))
            c = find(1 - np.isnan(crt[i+1:, j])) + i + 1
            if len(c):
                min_ic = np.min(c)  # min index on not NaN quadrand in the same column - below currenrt NaN
                crt1[i, j] = crt[min_ic, j] - dcrt_nan*(min_ic - i)
            if len(r):
                max_ir = np.max(r)   # max index on not NaN quadrand in the same row
                if np.isnan(crt1[i, j]): crt1[i, j] = crt[i, max_ir] + dcrt_nan*(j - max_ir)
                else:                    crt1[i, j] = (crt1[i, j]  +  crt[i, max_ir] + dcrt_nan*(j - max_ir))/2
    return crt1, w1
###################################################################################
def qz_best(x, args, dsp=False):
    # Best cross binning: zones and quadrants sequence determination
    dcrt_nan = args['dcrt_nan']
    w_nan = args['w_nan']
    max_comb = args['max_comb']
    G, B, R, TGB, TGBR, crt0 = stcbng(x, args)
    crt, w1 = cfilnans(crt0, dcrt_nan, w_nan)

    x = m_()
    m, n = G.shape
    CQ = nans(m, n)
    CQ[0, 0] = 1
    CQ = [CQ]
    while np.max(CQ[0][1 - np.isnan(CQ[0]) == 1]) + 1 < m*n:
        m0, _ = max1(CQ[0], axis=-1, naskip=True)
        if dsp: tic2('permqz: ')
        CQ = permqz(CQ, max_comb, dsp)
        if dsp: toc2('permqz')
        m1, _ = max1(CQ[0], axis=-1, naskip=True)
        maxs = int(np.max(CQ[0][1 - np.isnan(CQ[0]) == 1]))
        i = 0
        for cq in CQ:
            x = nans((maxs,))
            y = nans((maxs,))
            w = nans((maxs,))
            ij = nans((maxs, 2))
            for h in range(int(maxs)):
                ii0, jj0 = find(cq == h + 1)
                ii = ii0[0]
                jj = jj0[0]
                ij[h] = [ii, jj]
                x[h] = h + 1
                y[h] = crt[ii, jj]
                w[h] = w1[ii, jj]
            xtp = 'ord'
            
            if dsp: print(i, ' from ', len(CQ))

            if dsp: tic2()
            ub = ubng(c_(x), xtp, w=c_(w), md=maxs, prcd=1e-6, nmin=1, met='svc', sv=[], xi_order=np.arange(1, maxs+1).tolist(), y=c_(y), ytp=['num'], yi=[], cnames=None, stats=True, dsp=False) # x - ord
            if dsp: toc2('ubng')
            if dsp: tic2()
            sb = sbng(ub, md=maxs, crt='maxb', skip_mos=['m', 'o', 'sv'], met_dist='manh', met='co1y', nmin_uy=m_([0, 0, 1])*np.min(np.min(w1))*1e-3, mar=1, pt=1, ba=0, maxprm=20000, dGBInd=1e-3, tolmindGBInd=1e-3, mt=1, minB=0, tolminB=0, stats=True, dsp=False)  # x - ord
            if dsp: toc2('sbng')
            if i == 0:
                sb_bst = sb
                sb_bst_y = copy.deepcopy(y)
            cnd1 = sb['st'][0]['my'][0] < sb_bst['st'][0]['my'][0]
            cnd2 = sb['st'][0]['my'][0] == sb_bst['st'][0]['my'][0]
            cnd3 = len(sb['bns']) > len(sb_bst['bns'])
            cnd5 = len(sb['bns']) == len(sb_bst['bns'])
            cnd4 = i == m * n or d_(sb['st'][0]['my'][[0, -1]]) <= d_(sb_bst['st'][0]['my'][[0, -1]])
            cnd7 = len(sb['bns']) < len(sb_bst['bns'])
            cnd6 = y[-1] < sb_bst_y[-1]

            cnd10 = y[x == m0][0] <= sb_bst_y[x == m0][0]
            cnd20 = sb['st'][0]['my'][0] == sb_bst['st'][0]['my'][0]
            cnd60 = y[x == m1][0] <= sb_bst_y[x == m1][0]
            cnd80 = np.all(d_(y[(x >= m0 + 1) & (x <= m1)]) > 0)

            #             # y_new = y[(x >= m0+1) & (x <= m1)]
            #             # cnd100 = y[y_new == np.min(y_new)] + m0
            #             for kb in sb['bns']:
            #                 if sb['bns'][kb]['type'] == 'Normal' and len(sb['bns'][kb]['lb']) > 1:
            #                     ub['bns'][sb['bns'][kb]['lb']]
            #                     pass
            # #            if i == 0 or cnd1 or cnd2 and (cnd3 or cnd5 and cnd4 or cnd7 and cnd6) or cnd10 or cnd20 and cnd60: #  and (min(d_(sb['st'][0]['my'])) >= min(d_(sb_bst['st'][0]['my'])))):
            # #            if i == 0 or cnd1 or cnd2 and (cnd3 or cnd5 and cnd4) and cnd10 and cnd20 and cnd60 and cnd80: #  and (min(d_(sb['st'][0]['my'])) >= min(d_(sb_bst['st'][0]['my'])))):
            if i == 0 or cnd1 or cnd2 and (cnd3 or cnd4 and cnd5) and cnd10 and cnd60:  # and (min(d_(sb['st'][0]['my'])) >= min(d_(sb_bst['st'][0]['my'])))):
                #     plot(sb['st'][0]['my'])
            #     plot(sb_bst['st'][0]['my'])
            #     plt.show()
                i_bst = i
                cq_bst = cq
                cb = {'ub': ub,
                      'sb': sb
                      }
                # cz_bst = nans(cq.shape)
                # map0 = sb['map']
                # map = sb['map']
                # sb = sbng(sb, md=maxs, crt='maxb', skip_mos=['m', 'o', 'sv'], met_dist='manh', met='co1y', nmin_uy=m_([0, 0, 1])*np.min(np.min(w1))*1e-3, mar=1, pt=1, ba=0, maxprm=20000, dGBInd=1e-3, tolmindGBInd=1e-3, mt=1, minB=0, tolminB=0, stats=True, dsp=False)
                # map = sb['map']
                # for im in range(map0.shape[0]):
                #     i1, j1 = find(cq == map0[im, 0])
                #     i2 = find(map0[im, 1] == map[:, 0])
                #     cz_bst[i1[0], j1[0]] = map[i2[0], 1].astype(int)
                sb_bst = sb
                sb_bst_y = copy.deepcopy(y)
            i += 1
        CQ = [CQ[i_bst]]
        
        if dsp: print(sb_bst['map'], '\n', np.hstack((c_(np.arange(1, len(sb_bst['st'][0]['my'])+1)), sb_bst['st'][0]['my'])), '\n', 'cq_bst:', cq_bst, '\n', 'Crit:', crt)
        # !!! FOR AISLAB ONLY !!!
            # sbng:
            #   y - num (continuous)
            #   eucl distance
            #   mar = -1 (max number of records to be as small as possible)
            #   mt
            #   find binning with max bins
            # cb = cbng(x1, x2, ...)
            #   /cb = {'cz': m x n matrix of int (s/cq matrix) - combined zones, ub1, ub2, st - stats}/
            #   aislab.dp_feng.cbng (combined binning)
            #   ub1 = ubng(x1, ...)     - single value classing / md = 100
            #   ub2 = ubng(x2, ...)     - single value classing / md = 100
            #   genopt(ub1, ub2, ...)   - doesn't depend on data
            #   risk_zones() -> best cbng()
            # !!! FOR AISLAB ONLY !!!
    cz_bst = nans(CQ[0].shape)
    # cq_bst = CQ[0].astype(int)
    k = 0
    for i in range(m):
        for j in range(n):
            if k <= len(cb['sb']['map']) - 1:
                cz_bst[i, j] = cb['sb']['map'][cq_bst[i, j].astype(int)-1, 1]
            k += 1
    cz_bst = cz_bst.astype(int)
    sb_bst1 = sb_bst['st'][0]['my']
    for i in range(m):
        for j in range(n):
            if w1[i, j] == w_nan and np.all(np.isnan(crt0[cz_bst == cz_bst[i, j]])):
                cz_bst[cz_bst > cz_bst[i, j]] = cz_bst[cz_bst > cz_bst[i, j]] - 1
                sb_bst1 = np.vstack((sb_bst1[:cz_bst[i, j]-1], sb_bst1[cz_bst[i, j]:]))
    cb['zns'] = cz_bst
    cb['qds'] = cq_bst
    cb['crt_zns'] = sb_bst1
            
    return cb

###################################################################################
def stcbng(x, args):
    from aislab.dp_feng.binenc import cut

    data = args['data']  # data set
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. second (GBR) scorecard

    lb1 = args['lb1']  # lower bound for cut-offs of the first scorecard
    lb2 = args['lb2']  # lower bound for cut-offs of the second scorecard
    ub1 = args['ub1']  # upper bound for cut-offs of the first scorecard
    ub2 = args['ub2']  # upper bound for cut-offs of the second scorecard
    minx = np.min([args['minx'], np.min(x)])  # upper bound for cut-offs of the first scorecard
    maxx = np.max([args['maxx'], np.max(x)])  # upper bound for cut-offs of the second scorecard

    x1, ss = sort(c_(x[:nc1]))
    x2, ss = sort(c_(x[nc1:]))
    minx = np.min([minx, np.min(x)])  # upper bound for cut-offs of the first scorecard
    maxx = np.max([maxx, np.max(x)])  # upper bound for cut-offs of the second scorecard
    x1 = (x1 - minx)/(maxx - minx)*(ub1 - lb1) + lb1
    x2 = (x2 - minx)/(maxx - minx)*(ub2 - lb2) + lb2
    x1 = np.round(x1.flatten())
    x2 = np.round(x2.flatten())

    x1_zones = cut(data[:, 0], x1).flatten()
    x2_zones = cut(data[:, 1], x2).flatten()

    G = confm(-x1_zones, -x2_zones, w=data[:, -3], ux1=range(-nc1, 1), ux2=range(-nc2, 1)).astype(int)
    B = confm(-x1_zones, -x2_zones, w=data[:, -2], ux1=range(-nc1, 1), ux2=range(-nc2, 1)).astype(int)
    R = confm(-x1_zones, -x2_zones, w=data[:, -1], ux1=range(-nc1, 1), ux2=range(-nc2, 1)).astype(int)

    BR = B/(G + B)*100
    TGB = G + B
    TGBR = TGB + R
    return G, B, R, TGB, TGBR, BR

###################################################################################
def permqz(CQ, max_comb, dsp=False):
    s = np.max(CQ[0][1 - np.isnan(CQ[0]) == 1]) + 1
    if s > CQ[0].shape[0]*CQ[0].shape[1]: return CQ
    if dsp: print('s: ', s, ',   len(CQ):', len(CQ))
    CQ1 = []
    for k in range(len(CQ)):
        CQk = CQ[k]
        e = eligible_qz(CQk)
        ii, jj = find(e)
        for h in range(len(ii)):
            i1 = ii[h]
            j1 = jj[h]
            cq = new(CQk)
            cq[i1,j1] = s
            CQ1.append(cq)
    if len(CQ1) < max_comb: CQ1 = permqz(CQ1, max_comb, dsp)
    return CQ1
###################################################################################

def eligible_qz(cq):
    m, n = cq.shape
    e = np.full((m, n), False)
    for i in range(m):
        for j in range(n):
            if (i == 0 or not np.any(np.isnan(cq[:i, j]))) and (j == 0 or not np.any(np.isnan(cq[i, :j]))) and np.isnan(cq[i, j]): e[i, j] = True
            else: continue
    return e

###################################################################################
