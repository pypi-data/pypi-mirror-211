#!/usr/bin/env python
# coding: utf-8

"""
WhiteBox instances
of different Gaussian 2D problems
"""

import numpy as np
from .. import g_models as gm
from .. import f_models
from .. import samplebox #č pro proxy_prod # pro parabolu
from ..whitebox import WhiteBox, Gaussian_Z_prod_2D
from ..whitebox import Gaussian_ProdFourBetas_2D
from ..whitebox import Gaussian_Z_sumexp_2D
from ..whitebox import Gaussian_Z_max
from ..whitebox import Gaussian_Hyperbola_2D

__all__ = []

#č zde ten __all__ těžko dohlídáme
#č budeme přidávat do seznamu postupně
def add(str): __all__.append(str)

f = f_models.SNorm(2)


""" FourBranch2D
g1 = k1 + 0.1*(x1 - x2)**2 - (x1 + x2)/np.sqrt(2)
g2 = k1 + 0.1*(x1 - x2)**2 + (x1 + x2)/np.sqrt(2)
g3 = (x1 - x2) + k2/np.sqrt(2)
g4 = (x2 - x1) + k2/np.sqrt(2) #č byl tu překlep v jednom članku
g = np.min((g1, g2, g3, g4), axis=0)"""
#whitebox.WhiteBox(f, gm.FourBranch2D(k1=3, k2=7))
#
# Four branch system
add('four_branch')
def four_branch():
    wt = WhiteBox(f, gm.FourBranch2D(k1=3, k2=7))
    wt.pf_exact = 2.221e-03
    wt.pf_exact_method = 'known $p_f$ value' #"some guys said me that" 
    wt.description = "Four branch system. Structural Safety 62 (2016) 66-75"
    return wt


add('four_branch_2')
def four_branch_2():
    wt = WhiteBox(f, gm.FourBranch2D(k1=5.5, k2=11))
    # TODO calculate
    #wt.pf_exact = 0.257
    #wt.pf_exact_method = 'known value' #"some guys said me that" it's 0.256
    wt.description = "Four branch system from another paper"
    return wt





# Breitung
# Piecewise linear function
add('piecewise_linear')
def piecewise_linear():
    wt = WhiteBox(f, gm.piecewise_2D_linear)
    wt.description = "Breitung. Piecewise linear function"
    return wt


""" Logistic2D
# sebemenší parametrizace
y1 = self._c1 - x1
y2 = self._c2 + x2
y3 = 1.0/(1+np.exp(-2.0*y2)) - 0.5

if self.easy_version:
    g = np.minimum(y1,y2)  # easy version for SuS
else:
    g = np.minimum(y1,y3)  # difficult version for SuS"""
#whitebox.WhiteBox(f, gm.Logistic2D(c1=5, c2=4, easy_version=True))
# Logistic 2D function
add('min_linear')
def min_linear():
    wt = WhiteBox(f, gm.Logistic2D())
    wt.description = "Breitung. 2D linear (easy version for SuS)"
    return wt

add('min_logistic')
def min_logistic():
    wt = WhiteBox(f, gm.Logistic2D(easy_version=False))
    wt.description = "Breitung. Logistic 2D function (hard version for SuS)"
    return wt



# soucin velicin plus nějaká konstanta 
# g= X1 * X2 * X3 * X4 + c
add('prod_1')
add('prod_03')
add('prod_5')
def prod_1():
    return Gaussian_Z_prod_2D(const=1)
def prod_03():
    return Gaussian_Z_prod_2D(const=-0.3, sign=1)
def prod_5():
    return Gaussian_Z_prod_2D(const=-5, sign=-1)

add('hyperbola_2')
def hyperbola_2():
    return Gaussian_Hyperbola_2D(const=2)





"""
c = 0.5 # wave amplitude in Gaussian space
d = 3.0 # average of sine fiunction in Gaussian space
k = 6   # number of sine waves (design points)
"""
add('sinball')
def sinball():
    return WhiteBox(f, gm.S_ballSin2D(c=1, d=5, k=6))


# Fajvka
# člověk se tu bez půllitry nevýzná
# viz. conic_section_boundaries_test.py pro inspiraciju
add('five')
def five():
    return WhiteBox(f, gm.ConicSection(l=.1, e=1.1, teta=-np.pi/4, c=(-1.8,1), sign=1))


# just circle, moved
#č v kódu máme něco takovýho:
# r = np.sqrt(np.square(x) + np.square(y))
# r_bound = abs(self._l / (1 - self._e * np.cos(phi-self._teta)))
# g = self._sign * (r - r_bound)
#č už si napamatuji, odkuď to bylo převzato (buď Rektorys, nebo wiki)
#č máme smulu.
add('circle')
def circle():
    return WhiteBox(f, gm.ConicSection(l=1.4, e=0, teta=0, c=(1.3, 0.6), sign=1))




add('parabola')
def parabola():
    return WhiteBox(f, gm.parabola)


# Sin2D
# g = self._kx * x + self._ky * y + np.sin(self._kxsin*x) + self._const
#add('sin')
#def sin():
#    return whitebox.WhiteBox(f, gm.Sin2D(kx=-1/4., ky=-1, kxsin=5, const=5))
add('sin_shields')
def sin_shields():
    wt = WhiteBox(f, gm.Sin2D(kx=-1/4., ky=-1, kxsin=5, const=4))
    wt.pf_exact = 4.1540e-4
    wt.pf_exact_method = "some guys said me that it is result of Monte Carlo"
    return wt


# Prod_FourBetas
# g = beta^2/2 - |x1 * x2|
#č Breitung má
# g = 15 - |x1 * x2|
# beta^2/2 == 15
# beta == sqrt(30)
add('prod_four_betas')
def prod_four_betas():
    return Gaussian_ProdFourBetas_2D(beta=np.sqrt(30))



""" BlackSwan2D
a = 2.0 # boundary for x1
b = 5.0 # boundary for x2
y = np.where(sim[:,0] <= a, sim[:,0], sim[:,1])
# pro x1 <= a   y = x1
# pro x1 >  a   y = x2
g = b - y # failure for b<y"""
#whitebox.WhiteBox(f, gm.BlackSwan2D(a=2.0, b=5.0))
add('black_swan')
def black_swan():
    a=2; b=5
    wt = WhiteBox(f, gm.BlackSwan2D(a=a, b=b))
    wt.pf_exact = f.marginals[0].sf(a) * f.marginals[1].sf(b)
    wt.pf_exact_method = 'exact solution' #"some guys said me that" 
    wt.description = "Black swan. Au/Wang (cited by Breitung)"
    return wt
    


""" Metaballs2D
# sebemenší parametrizace
y1 = 4/9*(x1 + 2  )**2 + 1/25 * (x2    )**2 
y2 = 1/4*(x1 - 2.5)**2 + 1/25 * (x2-0.5)**2 
g = 30.0/( y1**2 + 1.0 ) + 20.0/( y2**2 + 1.0 ) - self._const"""
#whitebox.WhiteBox(f, gm.Metaballs2D(const=5))
#ё проклял уж всех богов с этой "себеменьшей параметризацией", блин
#č u Breitung'a doopravdy vidím const=5
add('metaball')
def metaball():
    wt = WhiteBox(f, gm.Metaballs2D(const=5))
    wt.pf_exact = 1.13e-5
    wt.pf_exact_method = "after 1000 evaluations"
    wt.description = "Metaball. Breitung"
    return wt



""" CosExp2D
# sebemenší parametrizace
s = self._s
# g = cos((np.exp(-xm-s  ))*xm)   * np.exp(-(x +s  )/3)
g = np.cos( ( np.exp(-sample[:,0] - s ) )*sample[:,0])   * np.exp( -(sample[:,0] + s  )/3 )  """
#whitebox.WhiteBox(f, gm.CosExp2D(s=5))
add('cos_exp')
def cos_exp():
    return WhiteBox(f, gm.CosExp2D(s=5))


# g = np.sum(np.exp(-(sample**2)), axis=1) + self._const
add('sumexp')
def sumexp():
    return Gaussian_Z_sumexp_2D(-0.003)

add('modified_rastrigin')
def modified_rastrigin():
    wt = WhiteBox(f, gm.modified_rastrigin)
    wt.description = "Modified Rastrigin"
    wt.pf_exact = 7.34e-02
    wt.pf_exact_method = 'known value'
    return wt

add('quartic')
def quartic():
    wt = WhiteBox(f, gm.quartic)
    return wt


add('max')
def max():
    return Gaussian_Z_max(2, const=4)
