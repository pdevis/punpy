"""Run MCMC for atmospheric retrieval"""

'''___Built-In Modules___'''
from kumara.retrieval.MCMCRetrieval import MCMCRetrieval

'''___Third-Party Modules___'''


'''___NPL Modules___'''


'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "11/11/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"


class RetrievalFactory():
    @staticmethod
    def create_retrieval(method,*args,**kwargs):
        if method=='MCMC':
            print("Using MCMC for retrieval \n")
            return MCMCRetrieval(*args,**kwargs)


