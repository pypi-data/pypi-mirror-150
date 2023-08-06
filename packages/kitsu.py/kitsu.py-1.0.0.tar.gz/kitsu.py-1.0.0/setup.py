# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kitsu']

package_data = \
{'': ['*']}

modules = \
['LICENSE']
install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'kitsu.py',
    'version': '1.0.0',
    'description': 'kitsu.py is an asynchronous API wrapper for Kitsu written in Python.',
    'long_description': '<h1 align="center">Kitsu.py</h1>\n<p align="center">\n    <a href="https://pypi.python.org/pypi/kitsu.py">\n        <img src="https://img.shields.io/pypi/v/kitsu.py.svg?style=for-the-badge&color=orange&logo=&logoColor=white" />\n    </a>\n    <a href="https://github.com/MrArkon/kitsu.py/blob/master/LICENSE">\n        <img src="https://img.shields.io/pypi/l/kitsu.py?style=for-the-badge" />\n    </a>\n    <a>\n    <a href="https://www.codacy.com/gh/MrArkon/kitsu.py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MrArkon/kitsu.py&amp;utm_campaign=Badge_Grade">\n        <img src="https://img.shields.io/codacy/grade/a04e4a4edbb84f6ea6d0c5a091a912a5?style=for-the-badge" />\n    </a>\n    <br> kitsu.py is an asynchronous API wrapper for Kitsu written in Python.\n</p>\n\n## Key Features\n* Simple and modern Pythonic API using `async/await`\n* Fully typed\n* Filter & Limit functionality\n\n## Requirements\n\nPython 3.8+\n* [aiohttp](https://pypi.org/project/aiohttp/)\n* [python-dateutil](https://pypi.org/project/python-dateutil)\n\n## Installing\nTo install the library, run the following commands:\n```shell\n# Linux/MacOS\npython3 -m pip install -U kitsu.py\n\n# Windows\npy -3 -m pip install -U kitsu.py\n```\n\n## Usage\n\nSearch for an anime:\n```python\nimport kitsu\nimport asyncio\n\nclient = kitsu.Client()\n\nasync def main():\n    anime = await client.search_anime("jujutsu kaisen", limit=1)\n    \n    print("Canonical Title: " + anime.canonical_title)\n    print("Average Rating: " + str(anime.average_rating))\n    \n    # Close the internal aiohttp ClientSession\n    await client.close()\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\nThis prints:\n```\nCanonical Title: Jujutsu Kaisen\nAverage Rating: 85.98\n```\nYou can find more examples in the [examples](https://github.com/MrArkon/kitsu.py/tree/master/examples/) directory.\n    \n## Contributors\n* [Dymattic](https://github.com/dymattic)\n\n## License\n\nThis project is distributed under the [MIT](https://github.com/MrArkon/kitsu.py/blob/master/LICENSE.txt) license.\n',
    'author': 'MrArkon',
    'author_email': 'mrarkon@outlook.com',
    'maintainer': 'MrArkon',
    'maintainer_email': 'mrarkon@outlook.com',
    'url': 'https://github.com/MrArkon/kitsu.py/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
