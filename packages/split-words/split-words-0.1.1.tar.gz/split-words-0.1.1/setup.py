# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['split_words']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'split-words',
    'version': '0.1.1',
    'description': 'Split German words',
    'long_description': None,
    'author': 'freemt',
    'author_email': 'yucongo+fmt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
