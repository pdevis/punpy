.. Examples
   Author: Pieter De Vis
   Email: pieter.de.vis@npl.co.uk
   Created: 15/04/20

.. _examples:

Examples on how to use the punpy package
==================================================

in progress

1D input quantities and measurand
###################################

input arrays and measurand of length N, covariance of shape (N,N)

2D input quantities and measurand
###################################

input arrays and measurand of shape (M,N)
covariance matrices are flattened so that they are 2D arrays. (M*N,M*N) 


constants in 1D or 2D measurement functions
##############################################
allowed within punpy
constants are expanded into the shape of the input arrays.
e.g. is x2 in the measurement function is a constant::

   x2_array=x2_constant*np.ones_like(x1)

The uncertainty on this constant (single number) will, by definition, be treated as a systematic uncertainty common between all elements of the measurand.