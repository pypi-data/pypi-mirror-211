from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.1'

setup(
    name='Baozun-Winrobot',  # package name
    version=VERSION,  # package version
    description='影刀项目',  # package description
    packages=find_packages(),
    zip_safe=False,
)