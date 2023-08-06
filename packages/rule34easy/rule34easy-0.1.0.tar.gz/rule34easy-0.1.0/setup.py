# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rule34easy']
setup_kwargs = {
    'name': 'rule34easy',
    'version': '0.1.0',
    'description': 'Package for easy use rule34 API',
    'long_description': None,
    'author': 'MoDiFy',
    'author_email': 'mindustrys1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
