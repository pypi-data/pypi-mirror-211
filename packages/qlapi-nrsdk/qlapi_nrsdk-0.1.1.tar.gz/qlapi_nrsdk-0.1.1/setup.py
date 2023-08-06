from setuptools import setup
from setuptools import find_packages

VERSION = '0.1.1'
AUTHOR='eegion'
EMAIL='hehuajun@eegion.com'
REQUIRED = [
    'beautifulsoup',
    "lxml"
]

setup(
    name='qlapi_nrsdk',  # package name
    version=VERSION,  # package version
    author=AUTHOR,
    author_email=EMAIL,
    requires=REQUIRED,
    description='Api for use quanlan device',  # package description
    packages=find_packages(),
    package_data={
        "qlapi": ["lib/*.dll"],
        "":["*.txt", "*.md"]
    },
    zip_safe=False,
)