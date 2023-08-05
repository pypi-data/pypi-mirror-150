# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cleosim', 'cleosim.electrodes', 'cleosim.processing']

package_data = \
{'': ['*']}

install_requires = \
['bidict',
 'brian2>=2.4,<3.0,!=2.5.0.2',
 'matplotlib>=3.4,<4.0',
 'nptyping>=1.4.4,<2.0.0',
 'numpy>=1.16,<2.0',
 'scipy',
 'tklfp>=0.1,<0.2']

setup_kwargs = {
    'name': 'cleosim',
    'version': '0.1.0',
    'description': 'Closed Loop, Electrophysiology, and Optogenetics Simulator: testbed and prototyping kit',
    'long_description': None,
    'author': 'Kyle Johnsen',
    'author_email': 'kyle@kjohnsen.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cleosim.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
