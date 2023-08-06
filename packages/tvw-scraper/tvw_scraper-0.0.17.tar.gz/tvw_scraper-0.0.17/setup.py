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
    'version': '0.0.17',
    'description': 'Scraping tradingview.com',
    'long_description': "# tvw_scraper\nuse asyncio and websockets to retrieve candles and symbol info from tradingview.com\n\nUsage example:\n\nretrieve symbols to use them later in websocket queries\n```python\nfrom tvw_scraper.rest import SymbolScanner\nfrom tvw_scraper.models import Sectors\n\nSymbolScanner.get_sector_symbols(Sectors.russia)\n{'totalCount': 937, 'data': [{'s': 'MOEX:AFKS', 'd': []}, {'s': 'MOEX:JNJ-RM', 'd': []} . . .\n```\n\nretrieve candles and some info from tradingview websocket:\n```python\nimport asyncio\nfrom tvw_scraper.scraper import TradingviewWsScraper\nfrom tvw_scraper.models import Intervals\n\nscraper = TradingviewWsScraper()\n\nasync def main():\n    result = await asyncio.gather(*[\n        scraper.get_candles('NASDAQ:NVDA',Intervals.interval_1day), \n        scraper.get_candles('NASDAQ:NVDA',Intervals.interval_1hour), \n        scraper.get_symbol('NASDAQ:NVDA')\n        ])\n\n\nasyncio.get_event_loop().run_until_complete(main())\n```",
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
