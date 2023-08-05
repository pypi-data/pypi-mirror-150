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
    'version': '0.1.1',
    'description': 'Closed Loop, Electrophysiology, and Optogenetics Simulator: testbed and prototyping kit',
    'long_description': '# `cleosim`: Closed Loop, Electrophysiology, and Optogenetics Simulator\n\n[![Test and lint](https://github.com/kjohnsen/cleosim/actions/workflows/test.yml/badge.svg)](https://github.com/kjohnsen/cleosim/actions/workflows/test.yml)\n[![Documentation Status](https://readthedocs.org/projects/cleosim/badge/?version=latest)](https://cleosim.readthedocs.io/en/latest/?badge=latest)\n\nHello there! This package has the goal of making it easy to simulate electrode recording, optogenetics, and real-time input and output processing with the Brian 2 spiking neural network simulator. While `cleosim` was created to facilitate prototyping closed-loop control experiments, we hope the electrode and optogenetics components will be useful outside this scope for the broader community of Brian users.\n\nThis package was developed by [Kyle Johnsen](https://kjohnsen.org) and Nathan Cruzado under the direction of [Chris Rozell](https://siplab.gatech.edu) at Georgia Institute of Technology.\n\n## Installation\nJust use pip:\n```\npip install cleosim\n```\n\n## Usage\n[Read the docs!](https://cleosim.readthedocs.io)',
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
