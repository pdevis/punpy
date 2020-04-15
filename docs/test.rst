Principles of Uncertainty Analysis
----------------------------------

The Guide to the expression of Uncertainty in Measurement (GUM 2008)
provides a framework for how to determine and express the uncertainty of
the measured value of a given measurand (the quantity which is being
measured). The International Vocabulary of Metrology (VIM 2008) defines
measurement uncertainty as:

   *“a non-negative parameter characterizing the dispersion of the
   quantity values*

   *being attributed to a measurand, based on the information used.”*

The standard uncertainty is the measurement uncertainty expressed as a
standard deviation. Please note this is a separate concept to
measurement error, which is also defined in the VIM as:

   *“the measured quantity value minus a reference quantity value.”*

Generally, the “reference quantity” is considered to be the “true value”
of the measurand and is therefore unknown. Figure 2‑1 illustrates these
concepts.

|image0|

Figure 2‑1 - Diagram illustrating the different concepts of measured
value and true value, uncertainty and error.

Within the GUM framework uncertainty analysis begins with understanding
the measurement function. The measurement function establishes the
mathematical relationship between all known input quantities (e.g.
instrument counts) and the measurand itself (e.g. radiance). Generally,
this may be written as

.. math:: y = f\left( x_{i},\ldots,\ x_{N} \right)

where:

-  :math:`y` is the measurand;

-  :math:`x_{i}` are the input quantities.

Uncertainty analysis is then performed by considering in turn each of
these different input quantities to the measurement function, this
process is represented in Figure 2‑2. Each input quantity may be
influenced by one or more error effects which are described by an
uncertainty distribution. These separate distributions may then be
combined to determine the uncertainty of the measurand,
:math:`u^{2}(Y)`, using the *Law of Propagation of Uncertainties* (GUM,
2008),

.. math:: u^{2}\left( y \right) = \mathbf{\text{cS}}\left( \mathbf{x} \right)\mathbf{c}^{T}

where:

-  :math:`\mathbf{C}` is the vector of sensitivity coefficients,
   :math:`\partial Y/\partial X_{i}`;

-  :math:`\mathbf{S(x)}` is the error covariance matrix for the input
   quantities.

|image1|

Figure 2‑2 - Conceptual process of uncertainty propagation.

In a series of measurements (for example each pixel in a remote sensing
Level 1 (L1) data product) it is vital to consider how the errors
between the measurements in the series are correlated. This is crucial
when evaluating the uncertainty of a result derived from these data (for
example a Level 2 (L2) retrieval of geophysical parameter from a L1
product). In their vocabulary the Horizon 2020 FIDUCEO [1]_ (Fidelity
and uncertainty in climate data records from Earth observations) project
(see FIDUCEO Vocabulary, 2018) define three broad categories of error
correlation effects important to satellite data products, as follows:

-  **Random effects**: *“those causing errors that cannot be corrected
   for in a single measured value, even in principle, because the effect
   is stochastic. Random effects for a particular measurement process
   vary unpredictably from (one set of) measurement(s) to (another set
   of) measurement(s). These produce random errors which are entirely
   uncorrelated between measurements (or sets of measurements) and
   generally are reduced by averaging.”*

-  **Structured random effects**: *“means those that across many
   observations there is a deterministic pattern of errors whose
   amplitude is stochastically drawn from an underlying probability
   distribution; “structured random” therefore implies “unpredictable”
   and “correlated across measurements”…”*

-  **Systematic (or common) effects**: *“those for a particular
   measurement process that do not vary (or vary coherently) from (one
   set of) measurement(s) to (another set of) measurement(s) and
   therefore produce systematic errors that cannot be reduced by
   averaging.”*

.. [1]
   See: https://www.fiduceo.eu

.. |image0| image:: media/image1.png
   :width: 3.97506in
   :height: 2.46154in
.. |image1| image:: media/image2.emf
   :width: 4.61478in
   :height: 2.66265in
