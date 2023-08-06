# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aitg_doctools']

package_data = \
{'': ['*']}

install_requires = \
['sacremoses>=0.0.45,<0.0.46', 'spacy>=3.1.2,<4.0.0']

setup_kwargs = {
    'name': 'aitg-doctools',
    'version': '0.2.0',
    'description': 'a library for cleaning and chunking documents',
    'long_description': None,
    'author': 'redthing1',
    'author_email': 'redthing1@alt.icu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
