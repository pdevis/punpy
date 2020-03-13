"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''
from kumara.sensors.TRUTHS import TRUTHS

'''___Third-Party Modules___'''


'''___NPL Modules___'''


'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "11/11/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"


class SensorFactory():
    @staticmethod
    def create_sensor(sensor,*args,**kwargs):
        if sensor=='TRUTHS':
            print("Using TRUTHS instrument \n")
            return TRUTHS(*args,**kwargs)


