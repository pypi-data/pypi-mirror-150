# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitmproxy2swagger', 'mitmproxy2swagger.swagger_util']

package_data = \
{'': ['*']}

install_requires = \
['mitmproxy>=8.0.0,<9.0.0', 'ruamel.yaml>=0.17.21,<0.18.0']

entry_points = \
{'console_scripts': ['mitmproxy2swagger = '
                     'mitmproxy2swagger.mitmproxy2swagger:main']}

setup_kwargs = {
    'name': 'mitmproxy2swagger',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'alufers',
    'author_email': 'alufers@wp.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
