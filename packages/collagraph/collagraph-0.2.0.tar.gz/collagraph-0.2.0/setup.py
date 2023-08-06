# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['collagraph',
 'collagraph.cgx',
 'collagraph.components',
 'collagraph.renderers',
 'collagraph.renderers.pyside',
 'collagraph.renderers.pyside.objects']

package_data = \
{'': ['*']}

install_requires = \
['observ>=0.9.2,<0.10.0']

extras_require = \
{'pygfx': ['pygfx>=0.1.9,<0.2.0'],
 'pyside:python_version < "3.11"': ['pyside6_essentials>=6.3,<6.4']}

setup_kwargs = {
    'name': 'collagraph',
    'version': '0.2.0',
    'description': 'Reactive user interfaces',
    'long_description': '[![PyPI version](https://badge.fury.io/py/collagraph.svg)](https://badge.fury.io/py/collagraph)\n[![CI status](https://github.com/fork-tongue/collagraph/workflows/CI/badge.svg)](https://github.com/fork-tongue/collagraph/actions)\n\n# Collagraph 📓\n\nReactive user interfaces.\n\n> The word [Collagraphy](https://en.wikipedia.org/wiki/Collagraphy) is derived from the Greek word _koll_ or _kolla_, meaning glue, and graph, meaning the activity of drawing.\n\nCurrently in alpha.\n',
    'author': 'Berend Klein Haneveld',
    'author_email': 'berendkleinhaneveld@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fork-tongue/collagraph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
