# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ncm']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'siscomex-ncm',
    'version': '1.0.0',
    'description': 'API access to the NCM (Nomenclatura Comum do Mercosul) by Siscomex',
    'long_description': None,
    'author': 'Leonardo Gregianin',
    'author_email': 'leogregianin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
