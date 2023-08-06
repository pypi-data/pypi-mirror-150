# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nssurge_cli']

package_data = \
{'': ['*']}

install_requires = \
['nssurge-api==0.2.10',
 'rich[format]>=12.4.1,<13.0.0',
 'typer>=0.4.1,<0.5.0',
 'utils-tddschn>=0.1.5,<0.2.0']

entry_points = \
{'console_scripts': ['nsg = nssurge_cli:cli.app',
                     'nssurge-cli = nssurge_cli:cli.app']}

setup_kwargs = {
    'name': 'nssurge-cli',
    'version': '2.0.2',
    'description': '',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/nssurge-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
