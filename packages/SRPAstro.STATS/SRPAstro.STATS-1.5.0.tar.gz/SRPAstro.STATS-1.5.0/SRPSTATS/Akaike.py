""" Utility functions and classes for SRP

Context : SRP
Module  : Stats.py
Version : 1.0.0
Author  : Stefano Covino
Date    : 06/05/2022
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : Akaike (loglikelihood,npars)
            This function reports the Akaike information criterion knowking the best-fit Log Likelihoood,
            and the number of fit parameters.

Remarks :

History : (06/05/2022) First version.

"""




def Akaike(LLike,npars,ndata=0):
    if ndata < 1:
        return -2*LLike+2*npars
    else:
        return -2*LLike+2*npars+2*npars*(npars+1)/(ndata-npars-1)


    
    