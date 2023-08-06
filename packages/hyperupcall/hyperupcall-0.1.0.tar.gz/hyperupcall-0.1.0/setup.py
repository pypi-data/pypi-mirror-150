# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyperupcall']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hyperupcall',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Edwin Kofler',
    'author_email': 'edwin@kofler.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
