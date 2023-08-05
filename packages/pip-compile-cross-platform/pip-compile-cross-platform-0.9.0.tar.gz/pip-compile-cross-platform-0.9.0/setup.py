# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pip_compile_cross_platform']

package_data = \
{'': ['*']}

install_requires = \
['pip-requirements-parser>=31.2.0,<32.0.0', 'poetry>=1.2.0b1,<2.0.0']

setup_kwargs = {
    'name': 'pip-compile-cross-platform',
    'version': '0.9.0',
    'description': '',
    'long_description': None,
    'author': 'Mitchell Hentges',
    'author_email': 'mitch9654@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
