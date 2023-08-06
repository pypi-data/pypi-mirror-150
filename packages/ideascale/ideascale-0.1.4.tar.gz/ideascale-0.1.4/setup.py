from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.1.4'
DESCRIPTION = 'This package is for ideascale'
LONG_DESCRIPTION='This package helps to create multiple file format xlsx, md, and html that follow specification for Ideascale'

# Setting up
setup(
    name="ideascale",
    version=VERSION,
    author="Tien Nguyen",
    author_email="tiennguyenhotel97@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','xlsxwriter','openpyxl'],
    keywords=['python', 'excel'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
