# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decoration']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'decoration',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Samy CHBINOU',
    'author_email': 'samy.chbinou@greenflows.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
