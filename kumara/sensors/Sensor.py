"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''

'''___Third-Party Modules___'''
from abc import ABC, abstractmethod
'''___NPL Modules___'''


'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "11/11/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"

class Sensor(ABC): 
    def __init__(self, wavs):
        """
        Initialise Forward Model

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

    @abstractmethod
    def convolve(self,wavs,radiances):
        pass

    def get_radiances(self):
        return self.radiances

    def save_radiances(self,filename):
        savefile=open(filename,"w")
        savefile.write("#Wavelengths Radiances \n")
        for i in range(len(self.wavs)):
            savefile.write("%s   %s \n"%(self.wavs[i],self.radiances[i]))
        savefile.close()
