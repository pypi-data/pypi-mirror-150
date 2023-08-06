# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comis', 'comis.filters', 'comis.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'asyncpraw>=7.5.0,<8.0.0']

extras_require = \
{'docs': ['Sphinx>=4.5.0,<5.0.0',
          'sphinx-autodoc-typehints>=1.18.1,<2.0.0',
          'pydata-sphinx-theme>=0.8.1,<0.9.0']}

setup_kwargs = {
    'name': 'comis',
    'version': '0.1.0',
    'description': 'comis, the simplest way to create a reddit bot',
    'long_description': None,
    'author': 'Endercheif',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
