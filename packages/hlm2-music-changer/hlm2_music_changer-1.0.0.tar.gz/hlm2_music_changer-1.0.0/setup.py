# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hlm2_music_changer']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0']

entry_points = \
{'console_scripts': ['hlm2mc = hlm2_music_changer.hlm2mc:main']}

setup_kwargs = {
    'name': 'hlm2-music-changer',
    'version': '1.0.0',
    'description': 'A Python module to make the installation and management of Hotline Miami 2 music mods simpler.',
    'long_description': None,
    'author': 'generic-user1',
    'author_email': '89677116+generic-user1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
