# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst', encoding="utf-8") as f:
    readme = f.read()

setup(
    name='cryptopp',
    version='1.0.3',
    description='Command line Cryptocurrency Portfolio',
    long_description=readme,
    author='GordianSimpul/huwwp',
    author_email='gordian@simpul.me',
    url='https://github.com/GordianSimpul/cryptopp',
    license='GPLv3',
    keywords='crypto cli portfolio curses cryptocurrency bitcoin',
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    install_requires=['requests', 'requests_cache'],
    package_data={'cryptopp': ['config.ini']},
    entry_points = {
        'console_scripts': ['cryptopp = cryptopp.cryptopp:main'],
    }
)
