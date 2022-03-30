from setuptools import find_packages, setup
from glob import glob
from os.path import basename

setup(
    name='statsu',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    author='sbyim'
)