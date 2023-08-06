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
    'version': '0.1.1',
    'description': 'comis, the simplest way to create a reddit bot',
    'long_description': '\n# comis #\n*The simplest way to create a Reddit bot*\n\n---\nWith **comis** there is no need to worry about writing complex logic. Instead, the use of decorators allows you to implement simple chaining of logic by abstracting the actions typically needed which gives you more time to worry about actions on the content. \n\n### Why did I create comis?\nAs a Reddit moderator, I realised some tasks could be easily done if automated. AutoModerator was not powerful enough and directly using the API was tedious and repetitive. I created **comis** to make it easier.\n',
    'author': 'Endercheif',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Endercheif/comis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
