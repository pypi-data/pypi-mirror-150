from setuptools import setup

with open("README.rst", 'r') as f:
    long_description = f.read()

setup(
   name='ehrml',
   version='1.0.1',
   description='Utilities for using Models with health data.',
   license="GPL-3",
   long_description=long_description,
   author='Ryan Birmingham',
   author_email='rbirmin@emory.edu',
   packages=['ehrml'],
   install_requires=['numpy']
)
