from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'Predictive machine learning for Celonis'
LONG_DESCRIPTION = 'Enrich Celonis process mining analyses using predictive machine learning and visualisation tools'

# Setting up
setup(
    name="celoMine",
    version=VERSION,
    author="Jean BERTIN",
    author_email="<jeanbertin.ensam@gmail.com>",
    licence="GPL-v3",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pandas', 'numpy' ,'scikit-learn','matplotlib'],
    keywords=['python', 'celonis', 'process mining'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)