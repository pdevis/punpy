"""Use Monte Carlo to propagate uncertainties"""

import numpy as np
import time

'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "30/03/2019"
__maintainer__ = "Pieter De Vis"
__email__ = "pieter.de.vis@npl.co.uk"
__status__ = "Development"

class MCPropagation:
    def __init__(self,steps):
        """
        Initialise MC Propagator

        :param steps: number of MC iterations
        :type steps: int
        """

        self.MCsteps = steps


    def propagate_random(self,func,x,u_x,corr_between=None,return_corr=False,return_samples=False):
        """
        Propagate random uncertainties through measurement function with n input quantities.
        Input quantities can be floats, vectors or images.

        :param func: measurement function
        :type func: function
        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param u_x: list of random uncertainties on input quantities (usually numpy arrays)
        :type u_x: list[array]
        :param corr_between: covariance matrix (n,n) between input quantities, defaults to None
        :type corr_between: array, optional
        :param return_corr: set to True to return correlation matrix of measurand, defaults to False
        :type return_corr: bool, optional
        :param return_samples: set to True to return generated samples, defaults to False
        :type return_samples: bool, optional
        :return: uncertainties on measurand
        :rtype: array
        """
        MC_data = np.empty(len(x),dtype=np.ndarray)
        for i in range(len(x)):
            MC_data[i] = self.generate_samples_random(x[i],u_x[i])

        if corr_between is not None:
            MC_data = self.correlate_samples_corr(MC_data,corr_between)

        return self.process_samples(func,MC_data,return_corr,return_samples)

    def propagate_systematic(self,func,x,u_x,corr_between=None,return_corr=False,return_samples=False):
        """
        Propagate systematic uncertainties through measurement function with n input quantities.
        Input quantities can be floats, vectors or images.

        :param func: measurement function
        :type func: function
        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param u_x: list of systematic uncertainties on input quantities (usually numpy arrays)
        :type u_x: list[array]
        :param corr_between: covariance matrix (n,n) between input quantities, defaults to None
        :type corr_between: array, optional
        :param return_corr: set to True to return correlation matrix of measurand, defaults to False
        :type return_corr: bool, optional
        :param return_samples: set to True to return generated samples, defaults to False
        :type return_samples: bool, optional
        :return: uncertainties on measurand
        :rtype: array
        """
        MC_data = np.empty(len(x),dtype=np.ndarray)
        for i in range(len(x)):
            MC_data[i] = self.generate_samples_systematic(x[i],u_x[i])

        if corr_between is not None:
            MC_data = self.correlate_samples_corr(MC_data,corr_between)

        return self.process_samples(func,MC_data,return_corr,return_samples)

    def propagate_both(self,func,x,u_x_rand,u_x_syst,corr_between=None,return_corr=True,return_samples=False):
        """
        Propagate random and systematic uncertainties through measurement function with n input quantities.
        Input quantities can be floats, vectors or images.

        :param func: measurement function
        :type func: function
        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param u_x_rand: list of random uncertainties on input quantities (usually numpy arrays)
        :type u_x_rand: list[array]
        :param u_x_syst: list of systematic uncertainties on input quantities (usually numpy arrays)
        :type u_x_syst: list[array]
        :param corr_between: covariance matrix (n,n) between input quantities, defaults to None
        :type corr_between: array, optional
        :param return_corr: set to True to return correlation matrix of measurand, defaults to True
        :type return_corr: bool, optional
        :param return_samples: set to True to return generated samples, defaults to False
        :type return_samples: bool, optional
        :return: uncertainties on measurand
        :rtype: array
        """
        MC_data = np.empty(len(x),dtype=np.ndarray)
        for i in range(len(x)):
            MC_data[i] = self.generate_samples_both(x[i],u_x_rand[i],u_x_syst[i])

        if corr_between is not None:
            MC_data = self.correlate_samples_corr(MC_data,corr_between)

        return self.process_samples(func,MC_data,return_corr,return_samples)

    def propagate_type(self,func,x,u_x,u_type,corr_between=None,return_corr=True,return_samples=False):
        """
        Propagate random or systematic uncertainties through measurement function with n input quantities.
        Input quantities can be floats, vectors or images.

        :param func: measurement function
        :type func: function
        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param u_x: list of uncertainties on input quantities (usually numpy arrays)
        :type u_x: list[array]
        :param u_type: sting identifiers whether uncertainties are random or systematic
        :type u_type: list[str]
        :param corr_between: covariance matrix (n,n) between input quantities, defaults to None
        :type corr_between: array, optional
        :param return_corr: set to True to return correlation matrix of measurand, defaults to True
        :type return_corr: bool, optional
        :param return_samples: set to True to return generated samples, defaults to False
        :type return_samples: bool, optional
        :return: uncertainties on measurand
        :rtype: array
        """
        MC_data = np.empty(len(x),dtype=np.ndarray)
        for i in range(len(x)):
            if u_type[i].lower() == 'rand' or u_type[i].lower() == 'random' or u_type[i].lower() == 'r':
                MC_data[i] = self.generate_samples_random(x[i],u_x[i])
            elif u_type[i].lower() == 'syst' or u_type[i].lower() == 'systematic' or u_type[i].lower() == 's':
                MC_data[i] = self.generate_samples_systematic(x[i],u_x[i])
            else:
                raise ValueError(
                    'Uncertainty type not understood. Use random ("random", "rand" or "r") or systematic ("systematic", "syst" or "s").')

        if corr_between is not None:
            MC_data = self.correlate_samples_corr(MC_data,corr_between)

        return self.process_samples(func,MC_data,return_corr,return_samples)

    def propagate_cov(self,func,x,cov_x,corr_between=None,return_corr=True,return_samples=False):
        """
        Propagate uncertainties with given covariance matrix through measurement function with n input quantities.
        Input quantities can be floats, vectors or images.

        :param func: measurement function
        :type func: function
        :param x: list of input quantities (usually numpy arrays)
        :type x: list[array]
        :param cov_x: list of covariance matrices on input quantities (usually numpy arrays). In case the input quantity is an array of shape (m,o), the covariance matrix needs to be given as an array of shape (m*o,m*o).
        :type cov_x: list[array]
        :param corr_between: covariance matrix (n,n) between input quantities, defaults to None
        :type corr_between: array, optional
        :param return_corr: set to True to return correlation matrix of measurand, defaults to True
        :type return_corr: bool, optional
        :param return_samples: set to True to return generated samples, defaults to False
        :type return_samples: bool, optional
        :return: uncertainties on measurand
        :rtype: array
        """
        MC_data = np.empty(len(x),dtype=np.ndarray)
        for i in range(len(x)):
            if not hasattr(x[i],"__len__"):
                MC_data[i] = self.generate_samples_systematic(x[i],cov_x[i])
            else:
                MC_data[i] = self.generate_samples_cov(x[i].flatten(),cov_x[i]).reshape(x[i].shape+(self.MCsteps,))

        if corr_between is not None:
            MC_data = self.correlate_samples_corr(MC_data,corr_between)

        return self.process_samples(func,MC_data,return_corr,return_samples)

    def process_samples(self,func,data,return_corr,return_samples):
        """
        Run the MC-generated samples of input quantities through the measurement function and calculate
        correlation matrix if required.

        :param func: measurement function
        :type func: function
        :param data: MC-generated samples of input quantities
        :type data: array[array]
        :param return_corr: set to True to return correlation matrix of measurand
        :type return_corr: bool
        :param return_samples: set to True to return generated samples
        :type return_samples: bool
        :return: uncertainties on measurand
        :rtype: array
        """
        MC_y = func(*data)
        u_func = np.std(MC_y,axis=-1)
        if not return_corr:
            if return_samples:
                return u_func,MC_y,data
            else:
                return u_func
        else:
            if len(MC_y.shape) == 3:
                MC_y = MC_y.reshape((MC_y.shape[0]*MC_y.shape[1],self.MCsteps))
            corr_y = np.corrcoef(MC_y)
            if return_samples:
                return u_func,corr_y,MC_y,data
            else:
                return u_func,corr_y

    def generate_samples_random(self,param,u_param):
        """
        Generate MC samples of input quantity with random (Gaussian) uncertainties.

        :param param: values of input quantity (mean of distribution)
        :type param: float or array
        :param u_param: uncertainties on input quantity (std of distribution)
        :type u_param: float or array
        :return: generated samples
        :rtype: array
        """
        if not hasattr(param,"__len__"):
            return np.random.normal(size=self.MCsteps)*u_param+param
        elif len(param.shape) == 1:
            return np.random.normal(size=(len(param),self.MCsteps))*u_param[:,None]+param[:,None]
        elif len(param.shape) == 2:
            return np.random.normal(size=param.shape+(self.MCsteps,))*u_param[:,:,None]+param[:,:,None]
        else:
            print("parameter shape not supported")
            return None

    def generate_samples_systematic(self,param,u_param):
        """
        Generate correlated MC samples of input quantity with systematic (Gaussian) uncertainties.

        :param param: values of input quantity (mean of distribution)
        :type param: float or array
        :param u_param: uncertainties on input quantity (std of distribution)
        :type u_param: float or array
        :return: generated samples
        :rtype: array
        """
        if not hasattr(param,"__len__"):
            return np.random.normal(size=self.MCsteps)*u_param+param
        elif len(param.shape) == 1:
            return np.dot(u_param[:,None],np.random.normal(size=self.MCsteps)[None,:])+param[:,None]
        elif len(param.shape) == 2:
            return np.dot(u_param[:,:,None],np.random.normal(size=self.MCsteps)[:,None,None])[:,:,:,0]+param[:,:,None]
        else:
            print("parameter shape not supported")
            return None

    def generate_samples_both(self,param,u_param_rand,u_param_syst):
        """
        Generate correlated MC samples of the input quantity with random and systematic (Gaussian) uncertainties.

        :param param: values of input quantity (mean of distribution)
        :type param: float or array
        :param u_param_rand: random uncertainties on input quantity (std of distribution)
        :type u_param_rand: float or array
        :param u_param_syst: systematic uncertainties on input quantity (std of distribution)
        :type u_param_syst: float or array
        :return: generated samples
        :rtype: array
        """
        if not hasattr(param,"__len__"):
            return np.random.normal(size=self.MCsteps)*u_param_rand+np.random.normal(
                size=self.MCsteps)*u_param_syst+param
        elif len(param.shape) == 1:
            return np.random.normal(size=(len(param),self.MCsteps))*u_param_rand[:,None]+np.dot(u_param_syst[:,None],
                                                                                                np.random.normal(
                                                                                                    size=self.MCsteps)[
                                                                                                None,:])+param[:,None]
        elif len(param.shape) == 2:
            return np.random.normal(size=param.shape+(self.MCsteps,))*u_param_rand[:,:,None]+np.dot(
                u_param_syst[:,:,None],np.random.normal(size=self.MCsteps)[:,None,None])[:,:,:,0]+param[:,:,None]
        else:
            print("parameter shape not supported")
            return None

    def generate_samples_cov(self,param,cov_param):
        """
        Generate correlated MC samples of input quantity with a given covariance matrix.
        Samples are generated independent and then correlated using Cholesky decomposition.

        :param param: values of input quantity (mean of distribution)
        :type param: array
        :param cov_param: covariance matrix for input quantity
        :type cov_param: array
        :return: generated samples
        :rtype: array
        """
        try:
            L = np.linalg.cholesky(cov_param)
        except:
            cov = self.nearestPD(cov_param)
            L = np.linalg.cholesky(cov_param)
        return np.dot(L,np.random.normal(size=(len(param),self.MCsteps)))+param[:,None]

    def correlate_samples_corr(self,samples,corr):
        """
        Method to correlate independent samples of input quantities using correlation matrix and Cholesky decomposition.

        :param samples: independent samples of input quantities
        :type samples: array[array]
        :param corr: correlation matrix between input quantities
        :type corr: array
        :return: correlated samples of input quantities
        :rtype: array[array]
        """
        if np.max(corr) > 1 or len(corr) != len(samples):
            raise ValueError("The correlation matrix between variables is not the right shape or has elements >1.")
        else:
            try:
                L = np.linalg.cholesky(corr)
            except:
                corr = self.nearestPD(corr)
                L = np.linalg.cholesky(corr)

            #Cholesky needs to be applied to Gaussian distributions with mean=0 and std=1,
            #We first calculate the mean and std for each input quantity
            means = [np.mean(samples[i]) for i in range(len(samples))]
            stds = [np.std(samples[i]) for i in range(len(samples))]

            #We normalise the samples with the mean and std, then apply Cholesky, and finally reapply the mean and std.
            return np.dot(L,(samples-means)/stds)*stds+means

    @staticmethod
    def nearestPD(A):
        """
        Find the nearest positive-definite matrix

        :param A: correlation matrix or covariance matrix
        :type A: array
        :return: nearest positive-definite matrix
        :rtype: array

        Copied and adapted from [1] under BSD license.
        A Python/Numpy port of John D'Errico's `nearestSPD` MATLAB code [2], which
        credits [3].

        [1] https://gist.github.com/fasiha/fdb5cec2054e6f1c6ae35476045a0bbd

        [2] https://www.mathworks.com/matlabcentral/fileexchange/42885-nearestspd

        [3] N.J. Higham, "Computing a nearest symmetric positive semidefinite
        matrix" (1988): https://doi.org/10.1016/0024-3795(88)90223-6
        """

        B = (A+A.T)/2
        _,s,V = np.linalg.svd(B)

        H = np.dot(V.T,np.dot(np.diag(s),V))

        A2 = (B+H)/2

        A3 = (A2+A2.T)/2

        if MCPropagation.isPD(A3):
            return A3

        spacing = np.spacing(np.linalg.norm(A))

        I = np.eye(A.shape[0])
        k = 1
        while not MCPropagation.isPD(A3):
            mineig = np.min(np.real(np.linalg.eigvals(A3)))
            A3 += I*(-mineig*k**2+spacing)
            k += 1

        if np.any(abs(A-A3)/A > 0.0001):
            raise ValueError(
                "One of the provided covariance matrix is not postive definite. Covariance matrices need to be at least positive semi-definite. Please check your covariance matrix.")
        else:
            print(
                "One of the provided covariance matrix is not positive definite. It has been slightly changed (less than 0.01% in any element) to accomodate our method.")
            return A3

    @staticmethod
    def isPD(B):
        """
        Returns true when input is positive-definite, via Cholesky

        :param B: matrix
        :type B: array
        :return: true when input is positive-definite
        :rtype: bool
        """
        try:
            _ = np.linalg.cholesky(B)
            return True
        except np.linalg.LinAlgError:
            return False

    @staticmethod
    def convert_corr_to_cov(corr,u):
        """
        Convert correlation matrix to covariance matrix

        :param corr: correlation matrix
        :type corr: array
        :param u: uncertainties
        :type u: array
        :return: covariance matrix
        :rtype: array
        """
        return u.flatten()*corr*u.flatten().T

    @staticmethod
    def convert_cov_to_corr(cov,u):
        """
        Convert covariance matrix to correlation matrix

        :param corr: covariance matrix
        :type corr: array
        :param u: uncertainties
        :type u: array
        :return: correlation matrix
        :rtype: array
        """
        return 1/u.flatten()*cov/u.flatten().T
