from setuptools import setup, find_packages


# Details
PACKAGE_NAME = 'pysustrans'
AUTHOR = 'Rahul Raoniar'
EMAIL = "rahul.raoniar@outlook.com"
URL = 'https://github.com/rahul-raoniar/pysustrans'
DOWNLOAD_URL = 'https://pypi.org/project/pysustrans/'
VERSION = "0.0.107"
DESCRIPTION = 'pysustran is a statistical Python package for Transportation data analysis.'
LONG_DESCRIPTION = 'A package that allows performing common statitical analysis on transportation related data.'
LICENSE = 'MIT'
CLASSIFIERS = [
        'Programming Language :: Python :: 3'
]

LONG_DESC_TYPE = "text/markdown"


# Setting up
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESC_TYPE,
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'pandas', 'matplotlib', 'seaborn'],
    classifiers= CLASSIFIERS,
)

