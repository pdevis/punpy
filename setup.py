from setuptools import find_packages, setup

from os import path
from io import open

# Get package __version__.
# Same effect as "from s import __version__",
# but avoids importing the module which may not be installed yet:
here = path.abspath(path.dirname(__file__))
__version__ = None
with open('kumara/version.py') as f:
    exec(f.read())

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='kumara',
      version=__version__,
      description='liKelihood-based Uncertainties from Mcmc Atmospheric Retrieval Algorithm package',
      author='Pieter De vis',
      long_description=long_description,
      author_email='pieter.de.vis@npl.co.uk',
      url='http://www.npl.co.uk',
      keywords="MCMC atmospheric retrieval",
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=['numpy',
                        'emcee'],
)
