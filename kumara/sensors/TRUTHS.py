"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''
from kumara.sensors.Sensor import Sensor

'''___Third-Party Modules___'''
import os
import numpy as np
from scipy.interpolate import interp1d 
'''___NPL Modules___'''


'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "11/11/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"


class TRUTHS(Sensor):
    def __init__(self,wavs):
        """
        Initialise Sensor

        :type product_path: str
        :param product_path: The data product file path.

        :type detail: str
        :param detail: Can take values:

        * "min" (default) - only information available with filename parsed.
        * "max" - information available in metadata files also parsed, but with opening the product.

        :type kwargs: -
        :param kwargs: Parsing parameters
        """

        self.wavs=wavs
        self.radiances = None 
        self.uncertainties = None

    def convolve(self,wavs,radiances):
        func=interp1d(wavs,radiances)
        self.radiances=func(self.wavs)
        return self.radiances