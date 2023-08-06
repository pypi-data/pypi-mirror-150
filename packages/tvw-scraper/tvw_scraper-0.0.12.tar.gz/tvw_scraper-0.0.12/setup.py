# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tvw_scraper']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'dataclass-factory>=2.14,<3.0',
 'inflection>=0.5.1,<0.6.0',
 'regex>=2022.1.18,<2023.0.0',
 'tenacity>=8.0.1,<9.0.0',
 'uplink>=0.9.7,<0.10.0',
 'websocket-client>=1.2.3,<2.0.0',
 'websockets>=10.2,<11.0']

setup_kwargs = {
    'name': 'tvw-scraper',
    'version': '0.0.12',
    'description': 'Scraping tradingview.com',
    'long_description': '',
    'author': 'fip',
    'author_email': 'ogremagi9@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ogremagi4/tvw_scraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
