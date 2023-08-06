# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rhoknp', 'rhoknp.pas', 'rhoknp.processors', 'rhoknp.units', 'rhoknp.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rhoknp',
    'version': '0.1.0',
    'description': 'Yet another Python binding for Juman++/KNP',
    'long_description': None,
    'author': 'Hirokazu Kiyomaru',
    'author_email': 'h.kiyomaru@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ku-nlp/rhoknp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
