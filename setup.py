from distutils.core import setup
from setuptools import find_packages
import os


# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    # Name of the package
    name='PokerBots',
    packages=find_packages('.'),
    version='1.1',
    license='MIT',
    description='A Pure Python library to test your Poker Bots in a trivial and simple way.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nikolay Skripko',
    author_email='nskripko@icloud.com',

    # Either the link to your github or to your website
    url='https://www.youtube.com/@_NickTech',

    # Link from which the project can be downloaded
    download_url='',

    # List of keyword arguments
    keywords=[],

    # List of packages to install with this one
    install_requires=[
        'treys==0.1.8'
        ],
)