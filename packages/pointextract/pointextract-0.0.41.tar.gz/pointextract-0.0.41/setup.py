from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pointextract',
    version='0.0.41',
    keywords=['pointextract','PowerPlant','Engineering','3d visualization'],
    description='Extract points information from 2d images to build a 3D object',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://engineering.case.edu/centers/sdle/',
    author='Roger French(ORCID:000000-0002-6162-0532), Liangyi Huang(ORCID:0000-0003-0845-3293)',
    author_email='roger.french@case.edu, lxh442@case.edu',
    # BSD 3-Clause License:
    # - http://choosealicense.com/licenses/bsd-3-clause
    # - http://opensource.org/licenses/BSD-3-Clause
    license='BSD License (BSD-3)',
    packages=find_packages(),
    include_package_data=True,
)