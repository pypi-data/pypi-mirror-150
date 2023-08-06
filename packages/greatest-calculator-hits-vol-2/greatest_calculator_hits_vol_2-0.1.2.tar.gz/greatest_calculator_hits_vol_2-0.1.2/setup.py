# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['greatest_calculator_hits_vol_2']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'greatest-calculator-hits-vol-2',
    'version': '0.1.2',
    'description': 'A very basic python calculator',
    'long_description': '',
    'author': 'heliossjr',
    'author_email': 'helio.junior@loggi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/heliossjr/greatest_calculator_hits',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
