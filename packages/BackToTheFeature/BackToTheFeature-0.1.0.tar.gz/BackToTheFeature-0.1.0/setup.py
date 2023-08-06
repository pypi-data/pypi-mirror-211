from setuptools import setup, find_packages

setup(
    name='BackToTheFeature',
    version='0.1.0',
    url='https://github.com/Repsajsov/BackToTheFeature/tree/main/base-folder/BackToTheFeature',
    author='Jasper Vos',
    author_email='jaspervos12@outlook.com',
    description='A Python package that provides functionality for data processing and analysis using the "BackToTheFeature" class, derived from pandas DataFrame, for managing and manipulating time-related features.',
    packages=find_packages(),    
    install_requires=[
        'pandas >= 1.1.5',
    ],
)