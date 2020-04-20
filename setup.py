from setuptools import find_packages, setup

from os import path
from io import open

# Get package __version__.
# Same effect as "from s import __version__",
# but avoids importing the module which may not be installed yet:
__version__ = None
here = path.abspath(path.dirname(__file__))
with open('punpy/version.py') as f:
    exec(f.read())

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='punpy',
      version=__version__,
      description='Propagating UNcertainties in PYthon',
      author='Pieter De vis',
      long_description=long_description,
      author_email='pieter.de.vis@npl.co.uk',
      url='https://github.com/pdevis/punpy',
      keywords="uncertainty propagation covariance MC measurement function",
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=['numpy','matplotlib'],
)
