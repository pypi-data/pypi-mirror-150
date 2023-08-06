# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safebag']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'safebag',
    'version': '0.1.1',
    'description': 'Easy Python package for optional chaining pattern',
    'long_description': None,
    'author': 'Alexandr Solovev',
    'author_email': 'nightingale.alex.info@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
