"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''
from kumara.forwardModel.ForwardModel import ForwardModel
from kumara.forwardModel.UVspec import UVspec

'''___Third-Party Modules___'''
import os
import numpy as np
import matplotlib.pyplot as plt

'''___NPL Modules___'''


'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "11/11/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"




libradtranpath = "/opt/libRadtran-2.0.2/"
INPUTDIR = '/home/pdv/libradtran/examples'
OUTPUTDIR = '/home/pdv/libradtran/examples'
PLOTDIR = '/home/pdv/libradtran/plots'

class LibradtranModel(ForwardModel):
    def __init__(self,path='./libradtran/'):
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

        # Initialise class attributes
        if not os.path.exists(path):
            os.makedirs(path)

        self.path=path
        self.lambd = None 
        self.TOAradiance = None
        self.RTcode = 'libradtran'

        self.edir = None  # Parse attributes dictionary
        self.edn = None  # Parse attributes dictionary
        self.eup = None  # Parse attributes dictionary
        self.uavg = None  # Parse attributes dictionary
        self.uu = None  # Parse attributes dictionary
        self.eglo = None  # Parse attributes dictionary

    def read_output(self,filename):
        self.lambd, self.edir, self.edn, self.eup, self.uavg, self.uu, self.eglo = np.genfromtxt('%s/%s.OUT'%(self.path,filename),unpack=True,usecols=[0,1,2,3,4,5,6])


    def run_model(self,filename,albedo_file,aerosol,H2O,sza=30,saa=180,vza=0,vaa=0,altitude=470,latitude=-23.501,longitude=15.095,O3=-99,CH4=-99,CO2=-99,atmosphere="midlatitude_summer",rte_solver='disort'):
        # some sensible alternative numbers for the variables:
        #H2Os = ["0","15","30"]
        #O3s = ["200","300","500"]
        #CH4s = [20e+18,30e+18,40e+18]
        #CO2s = [5e+21,7.5e+21,10e+21]
        #atmospheres = ["afglus","tropics","midlatitude_summer","midlatitude_winter","subarctic_summer","subarctic_winter","US-standard"]
        #solvers=['twostr','disort','MYSTIC']

        inputFilename = filename+'.INP'
        outputFilename = filename+'.OUT'
        inp = os.path.join(self.path,inputFilename)
        out = os.path.join(self.path,outputFilename)
        verbose=False

        uvspec = UVspec()
        uvspec.inp["data_files_path"] = libradtranpath+'data'

        if not verbose:
            uvspec.inp["quiet"]=""
        uvspec.inp["atmosphere_file"] = atmosphere
        uvspec.inp["source"] = 'solar '+libradtranpath+'/data/solar_flux/kurudz_0.1nm.dat'
        uvspec.inp["albedo_file"] = albedo_file
        #uvspec.inp["albedo"] = albedo_file
        uvspec.inp["pseudospherical"] = ""

        uvspec.inp["sza"] = str(sza)
        uvspec.inp["umu"] = str(np.cos(np.deg2rad(vza)))
        uvspec.inp["phi"] = str(vaa)
        uvspec.inp["phi0"] = str(180-saa)
        uvspec.inp["altitude"] = str(altitude/1000)
        if latitude>0:
            uvspec.inp["latitude"] = "N "+str(latitude)
        else:    
            uvspec.inp["latitude"] = "S "+str(-latitude)
        if longitude>0:
            uvspec.inp["longitude"] = "E "+str(longitude)
        else:    
            uvspec.inp["longitude"] = "W "+str(-longitude)
        
        uvspec.inp["zout"] = "TOA"

        uvspec.inp["rte_solver"] = rte_solver
        uvspec.inp["mol_abs_param"] = 'reptran fine'
        if O3>0:
            uvspec.inp["mol_modify O3"] = str(O3)+" DU"
        if H2O>0:
            uvspec.inp["mol_modify H2O"] = str(H2O)+" MM"
        if CH4>0:
            uvspec.inp["mol_modify CH4"] = str(CH4)+" cm_2"
        if CO2>0:
            uvspec.inp["mol_modify CO2"] = str(CO2)+" cm_2"

        #deltam off               # disable delta-scaling

        #uvspec.inp["number_of_streams"] = "24"      # number of streams used in DISORT

        uvspec.inp["wavelength"] = "351.0 2480.0"  # Wavelength range [nm]

        uvspec.inp["aerosol_default"] = ""  # the simplest way to include aerosol :-)
        uvspec.inp["aerosol_visibility"] = aerosol  
        uvspec.inp["output_user"] = "lambda edir edn eup uavg uu eglo"

        uvspec.inp["output_quantity"] = 'reflectivity' #'transmittance' #

        uvspec.write_input(inp)
        uvspec.run(inp,out,verbose,path=libradtranpath)
        return None

    def get_TOA(self,filename):
        rad = np.genfromtxt('%s/%s.OUT'%(self.path,filename),unpack=True,usecols=[5]) #in mW / (m2 nm) 
        return rad 

    def get_wavs(self,filename):
        wavs = np.genfromtxt('%s/%s.OUT'%(self.path,filename),unpack=True,usecols=[0])
        return wavs     

    def plot_spectrum(self,filename):
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.plot(self.lambd,self.edir)
        ax.plot(self.lambd,self.edn)
        ax.plot(self.lambd,self.eup)
        ax.plot(self.lambd,self.uavg)
        ax.plot(self.lambd,self.uu)
        ax.plot(self.lambd,self.eglo)
        ax.set_xlabel(r"$\lambda$ (nm)")
        ax.set_ylabel(r"Brightness")
        ax.set_ylim([0,1])
        fig.savefig('%s/%s.png'%(self.path,filename))
        del fig
        return None
