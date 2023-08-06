# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacy_richtext_utils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'spacy>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'spacy-richtext-utils',
    'version': '0.1.0',
    'description': 'Spacy tokenizer and pipeline steps to exploit the semantics of a Rich Text, like HTML or RTF.',
    'long_description': None,
    'author': 'Massimo Rebuglio',
    'author_email': 'massimo.rebuglio@polito.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
