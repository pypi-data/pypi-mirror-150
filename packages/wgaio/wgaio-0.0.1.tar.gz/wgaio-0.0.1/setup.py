# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wgaio']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wgaio',
    'version': '0.0.1',
    'description': 'Asynchronous Wargaming API client',
    'long_description': '# Ayncronous Wargaming API client',
    'author': 'Sergey Tsaplin',
    'author_email': 'me@sergeytsaplin.com',
    'maintainer': 'Sergey Tsaplin',
    'maintainer_email': 'me@sergeytsaplin.com',
    'url': 'https://github.com/SergeyTsaplin/wgaio',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
