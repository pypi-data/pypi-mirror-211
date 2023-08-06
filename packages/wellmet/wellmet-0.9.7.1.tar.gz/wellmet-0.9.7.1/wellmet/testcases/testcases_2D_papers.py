#!/usr/bin/env python
# coding: utf-8

"""
WhiteBox instances
of different non-Gaussian 2D problems
"""

import numpy as np
from .. import g_models as gm
from .. import f_models
from ..whitebox import WhiteBox
import scipy.stats as stats
from scipy import integrate # for Pareto tail

__all__ = [
            'uniform_branin_2D',
            'piecewise_pareto_tail',
            'natafm_plane_2D',
            ]


# Uniform-uniform
# from scipy: "In the standard form, the distribution is uniform on [0, 1]."
u = f_models.UnCorD((stats.uniform, stats.uniform))

gewm = f_models.Nataf((stats.gumbel_r, stats.weibull_min(c=1.5)), [[1,-0.8], [-0.8,1]])


"""
I would like to use function definitions to clearly isolate ones testcases
"""

# Rescaled Branin function
def uniform_branin_2D():
    wt = WhiteBox(u, gm.branin_2D)
    wt.pf_exact = 0.257
    wt.pf_exact_method = 'known value' #"some guys said me that" it's 0.256
    wt.description = "Rescaled Branin function"
    return wt



# Pareto tail
class PiecewiseParetoDist:
    def __init__(self, a=3.5):
        self.ax = a
        self.au = stats.norm.cdf(a) 
        self.c = np.log(stats.norm.cdf(-a))/np.log(a)
        self.pareto = stats.pareto(b=-self.c)
        # без излишевст
        self._p = integrate.quad(lambda x: self.pdf(x), -np.inf, np.inf)[0]
        self._mean = integrate.quad(lambda x: x*self.pdf(x), -np.inf, np.inf)[0]
        self._var = integrate.quad(lambda x: x**2*self.pdf(x), -np.inf, np.inf)[0]
        
    def cdf(self, x):
        return np.where(x < self.ax, stats.norm.cdf(x), self.pareto.cdf(x))
    def pdf(self, x):
        return np.where(x < self.ax, stats.norm.pdf(x), self.pareto.pdf(x))
    def ppf(self, u):
        return np.where(u < self.au, stats.norm.ppf(u), self.pareto.ppf(u))
        
    def mean(self): return self._mean
    def var(self): return self._var
    def std(self): return np.sqrt(self._var)
    


def piecewise_pareto_tail():
    h = f_models.UnCorD((stats.norm, PiecewiseParetoDist()))
    wt = WhiteBox(h, gm.non_chi_squares)
    wt.pf_exact = 1.87e-06
    wt.pf_exact_method = 'FORM-type thought-three beta points'
    wt.description = "Breitung. Pareto tail"
    return wt



def natafm_plane_2D():
    wt = WhiteBox(gewm, gm.Linear_nD((-1, -2, 7)))
    wt.pf_exact = 0.00114
    wt.Nsim = int(10e8)
    wt.pf_exact_method = 'MC'
    return wt
    
    



