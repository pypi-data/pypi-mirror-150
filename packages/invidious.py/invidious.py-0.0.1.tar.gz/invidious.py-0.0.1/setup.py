from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Python wrapper for Invidious API'
LONG_DESCRIPTION = 'A package that make work with Invidious API so easy.'

# Setting up
setup(
    name="invidious.py",
    version=VERSION,
    author="loliconshik3",
    author_email="loliconshik3@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'invidious', 'youtube', 'video', 'api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)