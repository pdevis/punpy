"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''

'''___Third-Party Modules___'''
import numpy as np
from netCDF4 import Dataset
from scipy import stats
import xarray as xr
import os
import emcee

'''___NPL Modules___'''


'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "11/11/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"


def findchimarg_all(theta):
    Ptots=np.zeros(len(dat_all[0]))
    for SFH_i in range(6):
        Models_i=np.empty((len(Minigrid),6,len(Tendgrid)))
        for ig in range(len(Minigrid)): # run models for the 6 initial masses, and interpolate between them to get the other initial masses
            Models_i[ig]=currentModel(Minigrid[ig],SFHgrid[SFH_i],theta)
        intf=interp1d(Minigrid,Models_i,axis=0)
        for Mini_i in range(len(Minigrid_int)):
            mod=intf(Minigrid_int[Mini_i])
            for t in range(len(mod[0])):
                for it in range(len(dat_all[0])):
                    dat_s= [dat_all[di][it] for di in range(len(dat_all))]
                    err_s= [err_all[di][it] for di in range(len(err_all))]
                    chisum=0
                    for i in range(len(err_s)):
                        ob2=mod[i][t]
                        if dat_s[i]>-98:
                            chi=(ob2-dat_s[i])**2/err_s[i]**2
                        if np.isfinite(chi):
                            chisum+=chi
                    Ptots[it]+=np.exp(-0.5*chisum)
    return -2*np.log(Ptots)

def lnlike(theta):
    return -0.5*(np.sum(findchimarg_all(theta)))

def lnprior(theta):
    if np.log10(min(SNgrid)) <= theta[0] <= np.log10(max(SNgrid)) and min(destroygrid) <=theta[1] <= max(destroygrid) and np.log10(min(fragmentgrid)) <=theta[2] <= np.log10(max(fragmentgrid)) and np.log10(min(ggcloudgrid)) <=theta[3] <= np.log10(max(ggcloudgrid)) and min(ggdiffusegrid) <=theta[4] <= 10. and min(favailablegrid) <=theta[5] <= max(favailablegrid):
        return 0.0
    return -np.inf

def lnprob(theta):
    lp = lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    print(theta,lp+lnlike(theta))
    return lp + lnlike(theta)

def retrieval():
    ndimw, nwalkers = 6, 100
    pos = [np.array([np.random.uniform(np.log10(min(SNgrid)),np.log10(max(SNgrid)),1)[0],np.random.uniform(min(destroygrid),max(destroygrid),1)[0],(np.random.uniform(np.log10(min(fragmentgrid)),np.log10(max(fragmentgrid)),1)[0]),(np.random.uniform(np.log10(min(ggcloudgrid)),np.log10(max(ggcloudgrid)),1)[0]),np.random.uniform(min(ggdiffusegrid),10,1)[0],np.random.uniform(min(favailablegrid),max(favailablegrid),1)[0]]) for i in range(nwalkers)]

#with terminating(Pool(processes=30)) as pool:
    sampler = emcee.EnsembleSampler(nwalkers, ndimw, lnprob, pool=pool)
    sampler.run_mcmc(pos, 200, progress=True)

samples = sampler.chain[:, :, :].reshape((-1, ndimw))
