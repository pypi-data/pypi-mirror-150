# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allay']

package_data = \
{'': ['*']}

install_requires = \
['tokenstream>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'allay',
    'version': '1.3.0',
    'description': 'A parser to convert a descriptive text format into minecraft text components',
    'long_description': None,
    'author': 'DoubleFelix',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
