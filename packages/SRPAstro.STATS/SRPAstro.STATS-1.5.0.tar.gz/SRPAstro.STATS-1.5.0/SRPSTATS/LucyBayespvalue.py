""" Utility functions and classes for SRP

Context : SRP
Module  : Stats
Version : 1.0.0
Author  : Stefano Covino
Date    : 02/05/2022
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino
Remark  : This is the proxy to the so-called Posterior predictive p-value (Gelman, A.,
            Carlin, J. B., Stern, H. S., et al. 2013, Bayesian Data Analysis
            (Boca Raton, FL: CRC Press) introduced by Lucy (2018, A&A 614,
            25) and Lucy (2018,

Usage   : LucyBayespvalue(model, data, edata, npars)

Example:
        # Derive a set of models based on the posterior distribution
        S =  model([samples[:,[0]],samples[:,[1]]],dt['angle'])

History : (02/05/2022) First version.
"""

from SRPSTATS.chi2 import chi2
import scipy.stats as ss
import numpy as np


def LucyBayespvalue (model, data, edata, npars):
    #
    b = chi2(model,data,edata).mean() - npars
    return {"Lucy-Bayes-p-value": ss.chi2.sf(b,len(ndata)-npars)}
