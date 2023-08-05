# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nv', 'nv.utils.introspect', 'nv.utils.introspect.parsers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nv-utils-introspect',
    'version': '0.2.1',
    'description': 'Helpers to import from or serialize certain Python objects to strings based on their naming convention on a somehow safe manner.',
    'long_description': None,
    'author': 'Gustavo Santos',
    'author_email': 'gustavo@next.ventures',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nextventures/nv-utils-introspect.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
