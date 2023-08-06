from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.2'

setup(
    name='baozun_winrobot',  # package name
    version=VERSION,  # package version
    description='影刀项目',  # package description
    packages=find_packages(),
    zip_safe=False,
)