""" Utility functions and classes for SRP

Context : SRP
Module  : Stats.py
Version : 1.0.1
Author  : Stefano Covino
Date    : 29/04/2022
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : BIC (loglikelihood,npars,ndata)
            This function reports the BIC knowking the best-fit Log Likelihoood,
            the number of data-points and the number of fit parameters.

Remarks :

History : (17/01/2022) First version.
        : (29/04/2022) Minor bug corrected.

"""


import numpy as np


def BIC(LLike,npars,ndata):
    return -2*LLike+npars*np.log(ndata)


    
    