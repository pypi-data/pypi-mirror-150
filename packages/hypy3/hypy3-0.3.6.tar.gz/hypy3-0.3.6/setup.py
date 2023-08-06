# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypy', 'hypy.modules']

package_data = \
{'': ['*']}

install_requires = \
['asciitree>=0.3.3,<0.4.0',
 'click>=7.0,<8.0',
 'paramiko>=2.6,<3.0',
 'pywinrm>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['hypy = hypy.__main__:cli']}

setup_kwargs = {
    'name': 'hypy3',
    'version': '0.3.6',
    'description': 'Multiplataform Hyper-V Manager using Python and FreeRDP',
    'long_description': None,
    'author': 'Gabriel Avanzi',
    'author_email': 'gabriel.avanzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
