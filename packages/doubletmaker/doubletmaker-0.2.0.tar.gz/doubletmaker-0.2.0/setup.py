# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doubletmaker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'doubletmaker',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Patrick Lynch',
    'author_email': 'p@tricklynch.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
