# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rajinipp', 'rajinipp.ast', 'rajinipp.parser']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'munch>=2.5.0,<3.0.0',
 'rply>=0.7.8,<0.8.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['rajinipp = rajinipp.__main__:app']}

setup_kwargs = {
    'name': 'rajinipp',
    'version': '0.2.0',
    'description': 'Rajini++ (rajiniPP) is a programming language based on the iconic dialogues by Rajinikanth.',
    'long_description': None,
    'author': 'Aadhithya Sankar',
    'author_email': 'a.sankar@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.8,<3.11',
}


setup(**setup_kwargs)
