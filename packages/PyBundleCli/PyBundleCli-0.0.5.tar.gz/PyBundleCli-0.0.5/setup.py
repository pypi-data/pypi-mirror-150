# coding: utf-8

from setuptools import setup, find_packages
from pybundler import __VERSION__


def _requires_from_file(filename):
    return open(filename).read().splitlines()


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_txt = f.read()

setup(
    name='PyBundleCli',
    version=__VERSION__,
    description='bundle python files for command line tools',
    entry_points={
        "console_scripts": [
            "pybundle = pybundler.pybundler:main"
        ]
    },
    long_description=readme,
    author='Kyohei Horikawa',
    author_email='kyohei3430@gmail.com',
    url='https://github.com/kyohei-horikawa/PyBundleCli',
    license=license_txt,
    packages=find_packages(exclude=('sample',)),
    install_requires=_requires_from_file('requirements.txt'),
)
