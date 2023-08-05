import numpy as np
import pandas as pd
from aislab.gnrl.bf import *
from aislab.gnrl.sf import *
from aislab.gnrl.measr import *
#from aislab.gnrl.measr import confm
from aislab.dp_feng.binenc import cut


# exp1:                                                 # y = a + b*e^x
# exp2:                                                 # y = a + b*e^(x + c)
# exp3:   ym = pm[0] + pm[1]*np.exp(x*pm[2])            # y = a + b*e^(x*c)
# log:    ym = pm[0] + pm[1]*np.log(abs(x) + 1)         # ym = a + b*ln(x)
# log1:   ym = pm[0] + pm[1]*np.log(pm[2]*abs(x) + 1)   # y = a + b*ln(c*|x| + 1)
# logW:   ym = pm[0] + pm[1]*np.log(abs(pm[2]*x + 1))   # y = a + b*ln(|c*x + 1|)
# lgr:    ym = 1/(1 + np.exp(-x@pm))                    # y = 1/(1 + e^-(x*pm))
# exp model
# args['b'] = 1e-8
# args['c'] = 1e3
# log model
# args['b'] = 0.01
# args['c'] = 1e3


###################################################################################
def f_cbng(X, args): # F objective
    # Objective function for cross binning with binary dependent
    # X - population (xi = X[i, :] - i-th individual
    # args - all remaining arguments of F
    # F - objective function

    Cd0 = args['Cd0']       # desired lower my (in cell c[0, 0])
    Cdn = args['Cdn']       # desired upper my (in cell c[-1, -1])
    nwd0 = args['nwd0']     # desired weighted number of observations in c[0, 0]
    nwdn = args['nwdn']     # desired weighted number of observations in c[-1, -1]
    miny0 = args['miny0']   # minimum acceptable number of observations with y=0 in each cell c[i, j]
    miny01 = args['miny01'] # minimum number of observations with y={0, 1} in each cell c[i, j]
    mindC = args['mindC']   # minimum change in the criterion moving from one to a neighbour cell
    wi = args['wi']         # weights of components of F objective
    nc1 = args['nc1']       # number of cut-offs w.r.t. row variable
    nc2 = args['nc2']       # number of cut-offs w.r.t. col variable
    lb1 = args['lb1']       # lower bound for row cut-offs
    lb2 = args['lb2']       # lower bound for col cut-offs
    ub1 = args['ub1']       # upper bound for row cut-offs
    ub2 = args['ub2']       # upper bound for col cut-offs
    minx0 = args['minx']
    maxx0 = args['maxx']

    data = args['data'] # todo: svc

    if X.ndim == 1: X = np.array([X])
    N = len(X)
    F = nans((N,))
    i = 0
    for x in X:
        x1, ss = sort(c_(x[:nc1, ]))
        x2, ss = sort(c_(x[nc1:, ]))
        minx = np.min([minx0, np.min(x)])  # upper bound for row cut-offs
        maxx = np.max([maxx0, np.max(x)])  # upper bound for col cut-offs
        x1 = (x1 - minx)/(maxx - minx)*(ub1 - lb1) + lb1
        x2 = (x2 - minx)/(maxx - minx)*(ub2 - lb2) + lb2
        x1 = np.round(x1.flatten())
        x2 = np.round(x2.flatten())

        if len(set(x1)) != len(x1) or len(set(x2)) != len(x2):
            F[i] = np.inf
            i += 1
            continue # skip individual with 2 or more edqual cut-offs per variable => F = inf
        try:
            x1_zones = cut(data[:, 0], x1).flatten()
            x2_zones = cut(data[:, 1], x2).flatten()
        except:
            raise Exception('In f_cbng(): Wrong cut-offs in ' + str(i) + '-th individual.')
        Y1 = confm(-x1_zones, -x2_zones, w=data[:, 2]).astype(int)  # confusion matrix
        Y0 = confm(-x1_zones, -x2_zones, w=data[:, 3]).astype(int)  # confusion matrix
        Yna = confm(-x1_zones, -x2_zones, w=data[:, 4]).astype(int)  # confusion matrix
        import warnings
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        Crit = Y0/(Y1 + Y0)*100
        T01 = Y1 + Y0
        Tot = Y1 + Y0 + Yna
        
        
        
        
        drC = Crit[:, 1:] - Crit[:, :-1]  # rowwise delta Crit
        dcC = Crit[1:, :] - Crit[:-1, :]  # colwise delta Crit

        mr, nr = np.shape(drC)
        mc, nc = np.shape(dcC)
        drC = new(drC)
        for k in range(nr-1, 0, -1):
            for j in range(mr-1, 0, -1):
                if k-1 >= 0 and not np.isnan(drC[j, k]) and np.isnan(drC[j, k-1]): drC[j, k-1] = drC[j, k]
                if j-1 >= 0 and not np.isnan(drC[j, k]) and np.isnan(drC[j-1, k]): drC[j-1, k] = drC[j, k]
        dcC = new(dcC)
        for k in range(nc-1, 0, -1):
            for j in range(mc-1, 0, -1):
                if k-1 >= 0 and not np.isnan(dcC[j, k]) and np.isnan(dcC[j, k-1]): dcC[j, k-1] = dcC[j, k]
                if j-1 >= 0 and not np.isnan(dcC[j, k]) and np.isnan(dcC[j-1, k]): dcC[j-1, k] = dcC[j, k]
        negdrC = drC[drC < mindC]  # negative trend or not enough change in rowwise delta Crit
        negdcC = dcC[dcC < mindC]  # negative trend or not enough change in colwise delta Crit

        Fi = nans((7, 1))
        # discriminatory power of the strategy  #  min(F1) = 0
        Fi[0, 0] = (((Cd0 - Crit[0, 0])/max(1e-6, 100 - Cd0))**2 + ((nwd0 - Tot[0, 0])/max(1e-6, nwd0))**2)/2
        Fi[1, 0] = (((Cdn - Crit[-1, -1])/max(1e-6, Cdn - 0))**2 + ((nwdn - Tot[-1, -1])/max(1e-6, nwdn))**2)/2
        # monotonicity of Crit  #  min(F2) = 0
        Fi[2, 0] = ((np.sum(mindC - negdrC) + np.sum(mindC - negdcC))/(nc1*nc2))**2
        # mininmum number of Bad and Good & Bad applications per segment  #  min(F4) = min(F5) = 0
        Fi[3, 0] = (np.sum((miny0 - Y0)*(miny0 - Y0 > 0)*(T01 > 0))/max(1e-6, (nc1 + 1)*(nc2 + 1)*miny0))**2
        Fi[4, 0] = (np.sum((miny01 - T01)*(miny01 - T01 > 0)*(T01 > 0))/max(1e-6, (nc1 + 1)*(nc2 + 1)*miny01))**2
        # minimum number of NaN cells: min(F6) = 0
        Fi[5, 0] = (np.sum(np.sum(np.isnan(Crit)))/((nc1 + 1)*(nc2 + 1)))**2
        # minimum number of records in most populated cell  # min(F7) = 0
        Fi[6, 0] = np.max(np.max(Tot))/max(1e-6, sum(sum(Tot)))
        F[i] = r_(wi)@Fi

        if np.isnan(F[i]):
            F[i] = np.inf
            if i == len(F):
                return F
        i += 1

    return F
###################################################################################
def f_exp1(args):
    # F for model: y = a + b*e^x
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp1_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_exp2(args):
    # F for model: y = a + b*e^(x + c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp2_apl(x, pm)
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = args['b']
    c = args['c']
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_exp3(args):
   # F for model: y = a + b*e^(x*c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp3_apl(x, pm)
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    # print(np.hstack((e, w)))

    b = args['b']
    c = args['c']
    d1 = pm.flatten()
    d2 = (1 - (pm[0, 0] + pm[1, 0]))**2*c
    A = np.diag((d1 < b))*c
    F = F + pm.T@A@pm + d2

    return F, args
###################################################################################
def f_lgr(args):
    # F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    ym = lgr_apl(x, pm)
    ym[ym > 1 - 1e-10] = 1 - 1e-10
    ym[ym < 1e-10] = 1e-10
    m = pm.shape[1]
    yy = np.matlib.repmat(y, 1, m)
    ww = np.matlib.repmat(w, 1, m)
    F = -sum(yy*np.log(ym)*ww + (1 - yy)*np.log(1 - ym)*ww)
    args['data'][:, -1] = ym.flatten()
    return F, args
###################################################################################
def f_log1(args):
    # F for exponential model: ym = a + b*ln(x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log1_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_log2(args):
    # F for exponential model: ym = a + b*ln(x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log2_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_log3(args):
    # F for exponential model: ym = a + b*ln(c*x + 1)
    pm = args['x']
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log3_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = args['b']
    c = args['c']
    d1 = pm.flatten()
    d2 = (pm[0, 0] - 1)**2*c

    A = np.diag((d1 < b))*c
    F = F + pm.T@A@pm + d2

    return F, args
###################################################################################
def g_exp1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for model: y = a + b*e^x
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    e = y - ym
    g = np.zeros((2, 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.exp(x))[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_exp2(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F model: y = a + b*e^(x + c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    tmp = np.exp(x + pm[2])
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@tmp)[0]
    g[2] = (-2*pm[1]*(w*e).T@tmp)[0]

    b = args['b']
    c = args['c']
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_exp3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for model: y = a + b*e^(x*c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    tmp = np.exp(x*pm[2])
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@tmp)[0]
    g[2] = (-2*pm[1]*(w*e*x).T@tmp)[0]

    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    g = g + 2*A@pm + np.array([[-2*(1 - (pm[0,0] + pm[1,0]))*c], [-2*(1 - (pm[0,0] + pm[1,0]))*c], [0]])
    return g
###################################################################################
def g_lgr(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    g = -x.T@((y - ym)*w)
    return g
###################################################################################
def g_log1(args=None):
    # gradient of F for log model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    e = y - ym
    g = np.zeros((2, 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.log(abs(x) + 1))[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_log3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.log(abs(pm[2]*x) + 1))[0]
    g[2] = ((-2*pm[1]*(w*e/(abs(pm[2]*x) + 1)).T@x)*np.sign(pm[2]*x + 1))[0]  # !!!: np.sign(0) = 0

    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    d2 = (pm[0, 0] - 1)**2*c
    g = g + 2*A@pm + np.array([[2*(pm[0,0] - 1)*c], [0], [0]])
    return g
###################################################################################
def h_exp1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for model: y = a + b*e^x
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    H = np.zeros(shape = (2,2))
    tmp = np.exp(x)
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    H = H + 2*A

    return H
###################################################################################
def h_exp2(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for model: y = a + b*e^(x + c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.exp(x + pm[2])
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = 2*pm[1]*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = 2*pm[1]*((w*tmp).T@tmp)[0] - 2*((w*e).T@tmp)[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w*tmp).T@tmp)[0] - 2*pm[1]*((w*e).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    H = H + 2*A
    return H
    dd = pm.flatten()
    A = np.diag((dd < b))*c
###################################################################################
def h_exp3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for model: y = a + b*e^(x*c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.exp(x*pm[2])
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = 2*pm[1]*((w*x).T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = 2*pm[1]*((w*tmp*x).T@tmp)[0] - 2*((w*e*x).T@tmp)[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w*tmp*x**2).T@tmp)[0] - 2*pm[1]*((w*e*x**2).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    H = H + 2*A + np.array([[2*c, 2*c, 0], [2*c, 2*c, 0], [0, 0, 0]])
    return H
###################################################################################
def h_lgr(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    n = x.shape[1]
    H = (x*np.matlib.repmat(ym*(1 - ym)*w, 1, n)).T@x
    return H
###################################################################################
def h_log1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    H = np.zeros(shape = (2,2))
    tmp = np.log(abs(x) + 1)
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    H = H + 2*A
    return H
###################################################################################
def h_log3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.log(abs(pm[2]*x + 1))
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = (2*pm[1]*((w/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1))[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = (2*pm[1]*((w*tmp/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1) - 2*((w*e/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1))[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w/abs(pm[2]*x + 1)*x).T@x)[0] - 2*pm[1]*((w*e*x/abs(pm[2]*x + 1)).T@x)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    H = H + 2*A + np.array([[2*c, 0, 0], [0, 0, 0], [0, 0, 0]])
    return H
###################################################################################
def exp1_apl(x, pm):
    # model: y = a + b*e^x
    ym = pm[0] + pm[1]*np.exp(x)
    return ym
###################################################################################
def exp2_apl(x, pm):

    ym = pm[0] + pm[1]*np.exp(x + pm[2])
    return ym
###################################################################################
def exp3_apl(x, pm):
    # model: y = a + b*e^(x*c)
    ym = pm[0] + pm[1]*np.exp(x*pm[2])
    return ym
###################################################################################
def lgr_apl(x, pm):
    # logistic regression function
    if not isinstance(x, np.ndarray): x = np.array([[x]])
    if not isinstance(pm, np.ndarray): pm = np.array([[pm]])
    ym = 1/(1 + np.exp(-x@pm))
    return ym
###################################################################################
def log1_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(abs(x) + 1)
    return ym
###################################################################################
def log2_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(pm[2]*abs(x) + 1)
    return ym
###################################################################################
def log3_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(abs(pm[2]*x + 1))
    return ym
###################################################################################
