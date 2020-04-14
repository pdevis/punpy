"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''

'''___Third-Party Modules___'''
import numpy as np
from netCDF4 import Dataset
from scipy import stats
import xarray as xr
import os

'''___NPL Modules___'''

'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "30/03/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"
