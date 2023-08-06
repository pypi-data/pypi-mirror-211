import setuptools
from setuptools import setup
from lchelper.constants import VERSION


install_requires = []

setup(
    name='lchelper',
    version=VERSION,
    packages=setuptools.find_packages(),
    install_requires=install_requires
)
