"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''

'''___Third-Party Modules___'''
from libradtran import *
import UVspec
import os
import numpy as np
from netCDF4 import Dataset
from scipy import stats
import xarray as xr
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


def runLibradtran(filename,albedo_file,aerosol,sza=30,H2O=-99,O3=-99,CH4=-99,CO2=-99,atmosphere="midlatitude_summer",rte_solver='disort'):
    # some sensible alternative numbers for the variables:
    #H2Os = ["0","15","30"]
    #O3s = ["200","300","500"]
    #CH4s = [20e+18,30e+18,40e+18]
    #CO2s = [5e+21,7.5e+21,10e+21]
    #atmospheres = ["afglus","tropics","midlatitude_summer","midlatitude_winter","subarctic_summer","subarctic_winter","US-standard"]
    #solvers=['twostr','disort','MYSTIC']

    inputFilename = filename+'.INP'
    outputFilename = filename+'.OUT'
    inp = os.path.join(INPUTDIR,inputFilename)
    out = os.path.join(OUTPUTDIR,outputFilename)

    uvspec = UVspec.UVspec()
    uvspec.inp["data_files_path"] = libradtranpath+'data'

    uvspec.inp["atmosphere_file"] = atmosphere
    uvspec.inp["source"] = 'solar '+libradtranpath+'/data/solar_flux/kurudz_0.1nm.dat'
    uvspec.inp["albedo_file"] = albedo_file
    uvspec.inp["pseudospherical"] = ""

    uvspec.inp["sza"] = str(sza)
    #uvspec.inp["umu"] = '1.0'
    #uvspec.inp["phi"] = '0.0'
    #uvspec.inp["phi0"] = '180.0'
    uvspec.inp["zout"] = zout

    uvspec.inp["rte_solver"] = rte_solver
    uvspec.inp["mol_abs_param"] = 'reptran fine'
    if O3>0:
        uvspec.inp["mol_modify O3"] = O3+" DU"
    if H2O>0:
        uvspec.inp["mol_modify H2O"] = H2O+" MM"
    if CH4>0:
        uvspec.inp["mol_modify CH4"] = CH4+" cm_2"
    if CO2>0:
        uvspec.inp["mol_modify CO2"] = CO2+" cm_2"

    #deltam off               # disable delta-scaling

    #uvspec.inp["number_of_streams"] = "24"      # number of streams used in DISORT

    uvspec.inp["wavelength"] = "250.0 2500.0"  # Wavelength range [nm]

    uvspec.inp["aerosol_default"] = ""  # the simplest way to include aerosol :-)
    uvspec.inp["aerosol_visibility"] = aerosol  # the simplest way to include aerosol :-)
    uvspec.inp["output_user"] = "lambda edir edn eup uavg uu eglo"

    #uvspec.inp["output_quantity"] = 'reflectivity' #'transmittance' #

    uvspec.write_input(inp)
    uvspec.run(inp,out,verbose,path=libradtranpath)
    return None

def plotRTSpectrum(lambd,edir,edn,eup,uavg):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(lambd,edir)
    ax.plot(lambd,edn)
    ax.plot(lambd,eup)
    ax.plot(lambd,uavg)
    ax.set_xlabel(r"$\lambda$ (nm)")
    ax.set_ylabel(r"Brightness")
    ax.set_ylim([0,2000])
    fig.savefig('%s/%s.png'%(PLOTDIR,filename))
    return None