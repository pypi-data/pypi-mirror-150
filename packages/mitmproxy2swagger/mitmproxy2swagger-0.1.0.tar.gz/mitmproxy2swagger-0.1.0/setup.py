# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mitmproxy2swagger']
install_requires = \
['mitmproxy>=8.0.0,<9.0.0', 'ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'mitmproxy2swagger',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'alufers',
    'author_email': 'alufers@wp.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
