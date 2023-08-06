# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycrashcourse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycrashcourse',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Oscar Bahamonde',
    'author_email': 'oscarmartinbahamondemunoz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
