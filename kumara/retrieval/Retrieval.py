"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''

'''___Third-Party Modules___'''
#import Libradtran
import os
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
'''___NPL Modules___'''


'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "11/11/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"

class Retrieval(ABC): 
    @abstractmethod
    def read_output(self,filename):
        pass

    @abstractmethod
    def run_retrieval(self,filename,albedo_file,aerosol,**kwargs):
        pass

    @abstractmethod
    def plot_spectrum(self,filename):
        pass   
