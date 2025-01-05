import os
from setuptools import setup, find_packages

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'PyPI_README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    print("Exception occurred during parsing README_PyPI.md")
    long_description = ''

# Parse requirements from requirements.txt
try:
    with open(os.path.join(current_directory, 'requirements.txt'), encoding='utf-8') as f:
        requirements = f.read().splitlines()
except Exception:
    print("Exception occurred during parsing requirements.txt")
    requirements = [
        'treys==0.1.8',
        'pokerkit==0.5.4'
    ]

setup(
    # Name of the package
    name='PokerBots',
    packages=find_packages('.'),
    version='2.0.3',
    license='MIT',
    description='A Pure Python library to test your Poker Bots in a trivial and simple way.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nikolay Skripko',
    author_email='nskripko@icloud.com',
    url='https://github.com/Skripkon/PokerBots',
    keywords=[],  # Add relevant keywords
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.11',  # Specify Python version compatibility
)
