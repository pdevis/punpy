"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''
from kumara.forwardModel.ForwardModelFactory import ForwardModelFactory
from kumara.sensors.SensorFactory import SensorFactory

'''___Third-Party Modules___'''
import numpy as np
import emcee
import threading
from multiprocessing import Pool
import time
'''___NPL Modules___'''


'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "01/03/2020"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"


# lock = threading.Lock()
class MCMCRetrieval:
    def __init__(self,sensor,wavs,observed,uncertainty,reflpath,forwardmodel='libradtran',path='MCMC'):
        self.observed=observed
        self.uncertainty=uncertainty
        self.FM=ForwardModelFactory.create_model(forwardmodel,path)
        self.sensor=SensorFactory.create_sensor(sensor,wavs)
        self.reflpath=reflpath

    def run_retrieval(self,theta_0,nwalkers,steps):
        
        ndimw = len(theta_0)
        pos = [theta_0*np.random.normal(1.0,0.1,len(theta_0)) for i in range(nwalkers)]

        with Pool(processes=20) as pool:
            sampler = emcee.EnsembleSampler(nwalkers, ndimw, self.lnprob, pool=pool)
            sampler.run_mcmc(pos, steps, progress=True)
        # sampler = emcee.EnsembleSampler(nwalkers, ndimw, self.lnprob)
        # sampler.run_mcmc(pos, steps, progress=True)

        return sampler.chain[:, :, :].reshape((-1, ndimw))

    def find_chisum(self,theta):
        # lock.acquire()
        filenameMCMC="MCMC_%s"%time.time()
        # lock.release()

        self.FM.run_model(filenameMCMC,self.reflpath,theta[0],theta[1])
        rad_RT=self.FM.get_TOA(filenameMCMC)
        wavs_RT=self.FM.get_wavs(filenameMCMC)
        model=self.sensor.convolve(wavs_RT,rad_RT)
        return np.sum((model-self.observed)**2/self.uncertainty**2)

    def lnlike(self,theta):
        return -0.5*(self.find_chisum(theta))

    def lnprior(self,theta):
        if True:
            return 0.0
        return -np.inf

    def lnprob(self,theta):
        lp = self.lnprior(theta)
        if not np.isfinite(lp):
            return -np.inf
        return lp + self.lnlike(theta)
