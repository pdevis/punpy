.. Examples
   Author: Pieter De Vis
   Email: pieter.de.vis@npl.co.uk
   Created: 15/04/20

.. _examples:

Examples on how to use the punpy package
==================================================

In progress...

1D input quantities and measurand
###################################

Input arrays and measurand of length N, covariance of shape (N,N)

2D input quantities and measurand
###################################

Input arrays and measurand of shape (M,N)

Covariance matrices are flattened so that they are 2D arrays. (M*N,M*N)


Constants in 1D or 2D measurement functions
##############################################
Allowed within punpy

Constants are expanded into the shape of the input arrays.

E.g. if x2 in the measurement function is a constant::

   x2_array=x2_constant*np.ones_like(x1)

The uncertainty on this constant (single number) is treated as a systematic uncertainty common between all elements of the measurand.