# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['split_words']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'rich>=12.4.1,<13.0.0',
 'set-loglevel>=0.1.2,<0.2.0',
 'typer>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'split-words',
    'version': '0.1.0',
    'description': 'Split German words',
    'long_description': None,
    'author': 'freemt',
    'author_email': 'yucongo+fmt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
