import setuptools
from setuptools import setup
from lchelper.constants import VERSION


with open("lchelper/requirements.txt", "r") as f:
    install_requires = f.read().splitlines()


setup(
    name='lchelper',
    version=VERSION,
    packages=setuptools.find_packages(),
    install_requires=install_requires
)
