# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testfolio']

package_data = \
{'': ['*']}

install_requires = \
['yfinance>=0.1.70']

setup_kwargs = {
    'name': 'testfolio',
    'version': '0.1.0a0',
    'description': "Library that backtests a given portfolio's asset allocation using historical market data from Yahoo.",
    'long_description': '# testfolio\n',
    'author': 'Bradley He',
    'author_email': 'bhe6001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BradleyHe/testfolio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
