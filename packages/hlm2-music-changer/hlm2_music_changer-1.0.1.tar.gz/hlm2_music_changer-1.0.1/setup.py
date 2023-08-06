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
    'version': '1.0.1',
    'description': 'A Python module to make the installation and management of Hotline Miami 2 music mods simpler.',
    'long_description': "# Hotline Miami 2 Music Changer\n### (a.k.a. hlm2_music_changer or hlm2mc)\nA Python module to make the installation and management of Hotline Miami 2 music mods simpler.\n\n## Installation\n- Make sure you have Python version 3.9 or above installed. If you don't, it can be downloaded [here](https://www.python.org/downloads/)\n- Make sure you have `pip` installed (more about installing `pip` [here](https://pip.pypa.io/en/stable/installation/))\n- Run `pip install hlm2_music_changer`\n- The package and dependencies should download and install automatically\n\n## Running after installation\nSimply run `hlm2mc` in your command processor of choice\n\n## Development\nThis project uses `poetry` for packaging and dependancy management. More about `poetry` can be found [here](https://python-poetry.org/docs/).\n\nOnce `poetry` is installed,\n- Clone this repository locally using `git clone https://github.com/generic-user1/hlm2_music_changer.git`\n- Enter the repository directory using `cd hlm2_music_changer`\n- Install a virtual environment with the appropriate dependencies using `poetry install`\n- Run the project using `poetry run hlm2mc`\n\n## Links\nPyPI: https://pypi.org/project/hlm2-music-changer\n\nGitHub: https://github.com/generic-user1/hlm2_music_changer\n\n## Other notes\nYou can purchase [Hotline Miami 2: Wrong Number](https://store.steampowered.com/app/274170/Hotline_Miami_2_Wrong_Number/) on [Steam](https://store.steampowered.com/). \nPlease note that the author of this software is not affiliated with Devolver Digital or Dennaton Games. This software is in no way official.\n",
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
