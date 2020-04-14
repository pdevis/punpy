"""
Tests for mc propagation class
"""

import unittest
import numpy as np
import numpy.testing as npt
from punpy.version import __version__
import punpy

'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "14/4/2020"
__version__ = __version__
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"

def test_function(x1,x2):
    return 2* x1 - x2

x1=np.ones(200)*50
x2=np.ones(200)*30
x1err=np.ones(200)
x2err=2*np.ones(200)
yerr_uncorr=8**0.5*np.ones(200)
yerr_corr=np.zeros(200)

class TestMCPropagation(unittest.TestCase):
    def test_propagate_random(self):
        prop = punpy.MCPropagation(10000)

        uf,ucorr = prop.propagate_random(test_function,[x1,x2],[x1err,x2err],
                                         only_u=False)
        npt.assert_allclose(ucorr,np.eye(len(ucorr)),atol=0.05)
        npt.assert_allclose(uf,yerr_uncorr,rtol=0.03)

        uf = prop.propagate_random(test_function,[x1,x2],
                                   [x1err,x2err],corr_between=np.ones((2,2)))
        npt.assert_allclose(uf,yerr_corr,atol=0.03)

    def test_propagate_systematic(self):
        prop = punpy.MCPropagation(10000)

        uf,ucorr = prop.propagate_systematic(test_function,[x1,x2],[x1err,x2err],
                                         only_u=False)
        npt.assert_allclose(ucorr,np.ones_like(ucorr),atol=0.05)
        npt.assert_allclose(uf,yerr_uncorr,rtol=0.03)

        uf = prop.propagate_random(test_function,[x1,x2],[x1err,x2err],
                                   corr_between=np.ones((2,2)))
        npt.assert_allclose(uf,yerr_corr,atol=0.03)

    def test_propagate_both(self):
        prop = punpy.MCPropagation(10000)

        uf,ucorr = prop.propagate_both(test_function,[x1,x2],[x1err,x2err],
                                       [np.zeros_like(x1err),np.zeros_like(x2err)],return_corr=True)
        npt.assert_allclose(ucorr,np.eye(len(ucorr)),atol=0.05)
        npt.assert_allclose(uf,yerr_uncorr,rtol=0.03)

        uf,ucorr = prop.propagate_both(test_function,[x1,x2],[np.zeros_like(x1err),np.zeros_like(x2err)],
                                       [x1err,x2err],return_corr=True)
        npt.assert_allclose(ucorr,np.ones_like(ucorr),atol=0.05)
        npt.assert_allclose(uf,yerr_uncorr,rtol=0.03)

        uf = prop.propagate_both(test_function,[x1,x2],[x1err,x2err],[np.zeros_like(x1err),np.zeros_like(x2err)],
                                 only_u=True,corr_between=np.ones((2,2)))
        npt.assert_allclose(uf,yerr_corr,atol=0.03)

    def test_propagate_type(self):
        prop = punpy.MCPropagation(10000)

        uf,ucorr = prop.propagate_type(test_function,[x1,x2],[x1err,x2err],['rand','rand'],return_corr=True)
        npt.assert_allclose(ucorr,np.eye(len(ucorr)),atol=0.05)
        npt.assert_allclose(uf,yerr_uncorr,rtol=0.03)

        uf,ucorr = prop.propagate_type(test_function,[x1,x2],[x1err,x2err],['syst','syst'],return_corr=True)

        npt.assert_allclose(ucorr,np.ones_like(ucorr),atol=0.05)
        npt.assert_allclose(uf,yerr_uncorr,rtol=0.03)

        uf = prop.propagate_type(test_function,[x1,x2],[x1err,x2err],['rand','rand'],return_corr=False,corr_between=np.ones((2,2)))
        npt.assert_allclose(uf,yerr_corr,atol=0.03)

if __name__ == '__main__':
    unittest.main()
