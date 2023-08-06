# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['passive_auto_design',
 'passive_auto_design.components',
 'passive_auto_design.devices',
 'passive_auto_design.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'scikit-rf>=0.22.1,<0.23.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'passive-auto-design',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Patarimi',
    'author_email': '38954040+Patarimi@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
