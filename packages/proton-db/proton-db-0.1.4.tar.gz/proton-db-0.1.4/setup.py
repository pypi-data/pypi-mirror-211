# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proton_db']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'proton-db',
    'version': '0.1.4',
    'description': 'A simple wrapper for the unofficial Proton-DB API.',
    'long_description': "Lightweight wrapper for the unofficial Proton-DB API (https://protondb.max-p.me/)\n\nUsage:\nimport proton_db as proton\n\nprotonDB = proton.protonDB()\n\n\ngetGames()\nLists all the games we have discovered so far. Returns an array of objects with these fields in it:\n\nappId\ntitle\n\ngetReports(appId)\nLists all reports for a given game (by Valve's appId), in reverse timestamp order. Returns an array of objects with these fields in it:\n\nid - Server's local id\nappId - The game ID for this report. Redundant for uniformity's sake.\ntimestamp\nrating\nnotes\nos\ngpuDriver\nspecs\nprotonVersion\n\n\n",
    'author': 'BiFr0st',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
