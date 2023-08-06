# coding=UTF-8
import sys
from pathlib import Path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    


install_requires = [
    'pandas == 1.2.5',
    'numpy == 1.22.3',
    'exchange-calendar == 3.3.0',
    'requests >= 2.7.0',
    'inflection >= 0.3.1',
    'python-dateutil',
    'six',
    'more-itertools',
    'tejapi',
    'matplotlib',
]

installs_for_two = [
    'pyOpenSSL',
    'ndg-httpsclient',
    'pyasn1'
]

if sys.version_info[0] < 3:
    install_requires += installs_for_two

packages = [
    'zipline-tej',
    'zipline-tej.assets',
    'zipline-tej.data',
    'zipline-tej.examples',
    'zipline-tej.finance',
    'zipline-tej.gens',
    'zipline-tej.lib',
    'zipline-tej.pipeline',
    'zipline-tej.resources',
    'zipline-tej.testing',
    'zipline-tej.utils',
]


this_directionary = Path(__file__).parent
long_description = (this_directionary/"README.rst").read_text(encoding='utf-8')
setup(
    name='zipline-tej',
    description='Package for stock backtesting modified by TEJ.',
    keywords=['tej', 'zipline', 'data', 'financial', 'economic','stock','backtest','TEJ',],
    long_description='tests',
    version='0.0.1',
    author='tej',
    author_email='tej@tej.com.tw',
    maintainer='tej api Development Team',
    maintainer_email='tej@tej.com',
    url='https://api.tej.com.tw',
    license='MIT',
    install_requires=install_requires,
    tests_require=[
        'unittest2',
        'flake8',
        'nose',
        'httpretty',
        'mock',
        'factory_boy',
        'jsondate'
    ],
    test_suite="nose.collector",
    packages=packages
)