# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['been']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'been',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dmitry Rubinstein',
    'author_email': 'dmitry@cyolo.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
